#!/usr/bin/env python3

import csv
import html as htmlmod
import json
import random
import re
import subprocess
import time
from typing import Dict, List, Optional, Tuple

UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/122.0.0.0 Safari/537.36"
)


def _sleep(base: float, jitter: float) -> None:
    time.sleep(base + random.random() * jitter)


def fetch(url: str, retries: int = 3) -> str:
    """Fetch a URL using curl."""
    for attempt in range(retries):
        cmd = [
            "curl",
            "-s",
            "-L",
            "--compressed",
            "-A",
            UA,
            "-H",
            "Accept-Language: en-AU,en;q=0.9",
            "-H",
            "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            url
        ]

        try:
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=40)
            out = res.stdout or ""
            if out.strip():
                return out
        except Exception:
            pass

        _sleep(2.0 * (attempt + 1), 1.0)

    return ""


ID_RE = re.compile(r"/A(\d{8})")


def extract_account_id(detail_url: str) -> str:
    m = ID_RE.search(detail_url)
    return f"A{m.group(1)}" if m else detail_url


def clean_ws(s: str) -> str:
    return re.sub(r"\s+", " ", s or "").strip()


def parse_suburb_links(page_html: str, state: str) -> List[str]:
    if not page_html:
        return []
    links = re.findall(rf"https://www\\.dentist\\.com\\.au/dentist/{state}/[a-z0-9-]+", page_html)
    seen = set()
    out = []
    for u in links:
        if u not in seen:
            seen.add(u)
            out.append(u)
    return out


def parse_premium_blocks(page_html: str) -> List[Dict[str, str]]:
    if not page_html:
        return []
    dentists = []
    blocks = re.split(r'<div class="info-row">', page_html)
    for block in blocks[1:]:
        name_match = re.search(r'<h3><a[^>]+href="([^"]+)"[^>]*>([^<]+)</a>', block)
        if not name_match:
            continue
        detail_url = name_match.group(1).strip()
        name = htmlmod.unescape(name_match.group(2).strip())

        address_match = re.search(r"<address>(.*?)</address>", block, re.S)
        address = ""
        if address_match:
            address = htmlmod.unescape(clean_ws(address_match.group(1)))

        phone_match = re.search(r'href="tel:([^"]+)"', block)
        phone = clean_ws(phone_match.group(1)) if phone_match else ""

        dentists.append(
            {
                "id": extract_account_id(detail_url),
                "name": name,
                "address": address,
                "detail_url": detail_url,
                "phone": phone,
                "website": "",
            }
        )
    return dentists


def parse_map_markers(page_html: str) -> List[Dict[str, str]]:
    if not page_html:
        return []
    m = re.search(r"mapData\s*=\s*JSON\.parse\(\"(.*?)\"\);", page_html, re.S)
    if not m:
        return []

    raw = m.group(1)
    raw = raw.replace("\\/", "/").replace("\\\"", '"')

    try:
        data = json.loads(raw)
    except Exception:
        try:
            # Try unescaping unicode
            data = json.loads(raw.encode("utf-8").decode("unicode_escape"))
        except Exception:
            return []

    markers = data.get("markers", [])
    out = []
    for mk in markers:
        title = htmlmod.unescape(mk.get("title", "") or "")
        html_content = mk.get("html", "") or ""
        url_match = re.search(r"href='([^']+)'", html_content)
        addr_match = re.search(r"<br/>(.*)", html_content)
        detail_url = url_match.group(1) if url_match else ""
        address = clean_ws(htmlmod.unescape(addr_match.group(1))) if addr_match else ""

        if not detail_url:
            continue

        out.append(
            {
                "id": extract_account_id(detail_url),
                "name": title,
                "address": address,
                "detail_url": detail_url,
                "phone": "",
                "website": "",
            }
        )
    return out


def parse_detail_page(detail_html: str) -> Tuple[str, str]:
    if not detail_html:
        return "", ""

    phone_match = re.search(r'href="tel:([^"]+)"', detail_html)
    phone = clean_ws(phone_match.group(1)) if phone_match else ""

    website = ""
    m = re.search(r'<a class="coffsd-link loggerable-external-link"[^>]* data="([^"]+)"', detail_html)
    if m:
        website = clean_ws(m.group(1))
    else:
        for mm in re.finditer(r'data="([^"]+)"', detail_html):
            cand = clean_ws(mm.group(1))
            if cand.startswith("http") and not any(b in cand for b in ["centaurportal.com", "dentist.com.au", "googletagmanager", "google.com"]):
                website = cand
                break

    return phone, website


