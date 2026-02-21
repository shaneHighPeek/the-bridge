#!/usr/bin/env python3

import csv
import os
import re
import time
import urllib.parse
import urllib.request
from typing import Dict, List, Optional, Tuple

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"
AJAX_URL = "https://www.dentist.com.au/index.php/ajax/processing_module"


def http_get(url: str, timeout: int = 20, tries: int = 3) -> Optional[str]:
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.read().decode("utf-8", errors="ignore")
        except Exception:
            if i == tries - 1:
                return None
            time.sleep(0.4 * (i + 1))
    return None


def http_post_form(url: str, data: Dict[str, str], timeout: int = 20, tries: int = 3) -> Optional[str]:
    body = urllib.parse.urlencode(data).encode("utf-8")
    for i in range(tries):
        try:
            req = urllib.request.Request(
                url,
                data=body,
                headers={
                    "User-Agent": UA,
                    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                },
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.read().decode("utf-8", errors="ignore")
        except Exception:
            if i == tries - 1:
                return None
            time.sleep(0.4 * (i + 1))
    return None


def clean_text(s: str) -> str:
    s = re.sub(r"<[^>]+>", " ", s)
    s = s.replace("&amp;", "&").replace("&nbsp;", " ")
    s = re.sub(r"\s+", " ", s).strip()
    return s


def extract_suburb_links(html: str, state: str) -> List[str]:
    state = state.lower()
    links = set(re.findall(rf"https://www\.dentist\.com\.au/dentist/{state}/[a-z0-9-]+", html))
    rels = re.findall(rf"href=\"/dentist/{state}/([a-z0-9-]+)\"", html)
    for r in rels:
        links.add(f"https://www.dentist.com.au/dentist/{state}/{r}")
    return sorted(links)


def extract_address_query(html: str) -> Optional[str]:
    m = re.search(r'var address = "([^"]*)";', html)
    if m:
        q = m.group(1).strip()
        return q if q and q != ", ," and q != ", , " else None
    return None


def parse_total_pages(html: str) -> int:
    # handle both attribute orders
    m = re.search(r'<input[^>]*id="total_pages"[^>]*value="(\d+)"', html)
    if not m:
        m = re.search(r'<input[^>]*value="(\d+)"[^>]*id="total_pages"', html)
    if m:
        try:
            return int(m.group(1))
        except Exception:
            pass
    return 1


def extract_listings_from_html(html: str) -> List[Dict[str, str]]:
    out = []
    chunks = html.split('<div class="info-row">')[1:]
    for chunk in chunks:
        name_m = re.search(r'class="p_profile"[^>]*>(.*?)</a>', chunk, re.DOTALL)
        prof_m = re.search(r'class="p_profile"\s+href="([^"]+)"', chunk)
        id_m = re.search(r'class="p_profile"[^>]*\sdata="(A\d+)"', chunk)
        addr_m = re.search(r'<address>(.*?)</address>', chunk, re.DOTALL)
        phone_m = re.search(r'href="tel:([^"]+)"', chunk)

        if not name_m or not prof_m:
            continue

        name = clean_text(name_m.group(1))
        profile_url = prof_m.group(1).strip()
        if profile_url.startswith("/"):
            profile_url = "https://www.dentist.com.au" + profile_url

        rid = id_m.group(1) if id_m else None
        if not rid:
            id2 = re.search(r"/(A\d+)(?:\?|$)", profile_url)
            rid = id2.group(1) if id2 else ""

        address = clean_text(addr_m.group(1)) if addr_m else ""
        phone = clean_text(phone_m.group(1)) if phone_m else ""

        out.append(
            {
                "id": rid,
                "name": name,
                "address": address,
                "phone": phone,
                "profile_url": profile_url,
            }
        )
    return out


def extract_external_website(profile_html: str) -> str:
    m = re.search(r'loggerable-external-link"\s+data="([^"]+)"', profile_html)
    if not m:
        m = re.search(r'loggerable-external-link[^>]*\sdata="([^"]+)"', profile_html)
    if m:
        url = m.group(1).strip()
        return url
    return ""


def load_existing_any(target_file: str) -> Tuple[Dict[str, Dict[str, str]], set]:
    """Return records dict keyed by id_or_key and set of ids."""
    records = {}
    ids = set()
    if not os.path.exists(target_file):
        return records, ids

    with open(target_file, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = (row.get("Practice Name") or row.get("Name") or "").strip()
            address = (row.get("Address") or row.get("Full Address") or "").strip()
            phone = (row.get("Phone") or row.get("Phone Number") or "").strip()
            website = (row.get("Website") or row.get("Website URL") or "").strip()
            pid = (row.get("ID") or row.get("id") or "").strip()
            profile = (row.get("ProfileURL") or row.get("Profile URL") or "").strip()

            key = pid or (name.lower() + "|" + address.lower())
            if not key.strip("|"):
                continue
            records[key] = {
                "Practice Name": name,
                "Address": address,
                "Phone": phone,
                "Website": website or profile,
            }
            if pid:
                ids.add(pid)

    return records, ids


def seed_from_other_files(state: str, seed_files: List[str], existing_records: Dict[str, Dict[str, str]]) -> None:
    for fpath in seed_files:
        if not os.path.exists(fpath):
            continue
        with open(fpath, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                name = (row.get("Practice Name") or row.get("Name") or "").strip()
                address = (row.get("Address") or row.get("Full Address") or "").strip()
                phone = (row.get("Phone") or row.get("Phone Number") or "").strip()
                website = (row.get("Website") or row.get("Website URL") or "").strip()
                pid = (row.get("ID") or row.get("id") or "").strip()
                profile = (row.get("ProfileURL") or row.get("Profile URL") or row.get("Profile") or "").strip()

                key = pid or (name.lower() + "|" + address.lower())
                if not key.strip("|"):
                    continue
                if key not in existing_records:
                    existing_records[key] = {
                        "Practice Name": name,
                        "Address": address,
                        "Phone": phone,
                        "Website": website or profile,
                    }


def write_records(target_file: str, records: Dict[str, Dict[str, str]]) -> None:
    tmp = target_file + ".tmp"
    with open(tmp, "w", newline="", encoding="utf-8") as f:
        fieldnames = ["Practice Name", "Address", "Phone", "Website"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for _, row in records.items():
            writer.writerow({
                "Practice Name": row.get("Practice Name", ""),
                "Address": row.get("Address", ""),
                "Phone": row.get("Phone", ""),
                "Website": row.get("Website", ""),
            })
    os.replace(tmp, target_file)


def harvest_state(
    state: str,
    seed_urls: List[str],
    target_file: str,
    target_count: int = 305,
    max_listing_pages: int = 120,
    delay_s: float = 0.08,
) -> Tuple[int, int]:
    records, _ = load_existing_any(target_file)

    # seed from existing project files
    seed_from_other_files(
        state,
        seed_files=[
            f"Spectrum_Dental_{state}_Lead_List.csv",
            f"Spectrum_{state}_300.csv",
            f"Spectrum_Dental_{state}_Lead_List.csv".replace("_Lead_List", "_Lead_List"),
        ],
        existing_records=records,
    )

    visited = set()
    queue = list(seed_urls)
    listing_pages_processed = 0

    website_cache: Dict[str, str] = {}

    def upsert_listing(item: Dict[str, str]):
        pid = item.get("id", "").strip()
        name = item.get("name", "").strip()
        address = item.get("address", "").strip()
        phone = item.get("phone", "").strip()
        profile_url = item.get("profile_url", "").strip()

        key = pid or (name.lower() + "|" + address.lower())
        if not key.strip("|"):
            return

        if key in records:
            # fill missing fields
            if not records[key].get("Address") and address:
                records[key]["Address"] = address
            if not records[key].get("Phone") and phone:
                records[key]["Phone"] = phone
            if not records[key].get("Website") and profile_url:
                records[key]["Website"] = profile_url
            return

        # resolve website via profile
        website = ""
        if pid and pid in website_cache:
            website = website_cache[pid]
        else:
            prof_html = http_get(profile_url)
            if prof_html:
                website = extract_external_website(prof_html)
            if pid:
                website_cache[pid] = website
            time.sleep(delay_s)

        records[key] = {
            "Practice Name": name,
            "Address": address,
            "Phone": phone,
            "Website": website or profile_url,
        }

    while queue and len(records) < target_count and listing_pages_processed < max_listing_pages:
        url = queue.pop(0)
        if url in visited:
            continue
        visited.add(url)
        listing_pages_processed += 1

        html = http_get(url)
        if not html:
            continue

        # premium listings on the page
        for item in extract_listings_from_html(html):
            if len(records) >= target_count:
                break
            upsert_listing(item)

        # standard listings via AJAX
        address_q = extract_address_query(html)
        if address_q:
            # page 1 first
            resp1 = http_post_form(
                AJAX_URL,
                {
                    "module": "dsearch",
                    "cmd": "dentist:results:standard_list:search",
                    "current_page": "1",
                    "address": address_q,
                    "type": "",
                    "value": "",
                },
            )
            time.sleep(delay_s)
            if resp1:
                total_pages = parse_total_pages(resp1)
                pages = range(1, total_pages + 1)

                def process_std_page(resp_html: str):
                    for item in extract_listings_from_html(resp_html):
                        if len(records) >= target_count:
                            break
                        upsert_listing(item)

                process_std_page(resp1)

                for p in pages:
                    if p == 1 or len(records) >= target_count:
                        continue
                    resp = http_post_form(
                        AJAX_URL,
                        {
                            "module": "dsearch",
                            "cmd": "dentist:results:standard_list:search",
                            "current_page": str(p),
                            "address": address_q,
                            "type": "",
                            "value": "",
                        },
                    )
                    time.sleep(delay_s)
                    if resp:
                        process_std_page(resp)

        # add more suburb links to queue
        for s in extract_suburb_links(html, state):
            if s not in visited:
                queue.append(s)

        # periodic save
        if listing_pages_processed % 5 == 0:
            write_records(target_file, records)

    write_records(target_file, records)
    return len(records), listing_pages_processed


def main():
    targets = {
        "VIC": {
            "target_file": "Spectrum_VIC_300_leads.csv",
            "seeds": [
                "https://www.dentist.com.au/dentist/vic/melbourne",
                "https://www.dentist.com.au/dentist/vic/geelong",
                "https://www.dentist.com.au/dentist/vic/ballarat",
                "https://www.dentist.com.au/dentist/vic/bendigo",
                "https://www.dentist.com.au/dentist/vic/frankston",
                "https://www.dentist.com.au/dentist/vic/dandenong",
                "https://www.dentist.com.au/dentist/vic/mildura",
                "https://www.dentist.com.au/dentist/vic/shepparton",
                "https://www.dentist.com.au/dentist/vic/warrnambool",
                "https://www.dentist.com.au/dentist/vic/traralgon",
            ],
        },
        "NSW": {
            "target_file": "Spectrum_NSW_300_leads.csv",
            "seeds": [
                "https://www.dentist.com.au/dentist/nsw/sydney",
                "https://www.dentist.com.au/dentist/nsw/parramatta",
                "https://www.dentist.com.au/dentist/nsw/liverpool",
                "https://www.dentist.com.au/dentist/nsw/penrith",
                "https://www.dentist.com.au/dentist/nsw/newcastle",
                "https://www.dentist.com.au/dentist/nsw/wollongong",
                "https://www.dentist.com.au/dentist/nsw/gosford",
                "https://www.dentist.com.au/dentist/nsw/bathurst",
                "https://www.dentist.com.au/dentist/nsw/wagga-wagga",
                "https://www.dentist.com.au/dentist/nsw/albury",
                "https://www.dentist.com.au/dentist/nsw/dubbo",
            ],
        },
        "QLD": {
            "target_file": "Spectrum_QLD_300_leads.csv",
            "seeds": [
                "https://www.dentist.com.au/dentist/qld/brisbane",
                "https://www.dentist.com.au/dentist/qld/toowoomba",
                "https://www.dentist.com.au/dentist/qld/cairns",
                "https://www.dentist.com.au/dentist/qld/townsville",
                "https://www.dentist.com.au/dentist/qld/ipswich",
                "https://www.dentist.com.au/dentist/qld/mackay",
                "https://www.dentist.com.au/dentist/qld/rockhampton",
                "https://www.dentist.com.au/dentist/qld/sunshine-coast",
                "https://www.dentist.com.au/dentist/qld/bundaberg",
                "https://www.dentist.com.au/dentist/qld/hervey-bay",
            ],
        },
    }

    for state, cfg in targets.items():
        count, pages = harvest_state(state, cfg["seeds"], cfg["target_file"], target_count=305)
        print(f"{state}: {count} records (listing pages processed: {pages}) -> {cfg['target_file']}")


if __name__ == "__main__":
    main()
