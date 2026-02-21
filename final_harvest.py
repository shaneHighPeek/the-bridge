import csv
import re
import sys
import time
import urllib.parse
import urllib.request
import random
from collections import deque
from html import unescape
import os
import subprocess
import json
import html as htmlmod

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
AJAX_URL = "https://www.dentist.com.au/index.php/ajax/processing_module"
STD_CMD = "dentist:results:standard_list:search"

def fetch(url: str, *, referer: str | None = None, timeout: int = 40) -> str:
    cmd = ["curl", "-s", "-L", "--compressed", "-A", UA]
    if referer: cmd.extend(["-H", f"Referer: {referer}"])
    cmd.append(url)
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return res.stdout or ""
    except: return ""

def post_ajax(*, referer: str, address: str, page: int, timeout: int = 40) -> str:
    cmd = ["curl", "-s", "-L", "--compressed", "-A", UA, "-X", "POST"]
    cmd.extend(["-H", f"Referer: {referer}"])
    data = f"module=dsearch&cmd={STD_CMD}&current_page={page}&address={address}&type=&value="
    cmd.extend(["-d", data])
    cmd.append(AJAX_URL)
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return res.stdout or ""
    except: return ""

def strip_tags(html: str) -> str:
    html = re.sub(r"<br\s*/?>", " ", html, flags=re.I)
    html = re.sub(r"<[^>]+>", " ", html)
    html = unescape(html)
    html = re.sub(r"\s+", " ", html).strip()
    return html

def norm_phone(phone: str) -> str:
    return re.sub(r"\D+", "", phone or "")

def norm_text(s: str) -> str:
    s = (s or "").lower().strip()
    s = re.sub(r"\s+", " ", s)
    s = re.sub(r"[^a-z0-9 ]+", "", s)
    return s

def make_key(name: str, phone: str, address: str) -> str:
    p = norm_phone(phone)
    if p: return f"p:{p}"
    return f"na:{norm_text(name)}|{norm_text(address)}"

def extract_address_var(base_html: str) -> str | None:
    m = re.search(r'var\s+address\s*=\s*"([^"]+)"\s*;', base_html)
    if m: return m.group(1).strip()
    return None

def extract_suburb_urls(html: str, state: str) -> list[str]:
    pat = rf"https://www\.dentist\.com\.au/dentist/{re.escape(state)}/[a-z0-9-]+"
    return list(dict.fromkeys(re.findall(pat, html)))

def extract_listings(html: str) -> list[dict]:
    out = []
    blocks = re.split(r'<div class="info-row[^"]*">', html)
    for block in blocks[1:]:
        name_match = re.search(r'<h3><a[^>]+href="([^"]+)"[^>]*>([^<]+)</a>', block)
        if not name_match: continue
        detail_url = name_match.group(1).strip()
        name = strip_tags(name_match.group(2))
        address_match = re.search(r'<address>(.*?)</address>', block, re.S | re.I)
        address = strip_tags(address_match.group(1)) if address_match else ""
        phone_match = re.search(r'href="tel:([^"]+)"', block, re.I)
        phone = strip_tags(phone_match.group(1)) if phone_match else ""
        if name and address:
            out.append({"Practice Name": name, "Phone": phone, "Address": address, "detail_url": detail_url, "Website": ""})
    return out

def parse_map_markers(page_html: str) -> list[dict]:
    if not page_html: return []
    m = re.search(r"mapData\s*=\s*JSON\.parse\(\"(.*?)\"\);", page_html, re.S)
    if not m: return []
    raw = m.group(1).replace("\\/", "/").replace("\\\"", '"')
    try: data = json.loads(raw)
    except:
        try: data = json.loads(raw.encode("utf-8").decode("unicode_escape"))
        except: return []
    markers = data.get("markers", [])
    out = []
    for mk in markers:
        title = htmlmod.unescape(mk.get("title", "") or "")
        html_content = mk.get("html", "") or ""
        url_match = re.search(r"href='([^']+)'", html_content)
        addr_match = re.search(r"<br/>(.*)", html_content)
        detail_url = url_match.group(1) if url_match else ""
        address = strip_tags(addr_match.group(1)) if addr_match else ""
        if not detail_url: continue
        out.append({"Practice Name": title, "Address": address, "Phone": "", "detail_url": detail_url, "Website": ""})
    return out