def harvest_state(
    state: str,
    seed_urls: List[str],
    target_min: int = 300,
    max_pages: int = 150,
) -> List[Dict[str, str]]:
    leads: Dict[str, Dict[str, str]] = {}
    visited = set()
    queue = list(seed_urls)

    pages = 0
    while queue and len(leads) < target_min and pages < max_pages:
        url = queue.pop(0)
        if url in visited:
            continue
        visited.add(url)
        pages += 1

        print(f"[{state.upper()}] Fetching {url} (Leads: {len(leads)})", flush=True)
        page_html = fetch(url)
        if not page_html:
            continue

        for d in parse_premium_blocks(page_html):
            leads.setdefault(d["id"], d)
            if d.get("phone") and not leads[d["id"]].get("phone"):
                leads[d["id"]]["phone"] = d["phone"]
            if d.get("address") and not leads[d["id"]].get("address"):
                leads[d["id"]]["address"] = d["address"]

        for d in parse_map_markers(page_html):
            if d["id"] not in leads:
                leads[d["id"]] = d
            else:
                if d.get("address") and not leads[d["id"]].get("address"):
                    leads[d["id"]]["address"] = d["address"]

        if len(leads) < target_min:
            for sl in parse_suburb_links(page_html, state):
                if sl not in visited and sl not in queue:
                    queue.append(sl)

        _sleep(1.0, 1.0)

    final: List[Dict[str, str]] = []
    ids = list(leads.keys())
    random.shuffle(ids)

    print(f"[{state.upper()}] Enriching {min(len(ids), target_min)} leads...", flush=True)

    count = 0
    for acc_id in ids:
        if count >= target_min:
            break
        d = leads[acc_id]

        if not d.get("phone") or not d.get("website"):
            detail_html = fetch(d["detail_url"])
            phone, website = parse_detail_page(detail_html)
            if phone: d["phone"] = phone
            if website: d["website"] = website
            _sleep(0.5, 0.5)

        if not d.get("phone") or not d.get("address"):
            continue

        final.append({
            "Practice Name": d["name"],
            "Address": d["address"],
            "Phone": d["phone"],
            "Website": d["website"]
        })
        count += 1
        if count % 10 == 0:
            print(f"[{state.upper()}] Progress: {count}/{target_min}", flush=True)

    return final


def write_csv(rows: List[Dict[str, str]], path: str) -> None:
    fields = ["Practice Name", "Address", "Phone", "Website"]
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)


def main():
    states = {
        "vic": [
            "https://www.dentist.com.au/dentist/vic/melbourne",
            "https://www.dentist.com.au/dentist/vic/richmond",
            "https://www.dentist.com.au/dentist/vic/south-yarra",
            "https://www.dentist.com.au/dentist/vic/geelong",
            "https://www.dentist.com.au/dentist/vic/ballarat"
        ],
        "nsw": [
            "https://www.dentist.com.au/dentist/nsw/sydney",
            "https://www.dentist.com.au/dentist/nsw/parramatta",
            "https://www.dentist.com.au/dentist/nsw/chatswood",
            "https://www.dentist.com.au/dentist/nsw/newcastle",
            "https://www.dentist.com.au/dentist/nsw/wollongong"
        ],
        "qld": [
            "https://www.dentist.com.au/dentist/qld/brisbane",
            "https://www.dentist.com.au/dentist/qld/gold-coast",
            "https://www.dentist.com.au/dentist/qld/sunshine-coast",
            "https://www.dentist.com.au/dentist/qld/townsville",
            "https://www.dentist.com.au/dentist/qld/cairns"
        ]
    }

    for state, seeds in states.items():
        print(f"Starting harvest for {state.upper()}...", flush=True)
        rows = harvest_state(state, seeds, target_min=300)
        filename = f"Spectrum_{state.upper()}_300.csv"
        write_csv(rows, filename)
        # Also save to projects folder
        import os
        if not os.path.exists("projects"):
            os.makedirs("projects")
        write_csv(rows, os.path.join("projects", filename))
        print(f"Finished {state.upper()}. Saved to {filename} and projects/{filename}. Total leads: {len(rows)}", flush=True)


if __name__ == "__main__":
    main()
