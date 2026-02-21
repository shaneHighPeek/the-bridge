import csv
import re
import sys
import time
import urllib.parse
import urllib.request
from collections import deque
from html import unescape

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
AJAX_URL = "https://www.dentist.com.au/index.php/ajax/processing_module"
STD_CMD = "dentist:results:standard_list:search"


def fetch(url: str, *, referer: str | None = None, timeout: int = 30) -> str:
    headers = {"User-Agent": UA, "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"}
    if referer:
        headers["Referer"] = referer
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        data = resp.read()
    return data.decode("utf-8", errors="ignore")


def post_ajax(*, referer: str, address: str, page: int, timeout: int = 30) -> str:
    payload = {
        "module": "dsearch",
        "cmd": STD_CMD,
        "current_page": str(page),
        "address": address,
        "type": "",
        "value": "",
    }
    data = urllib.parse.urlencode(payload).encode("utf-8")
    headers = {
        "User-Agent": UA,
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "*/*",
        "Referer": referer,
    }
    req = urllib.request.Request(AJAX_URL, data=data, headers=headers)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        body = resp.read()
    return body.decode("utf-8", errors="ignore")


def strip_tags(html: str) -> str:
    # very small + safe tag stripper
    html = re.sub(r"<br\s*/?>", " ", html, flags=re.I)
    html = re.sub(r"<[^>]+>", " ", html)
    html = unescape(html)
    html = re.sub(r"\s+", " ", html).strip()
    return html


def norm_phone(phone: str) -> str:
    digits = re.sub(r"\D+", "", phone or "")
    # Keep last 10-11 digits where possible; AU landlines show as 0396544455 etc
    return digits


def norm_text(s: str) -> str:
    s = (s or "").lower().strip()
    s = re.sub(r"\s+", " ", s)
    s = re.sub(r"[^a-z0-9 ]+", "", s)
    return s


def make_key(name: str, phone: str, address: str) -> str:
    p = norm_phone(phone)
    if p:
        return f"p:{p}"
    return f"na:{norm_text(name)}|{norm_text(address)}"


def extract_address_var(base_html: str) -> str | None:
    # var address = "Melbourne, VIC, 3000";
    m = re.search(r'var\s+address\s*=\s*"([^"]+)"\s*;', base_html)
    if m:
        return m.group(1).strip()
    return None


def extract_suburb_urls(html: str, state: str) -> list[str]:
    # https://www.dentist.com.au/dentist/vic/abbotsford
    pat = rf"https://www\.dentist\.com\.au/dentist/{re.escape(state)}/[a-z0-9-]+"
    return list(dict.fromkeys(re.findall(pat, html)))


def extract_listings(html: str) -> list[dict]:
    out = []
    blocks = re.split(r'<div class="info-row">', html)
    for block in blocks[1:]:
        name_match = re.search(r'<h3><a[^>]+href="([^"]+)"[^>]*>([^<]+)</a>', block)
        if not name_match:
            continue
        detail_url = name_match.group(1).strip()
        name = strip_tags(name_match.group(2))

        address_match = re.search(r'<address>(.*?)</address>', block, re.S | re.I)
        address = strip_tags(address_match.group(1)) if address_match else ""

        phone_match = re.search(r'href="tel:([^"]+)"', block, re.I)
        phone = strip_tags(phone_match.group(1)) if phone_match else ""

        # In many standard listings, external website isn't present; use detail page as fallback
        website = detail_url

        if name and address:
            out.append({
                "Practice Name": name,
                "Phone": phone,
                "Address": address,
                "Website": website,
            })
    return out


def extract_total_pages(html: str) -> int:
    # input type="hidden" value="5" id="total_pages"
    m = re.search(r'id="total_pages"[^>]*value="(\d+)"', html)
    if not m:
        m = re.search(r'value="(\d+)"[^>]*id="total_pages"', html)
    if m:
        try:
            return int(m.group(1))
        except Exception:
            return 1
    return 1