def extract_total_pages(html: str) -> int:
    m = re.search(r'id="total_pages"[^>]*value="(\d+)"', html)
    if not m: m = re.search(r'value="(\d+)"[^>]*id="total_pages"', html)
    return int(m.group(1)) if m else 1

def enrich_website(detail_url: str) -> tuple[str, str]:
    try:
        html = fetch(detail_url)
        phone_match = re.search(r'href="tel:([^"]+)"', html)
        phone = strip_tags(phone_match.group(1)) if phone_match else ""
        website = ""
        m = re.search(r'data="([^"]+)"[^>]*>WEBSITE', html)
        if m: website = unescape(m.group(1).strip())
        else:
            for mm in re.finditer(r'data="([^"]+)"', html):
                cand = unescape(mm.group(1).strip())
                if cand.startswith("http") and not any(b in cand for b in ["centaurportal.com", "dentist.com.au", "googletagmanager", "google.com"]):
                    website = cand; break
        return phone, website
    except: return "", ""

def scrape_state(state: str, seed_urls: list[str], target: int) -> list[dict]:
    seen_keys: set[str] = set()
    leads: list[dict] = []
    q = deque(seed_urls)
    visited: set[str] = set()
    while q and len(leads) < target + 50:
        url = q.popleft(); 
        if url in visited: continue
        visited.add(url)
        print(f"[{state.upper()}] Suburb {len(visited)}: {url} (found={len(leads)})", flush=True)
        base = fetch(url)
        if not base: continue
        for s in extract_suburb_urls(base, state):
            if s not in visited: q.append(s)
        for item in extract_listings(base) + parse_map_markers(base):
            k = make_key(item["Practice Name"], item["Phone"], item["Address"])
            if k not in seen_keys:
                seen_keys.add(k); leads.append(item)
        addr = extract_address_var(base)
        if addr:
            ajax1 = post_ajax(referer=url, address=addr, page=1)
            markers = parse_map_markers(ajax1)
            print(f"DEBUG: Found {len(markers)} markers in AJAX page 1", flush=True)
            for item in markers:
                k = make_key(item["Practice Name"], item["Phone"], item["Address"])
                if k not in seen_keys:
                    seen_keys.add(k); leads.append(item)
            total_pages = extract_total_pages(ajax1)
            for page in range(2, total_pages + 1):
                ajax_html = post_ajax(referer=url, address=addr, page=page)
                for item in parse_map_markers(ajax_html):
                    k = make_key(item["Practice Name"], item["Phone"], item["Address"])
                    if k not in seen_keys:
                        seen_keys.add(k); leads.append(item)
                if len(leads) >= target + 50: break
                time.sleep(0.1)
        time.sleep(0.2)
    
    print(f"[{state.upper()}] Found {len(leads)} leads. Enriching first {target}...", flush=True)
    final = []
    for i, item in enumerate(leads[:target]):
        phone, website = enrich_website(item["detail_url"])
        final.append({"Practice Name": item["Practice Name"], "Address": item["Address"], "Phone": phone or item["Phone"], "Website": website})
        if (i+1) % 25 == 0: print(f"[{state.upper()}] Enriched {i+1}/{target}", flush=True)
    return final

def write_csv(path: str, rows: list[dict]):
    cols = ["Practice Name", "Address", "Phone", "Website"]
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)

def main():
    targets = {
        "vic": ["https://www.dentist.com.au/dentist/vic/melbourne", "https://www.dentist.com.au/dentist/vic/geelong", "https://www.dentist.com.au/dentist/vic/ballarat"],
        "nsw": ["https://www.dentist.com.au/dentist/nsw/sydney", "https://www.dentist.com.au/dentist/nsw/parramatta", "https://www.dentist.com.au/dentist/nsw/newcastle"],
        "qld": ["https://www.dentist.com.au/dentist/qld/brisbane", "https://www.dentist.com.au/dentist/qld/gold-coast", "https://www.dentist.com.au/dentist/qld/sunshine-coast"]
    }
    if not os.path.exists("projects"): os.makedirs("projects")
    for state, seeds in targets.items():
        rows = scrape_state(state, seeds, 300)
        fname = f"Spectrum_{state.upper()}_300.csv"
        write_csv(fname, rows)
        write_csv(os.path.join("projects", fname), rows)
        print(f"WROTE {fname} and projects/{fname} ({len(rows)} rows)", flush=True)

if __name__ == "__main__":
    main()
