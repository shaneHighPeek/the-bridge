#!/usr/bin/env python3

import csv
import html as htmlmod
import json
import random
import re
import subprocess
import time
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/122.0.0.0 Safari/537.36"
)


def _sleep(base: float, jitter: float) -> None:
    time.sleep(base + random.random() * jitter)


def fetch(url: str, post: Optional[Dict[str, str]] = None, retries: int = 3) -> str:
    """Fetch a URL using curl (more browser-like than urllib in this environment)."""
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
        ]
        if post:
            cmd.append("-X")
            cmd.append("POST")
            for k, v in post.items():
                cmd.extend(["--data", f"{k}={v}"])
        cmd.append(url)

        try:
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=40)
            out = res.stdout or ""
            # Some blocking pages return HTML but extremely short; still return and let parsers fail.
            if out.strip():
                return out
        except Exception:
            pass

        _sleep(1.5 * (attempt + 1), 0.8)

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
    # De-dupe while preserving order
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
    # mapData = JSON.parse("...");
    m = re.search(r"mapData\s*=\s*JSON\\.parse\(\"(.*?)\"\);", page_html, re.S)
    if not m:
        return []

    raw = m.group(1)
    # Unescape common patterns first
    raw = raw.replace("\\/", "/").replace("\\\"", '"')

    candidates = []
    # Try a few decoding strategies
    candidates.append(raw)
    try:
        candidates.append(raw.encode("utf-8").decode("unicode_escape"))
    except Exception:
        pass

    for cand in candidates:
        try:
            data = json.loads(cand)
        except Exception:
            continue

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

    return []


def parse_detail_page(detail_html: str) -> Tuple[str, str]:
    """Return (phone, website) from a detail page HTML."""
    if not detail_html:
        return "", ""

    phone_match = re.search(r'href="tel:([^"]+)"', detail_html)
    phone = clean_ws(phone_match.group(1)) if phone_match else ""

    # Prefer the dedicated website link
    website = ""
    m = re.search(r'<a class="coffsd-link loggerable-external-link"[^>]* data="([^"]+)"', detail_html)
    if m:
        website = clean_ws(m.group(1))
    else:
        # Fallback: choose first plausible external link in data=...
        for mm in re.finditer(r'class="[^"]*loggerable-external-link[^"]*"[^>]* data="([^"]+)"', detail_html):
            cand = clean_ws(mm.group(1))
            if not cand:
                continue
            bad = (
                "centaurportal.com",
                "dentist.com.au",
                "javascript:",
            )
            if any(b in cand for b in bad):
                continue
            website = cand
            break

    return phone, website


def harvest_state(
    state: str,
    seed_urls: List[str],
    target_min: int = 320,
    max_pages: int = 220,
) -> List[Dict[str, str]]:
    """Crawl listing pages until we have enough unique practices; then enrich via detail pages."""

    leads: Dict[str, Dict[str, str]] = {}

    visited = set()
    queue = list(seed_urls)

    pages = 0
    while queue and len(leads) < max(target_min, 320) and pages < max_pages:
        url = queue.pop(0)
        if url in visited:
            continue
        visited.add(url)
        pages += 1

        page_html = fetch(url)
        if not page_html:
            continue

        # Premium blocks (often include phone)
        for d in parse_premium_blocks(page_html):
            leads.setdefault(d["id"], d)
            # If we already had it but without phone/address, merge
            if d.get("phone") and not leads[d["id"]].get("phone"):
                leads[d["id"]]["phone"] = d["phone"]
            if d.get("address") and not leads[d["id"]].get("address"):
                leads[d["id"]]["address"] = d["address"]

        # Map markers (good coverage)
        for d in parse_map_markers(page_html):
            if d["id"] not in leads:
                leads[d["id"]] = d
            else:
                # merge address if missing
                if d.get("address") and not leads[d["id"]].get("address"):
                    leads[d["id"]]["address"] = d["address"]

        # Only expand suburbs if we still need more
        if len(leads) < target_min:
            for sl in parse_suburb_links(page_html, state)[:160]:
                if sl not in visited and sl not in queue:
                    queue.append(sl)

        if pages % 5 == 0:
            print(f"{state.upper()} progress: leads={len(leads)} pages={pages} queue={len(queue)}", flush=True)

        _sleep(0.8, 1.2)  # polite pacing

    # Enrich details for at least target_min leads
    final: List[Dict[str, str]] = []

    ids = list(leads.keys())
    # deterministic-ish but varied order to spread load
    random.shuffle(ids)

    for i, acc_id in enumerate(ids):
        if len(final) >= target_min:
            break
        d = leads[acc_id]

        # Ensure detail URL exists
        if not d.get("detail_url"):
            continue

        if not d.get("phone") or d.get("website") is None:
            detail_html = fetch(d["detail_url"], retries=2)
            phone, website = parse_detail_page(detail_html)
            if phone and not d.get("phone"):
                d["phone"] = phone
            if website and not d.get("website"):
                d["website"] = website
            _sleep(0.4, 0.8)

        # Require phone + address for integrity; website can be blank.
        if not d.get("phone"):
            continue
        if not d.get("address"):
            continue

        final.append(
            {
                "Practice Name": d.get("name", ""),
                "Phone Number": d.get("phone", ""),
                "Full Address": d.get("address", ""),
                "Website URL": d.get("website", ""),
            }
        )

        if (i + 1) % 25 == 0:
            print(f"{state.upper()} enriched: {len(final)}/{target_min}", flush=True)

    return final


def write_csv(rows: List[Dict[str, str]], path: str) -> None:
    fields = ["Practice Name", "Phone Number", "Full Address", "Website URL"]
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in rows:
            w.writerow({k: (r.get(k, "") or "") for k in fields})


def main() -> None:
    random.seed(42)

    # NSW: Sydney metro extensively, then Newcastle, Wollongong, Central Coast, Wagga Wagga
    nsw_seeds = [
        "https://www.dentist.com.au/dentist/nsw/sydney",
        "https://www.dentist.com.au/dentist/nsw/newcastle",
        "https://www.dentist.com.au/dentist/nsw/wollongong",
        "https://www.dentist.com.au/dentist/nsw/central-coast",
        "https://www.dentist.com.au/dentist/nsw/wagga-wagga",
    ]

    # QLD: Brisbane, Gold Coast, Sunshine Coast, Townsville, Cairns
    qld_seeds = [
        "https://www.dentist.com.au/dentist/qld/brisbane",
        "https://www.dentist.com.au/dentist/qld/gold-coast",
        "https://www.dentist.com.au/dentist/qld/sunshine-coast",
        "https://www.dentist.com.au/dentist/qld/townsville",
        "https://www.dentist.com.au/dentist/qld/cairns",
    ]

    nsw_rows = harvest_state("nsw", nsw_seeds, target_min=320, max_pages=220)
    write_csv(nsw_rows, "Spectrum_Dental_NSW_Lead_List.csv")
    print(f"NSW CSV ready: {len(nsw_rows)} rows", flush=True)

    qld_rows = harvest_state("qld", qld_seeds, target_min=320, max_pages=220)
    write_csv(qld_rows, "Spectrum_Dental_QLD_Lead_List.csv")
    print(f"QLD CSV ready: {len(qld_rows)} rows", flush=True)


if __name__ == "__main__":
    main()