def scrape_state(state: str, seed_urls: list[str], target: int, *, max_suburbs: int = 120, max_pages_per_suburb: int = 1, delay_s: float = 0.2) -> list[dict]:
    seen_keys: set[str] = set()
    results: list[dict] = []

    q = deque(seed_urls)
    visited: set[str] = set()

    while q and len(results) < target and len(visited) < max_suburbs:
        url = q.popleft()
        if url in visited:
            continue
        visited.add(url)

        print(f"[{state.upper()}] suburb {len(visited)}/{max_suburbs}: {url} (leads={len(results)})", file=sys.stderr)

        try:
            base = fetch(url)
        except Exception as e:
            print(f"WARN fetch failed: {url}: {e}", file=sys.stderr)
            continue

        # discover more suburb urls
        for s in extract_suburb_urls(base, state):
            if s not in visited:
                q.append(s)

        # premium listings from base
        for item in extract_listings(base):
            k = make_key(item["Practice Name"], item["Phone"], item["Address"])
            if k not in seen_keys:
                seen_keys.add(k)
                results.append(item)
                if len(results) >= target:
                    break

        if len(results) >= target:
            break

        addr = extract_address_var(base)
        if not addr:
            # Some pages may not have a standard list
            continue

        # standard listings via AJAX
        try:
            ajax1 = post_ajax(referer=url, address=addr, page=1)
        except Exception as e:
            print(f"WARN ajax failed: {url}: {e}", file=sys.stderr)
            continue

        total_pages = extract_total_pages(ajax1)
        pages_to_get = min(max_pages_per_suburb, max(1, total_pages))

        for page in range(1, pages_to_get + 1):
            ajax_html = ajax1 if page == 1 else post_ajax(referer=url, address=addr, page=page)
            for item in extract_listings(ajax_html):
                k = make_key(item["Practice Name"], item["Phone"], item["Address"])
                if k not in seen_keys:
                    seen_keys.add(k)
                    results.append(item)
                    if len(results) >= target:
                        break
            if len(results) >= target:
                break
            time.sleep(delay_s)

        time.sleep(delay_s)

    return results


def write_csv(path: str, rows: list[dict]):
    if not rows:
        raise ValueError("No rows")
    cols = ["Practice Name", "Phone", "Address", "Website"]
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for r in rows:
            w.writerow({c: r.get(c, "") for c in cols})


def main():
    # NOTE: seeds chosen to match requested hubs.
    targets = {
        "vic": {
            "target": 330,
            "seeds": [
                "https://www.dentist.com.au/dentist/vic/melbourne",
                "https://www.dentist.com.au/dentist/vic/geelong",
                "https://www.dentist.com.au/dentist/vic/ballarat",
                "https://www.dentist.com.au/dentist/vic/bendigo",
                "https://www.dentist.com.au/dentist/vic/mornington",
            ],
        },
        "nsw": {
            "target": 330,
            "seeds": [
                "https://www.dentist.com.au/dentist/nsw/sydney",
                "https://www.dentist.com.au/dentist/nsw/newcastle",
                "https://www.dentist.com.au/dentist/nsw/wollongong",
                "https://www.dentist.com.au/dentist/nsw/gosford",
                "https://www.dentist.com.au/dentist/nsw/coffs-harbour",
                "https://www.dentist.com.au/dentist/nsw/albury",
            ],
        },
        "qld": {
            "target": 330,
            "seeds": [
                "https://www.dentist.com.au/dentist/qld/brisbane",
                "https://www.dentist.com.au/dentist/qld/southport",
                "https://www.dentist.com.au/dentist/qld/maroochydore",
                "https://www.dentist.com.au/dentist/qld/toowoomba",
                "https://www.dentist.com.au/dentist/qld/townsville",
                "https://www.dentist.com.au/dentist/qld/cairns",
            ],
        },
    }

    for state, cfg in targets.items():
        target = int(cfg["target"])
        seeds = cfg["seeds"]
        print(f"Scraping {state.upper()}... target={target}", file=sys.stderr)
        rows = scrape_state(state, seeds, target, max_suburbs=90, max_pages_per_suburb=1, delay_s=0.15)
        print(f"{state.upper()} scraped: {len(rows)}", file=sys.stderr)
        out_path = {
            "vic": "Spectrum_VIC_300.csv",
            "nsw": "Spectrum_NSW_300.csv",
            "qld": "Spectrum_QLD_300.csv",
        }[state]
        # Trim to 300 exact (while still being >=300 scraped)
        if len(rows) < 300:
            print(f"ERROR: {state.upper()} only {len(rows)} rows (<300)", file=sys.stderr)
        write_csv(out_path, rows[:300])
        print(f"WROTE {out_path} ({min(300, len(rows))} rows)", file=sys.stderr)


if __name__ == "__main__":
    main()
