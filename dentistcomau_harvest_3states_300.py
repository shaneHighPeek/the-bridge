#!/usr/bin/env python3

"""Resilient suburb-by-suburb harvest of dentist.com.au leads (VIC, NSW, QLD).

Outputs:
- Spectrum_VIC_300.csv
- Spectrum_NSW_300.csv
- Spectrum_QLD_300.csv

Fields:
- Practice Name
- Address
- Phone
- Website

Notes:
- Listing pages show only a few premium results in static HTML.
- The bulk of results are loaded via AJAX POST:
    https://www.dentist.com.au/index.php/ajax/processing_module
    module=dsearch
    cmd=dentist:results:standard_list:search
    current_page=N
    address="Suburb, STATE, POSTCODE"
- We crawl listing pages, discover suburb links, then paginate AJAX results.
- We then enrich each record via the practice detail page to obtain Website.
"""

import csv
import html as htmlmod
import os
import random
import re
import subprocess
import time
from collections import deque
from typing import Deque, Dict, List, Optional, Tuple

UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/122.0.0.0 Safari/537.36"
)

AJAX_URL = "https://www.dentist.com.au/index.php/ajax/processing_module"


def _sleep(base: float, jitter: float) -> None:
    time.sleep(base + random.random() * jitter)


def fetch(url: str, post: Optional[Dict[str, str]] = None, retries: int = 3, timeout: int = 45) -> str:
    """Fetch a URL using curl (often more resilient than urllib here)."""
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
            cmd.extend(["-X", "POST"])
            # data-urlencode so addresses with spaces/commas are safe
            for k, v in post.items():
                cmd.extend(["--data-urlencode", f"{k}={v}"])
        cmd.append(url)

        try:
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
            out = res.stdout or ""
            if out.strip():
                return out
        except Exception:
            pass

        _sleep(1.2 * (attempt + 1), 0.9)

    return ""


ID_RE = re.compile(r"/A(\d{8})")


def extract_account_id(detail_url: str) -> str:
    m = ID_RE.search(detail_url or "")
    return f"A{m.group(1)}" if m else (detail_url or "")


def clean_ws(s: str) -> str:
    s = s or ""
    s = s.replace("&nbsp;", " ")
    s = htmlmod.unescape(s)
    return re.sub(r"\s+", " ", s).strip()


def parse_address_var(page_html: str) -> str:
    """Extract the JS variable: var address = "Melbourne, VIC, 3000";"""
    if not page_html:
        return ""
    m = re.search(r'var\s+address\s*=\s*"([^"]+)"', page_html)
    return clean_ws(m.group(1)) if m else ""


def parse_suburb_links(page_html: str, state: str) -> List[str]:
    if not page_html:
        return []
    abs_links = re.findall(rf"https://www\.dentist\.com\.au/dentist/{state}/[a-z0-9-]+", page_html)
    rel_links = re.findall(rf"/dentist/{state}/[a-z0-9-]+", page_html)
    seen = set()
    out: List[str] = []
    for u in abs_links + rel_links:
        if u.startswith("/"):
            u = f"https://www.dentist.com.au{u}"
        if u not in seen:
            seen.add(u)
            out.append(u)
    return out


def parse_listing_blocks(page_html: str) -> List[Dict[str, str]]:
    """Parse dentist listing blocks from either premium HTML or standard AJAX HTML."""
    if not page_html:
        return []

    dentists: List[Dict[str, str]] = []

    # Blocks start with <div class="info-row"> or <div class="info-row bg">
    blocks = re.split(r'<div class="info-row(?:\s+bg)?">', page_html)
    for block in blocks[1:]:
        name_match = re.search(r'<h3><a[^>]+href="([^"]+)"[^>]*>([^<]+)</a>', block)
        if not name_match:
            continue
        detail_url = clean_ws(name_match.group(1))
        name = clean_ws(name_match.group(2))
        acc_id = extract_account_id(detail_url)

        address = ""
        m_addr = re.search(r"<address[^>]*>(.*?)</address>", block, re.S)
        if m_addr:
            address = clean_ws(m_addr.group(1))
        else:
            m_p = re.search(r"<p>\s*(.*?)\s*</p>", block, re.S)
            if m_p:
                address = clean_ws(m_p.group(1))

        phone = ""
        m_tel = re.search(r'href="tel:([^"]+)"', block)
        if m_tel:
            phone = clean_ws(m_tel.group(1))

        dentists.append(
            {
                "id": acc_id,
                "name": name,
                "address": address,
                "detail_url": detail_url,
                "phone": phone,
                "website": "",
            }
        )

    return dentists


def ajax_get_total_pages_and_page(address: str, current_page: int) -> Tuple[int, str]:
    html = fetch(
        AJAX_URL,
        post={
            "module": "dsearch",
            "cmd": "dentist:results:standard_list:search",
            "current_page": str(current_page),
            "address": address,
            "type": "",
            "value": "",
        },
        retries=3,
        timeout=55,
    )
    if not html:
        return 0, ""

    m = re.search(r'id="total_pages"\s+value="(\d+)"', html)
    total_pages = int(m.group(1)) if m else 1
    return total_pages, html


def enrich_from_detail(detail_url: str) -> Tuple[str, str]:
    dh = fetch(detail_url, retries=2, timeout=55)
    if not dh:
        return "", ""

    m_tel = re.search(r'href="tel:([^"]+)"', dh)
    phone = clean_ws(m_tel.group(1)) if m_tel else ""

    website = ""
    m_web = re.search(r'<a class="coffsd-link loggerable-external-link"[^>]* data="([^"]+)"', dh)
    if m_web:
        website = clean_ws(m_web.group(1))
    else:
        for mm in re.finditer(r'class="[^"]*loggerable-external-link[^"]*"[^>]* data="([^"]+)"', dh):
            cand = clean_ws(mm.group(1))
            if not cand:
                continue
            if any(bad in cand for bad in ("centaurportal.com", "dentist.com.au", "javascript:")):
                continue
            website = cand
            break

    return phone, website


def crawl_state(
    state: str,
    seed_urls: List[str],
    metro_url: str,
    target_final: int = 300,
    target_pool: int = 480,
    max_listing_pages: int = 180,
) -> List[Dict[str, str]]:
    leads: Dict[str, Dict[str, str]] = {}

    q: Deque[str] = deque(seed_urls)
    queued = set(seed_urls)
    visited = set()

    listing_pages_processed = 0

    while q and len(leads) < target_pool and listing_pages_processed < max_listing_pages:
        url = q.popleft()
        queued.discard(url)
        if url in visited:
            continue
        visited.add(url)
        listing_pages_processed += 1

        page_html = fetch(url)
        if not page_html:
            continue

        address_key = parse_address_var(page_html)

        # 1) Premium/static listings
        for d in parse_listing_blocks(page_html):
            acc_id = d["id"]
            if not acc_id:
                continue
            if acc_id not in leads:
                leads[acc_id] = d
            else:
                for k in ("name", "address", "detail_url", "phone"):
                    if d.get(k) and not leads[acc_id].get(k):
                        leads[acc_id][k] = d[k]

        # 2) Standard listings via AJAX (paginate)
        if address_key:
            total_pages, first_html = ajax_get_total_pages_and_page(address_key, 1)
            if first_html:
                for d in parse_listing_blocks(first_html):
                    acc_id = d["id"]
                    if not acc_id:
                        continue
                    if acc_id not in leads:
                        leads[acc_id] = d
                    else:
                        for k in ("name", "address", "detail_url", "phone"):
                            if d.get(k) and not leads[acc_id].get(k):
                                leads[acc_id][k] = d[k]

            _sleep(0.35, 0.55)

            for p in range(2, max(2, total_pages + 1)):
                if len(leads) >= target_pool:
                    break
                _, ph = ajax_get_total_pages_and_page(address_key, p)
                if not ph:
                    continue
                for d in parse_listing_blocks(ph):
                    acc_id = d["id"]
                    if not acc_id:
                        continue
                    if acc_id not in leads:
                        leads[acc_id] = d
                    else:
                        for k in ("name", "address", "detail_url", "phone"):
                            if d.get(k) and not leads[acc_id].get(k):
                                leads[acc_id][k] = d[k]
                _sleep(0.35, 0.65)

        # 3) Expand suburbs
        if len(leads) < target_pool:
            subs = parse_suburb_links(page_html, state)
            if url == metro_url:
                subs = subs[:240]
                for sl in reversed(subs):
                    if sl not in visited and sl not in queued:
                        q.appendleft(sl)
                        queued.add(sl)
            else:
                subs = subs[:140]
                for sl in subs:
                    if sl not in visited and sl not in queued:
                        q.append(sl)
                        queued.add(sl)

        if listing_pages_processed % 5 == 0:
            print(
                f"{state.upper()} listings: leads={len(leads)} pages={listing_pages_processed} queue={len(q)}",
                flush=True,
            )

        _sleep(0.55, 0.95)

    # Enrichment phase
    ids = list(leads.keys())
    random.shuffle(ids)

    final: List[Dict[str, str]] = []
    enriched = 0

    for acc_id in ids:
        if len(final) >= target_final:
            break

        d = leads[acc_id]
        detail_url = d.get("detail_url") or ""
        if not detail_url:
            continue

        if not d.get("phone") or not d.get("website"):
            phone, website = enrich_from_detail(detail_url)
            if phone and not d.get("phone"):
                d["phone"] = phone
            if website and not d.get("website"):
                d["website"] = website
            enriched += 1
            if enriched % 30 == 0:
                print(f"{state.upper()} enriched detail pages: {enriched}", flush=True)
            _sleep(0.25, 0.55)

        if not d.get("name") or not d.get("phone") or not d.get("address"):
            continue

        # Ensure Website is populated; fall back to detail URL if external website not available
        website_out = d.get("website") or detail_url

        final.append(
            {
                "Practice Name": d.get("name", ""),
                "Address": d.get("address", ""),
                "Phone": d.get("phone", ""),
                "Website": website_out,
            }
        )

    return final


def write_csv(rows: List[Dict[str, str]], path: str) -> None:
    fields = ["Practice Name", "Address", "Phone", "Website"]
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in rows:
            w.writerow({k: (r.get(k, "") or "") for k in fields})


def main() -> None:
    random.seed(42)

    cfgs = {
        "vic": {
            "seeds": [
                "https://www.dentist.com.au/dentist/vic/melbourne",
                "https://www.dentist.com.au/dentist/vic/geelong",
                "https://www.dentist.com.au/dentist/vic/ballarat",
                "https://www.dentist.com.au/dentist/vic/bendigo",
                "https://www.dentist.com.au/dentist/vic/mornington",
            ],
            "metro": "https://www.dentist.com.au/dentist/vic/melbourne",
            "out": "Spectrum_VIC_300.csv",
        },
        "nsw": {
            "seeds": [
                "https://www.dentist.com.au/dentist/nsw/sydney",
                "https://www.dentist.com.au/dentist/nsw/newcastle",
                "https://www.dentist.com.au/dentist/nsw/wollongong",
                "https://www.dentist.com.au/dentist/nsw/central-coast",
                "https://www.dentist.com.au/dentist/nsw/wagga-wagga",
            ],
            "metro": "https://www.dentist.com.au/dentist/nsw/sydney",
            "out": "Spectrum_NSW_300.csv",
        },
        "qld": {
            "seeds": [
                "https://www.dentist.com.au/dentist/qld/brisbane",
                "https://www.dentist.com.au/dentist/qld/gold-coast",
                "https://www.dentist.com.au/dentist/qld/sunshine-coast",
                "https://www.dentist.com.au/dentist/qld/townsville",
                "https://www.dentist.com.au/dentist/qld/cairns",
            ],
            "metro": "https://www.dentist.com.au/dentist/qld/brisbane",
            "out": "Spectrum_QLD_300.csv",
        },
    }

    os.makedirs("projects", exist_ok=True)

    for state, c in cfgs.items():
        print(f"\n=== START {state.upper()} ===", flush=True)
        rows = crawl_state(
            state,
            seed_urls=c["seeds"],
            metro_url=c["metro"],
            target_final=300,
            target_pool=520,
            max_listing_pages=190,
        )
        print(f"{state.upper()} complete: {len(rows)} rows", flush=True)

        out_path = c["out"]
        write_csv(rows, out_path)
        write_csv(rows, os.path.join("projects", out_path))
        print(f"WROTE {out_path} and projects/{out_path}", flush=True)


if __name__ == "__main__":
    main()
