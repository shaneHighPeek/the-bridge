
import subprocess
import re
import csv
import time
import json
import os
import html

def fetch_url(url, post_data=None):
    # Using -k to ignore SSL cert issues if they arise and -L to follow redirects
    cmd = ['curl', '-s', '-L', '-k', '-A', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36']
    if post_data:
        for k, v in post_data.items():
            cmd.extend(['-d', f'{k}={v}'])
    cmd.append(url)
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        return result.stdout
    except Exception as e:
        print(f"Error fetching {url}: {e}", flush=True)
        return None

def parse_map_data(page_html):
    if not page_html: return []
    match = re.search(r'mapData = JSON\.parse\("(.*?)"\);', page_html, re.S)
    if not match: return []
    
    json_str = match.group(1).replace('\\"', '"').replace('\\/', '/')
    try:
        json_str = json_str.encode('utf-8').decode('unicode_escape')
        data = json.loads(json_str)
        markers = data.get('markers', [])
        results = []
        for m in markers:
            title = m.get('title', '')
            html_content = m.get('html', '')
            url_match = re.search(r"href='([^']+)'", html_content)
            addr_match = re.search(r"<br/>(.*)", html_content)
            
            results.append({
                'Name': html.unescape(title),
                'DetailURL': url_match.group(1) if url_match else "",
                'Address': html.unescape(addr_match.group(1).strip()) if addr_match else ""
            })
        return results
    except Exception as e:
        return []

def extract_premium_dentists(page_html):
    if not page_html: return []
    dentists = []
    blocks = re.split(r'<div class="info-row">', page_html)
    for block in blocks[1:]:
        name_match = re.search(r'<h3><a[^>]+href="([^"]+)"[^>]*>([^<]+)</a>', block)
        if name_match:
            detail_url = name_match.group(1)
            name = html.unescape(name_match.group(2).strip())
            address_match = re.search(r'<address>(.*?)</address>', block, re.S)
            address = html.unescape(address_match.group(1).strip()) if address_match else ""
            phone_match = re.search(r'href="tel:([^"]+)"', block)
            phone = phone_match.group(1).strip() if phone_match else ""
            website_match = re.search(r'class="[^"]*loggerable-external-link[^"]*" data="([^"]+)"', block)
            website = website_match.group(1) if website_match else ""
            
            dentists.append({
                'Name': name,
                'Address': address,
                'Phone': phone,
                'Website': website,
                'DetailURL': detail_url
            })
    return dentists

def get_details(detail_url):
    page_html = fetch_url(detail_url)
    if not page_html: return "", ""
    phone_match = re.search(r'href="tel:([^"]+)"', page_html)
    phone = phone_match.group(1).strip() if phone_match else ""
    website_match = re.search(r'class="[^"]*loggerable-external-link[^"]*" data="([^"]+)"', page_html)
    website = website_match.group(1) if website_match else ""
    return phone, website

def harvest_state(state, hubs, target_count=300):
    results = {}
    visited_urls = set()
    queue = [h[1] for h in hubs]
    
    print(f"--- Starting harvest for {state.upper()} (Target: {target_count}) ---", flush=True)
    
    while queue and len(results) < target_count * 1.2: # Get extra for filtering
        url = queue.pop(0)
        if url in visited_urls: continue
        visited_urls.add(url)
        
        print(f"Scraping: {url}...", flush=True)
        html_content = fetch_url(url)
        if not html_content: continue
        
        # 1. Premium
        for d in extract_premium_dentists(html_content):
            key = (d['Name'], d['Address'][:30])
            results[key] = d
            
        # 2. Map Data
        for d in parse_map_data(html_content):
            key = (d['Name'], d['Address'][:30])
            if key not in results:
                results[key] = {
                    'Name': d['Name'], 'Address': d['Address'],
                    'Phone': "", 'Website': "", 'DetailURL': d['DetailURL']
                }
        
        # 3. Discover more suburbs if needed
        if len(results) < target_count:
            sub_links = re.findall(rf'https://www.dentist.com.au/dentist/{state}/[a-z0-9-]+', html_content)
            for sl in sub_links:
                if sl not in visited_urls and sl not in queue:
                    queue.append(sl)
        
        print(f"Current count for {state.upper()}: {len(results)}", flush=True)
        time.sleep(1)
        if len(visited_urls) > 50: break # Safety break

    # Detail enrichment
    final_list = []
    print(f"Enriching {state.upper()} leads...", flush=True)
    fetch_count = 0
    for key, d in results.items():
        if len(final_list) >= target_count: break
        
        if not d['Phone']:
            p, w = get_details(d['DetailURL'])
            d['Phone'] = p
            d['Website'] = w
            fetch_count += 1
            if fetch_count % 10 == 0: print(f"Enriched {fetch_count} items...", flush=True)
            time.sleep(0.5)
            
        final_list.append({
            'Practice Name': d['Name'],
            'Phone Number': d['Phone'],
            'Full Address': d['Address'],
            'Website URL': d['Website']
        })
        
    return final_list

def save_leads(data, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=['Practice Name', 'Phone Number', 'Full Address', 'Website URL'])
        w.writeheader()
        w.writerows(data)
    print(f"Successfully saved {len(data)} leads to {filename}", flush=True)

# Main Configuration
nsw_hubs = [
    ('Sydney', 'https://www.dentist.com.au/dentist/nsw/sydney'),
    ('Newcastle', 'https://www.dentist.com.au/dentist/nsw/newcastle'),
    ('Wollongong', 'https://www.dentist.com.au/dentist/nsw/wollongong'),
    ('Gosford', 'https://www.dentist.com.au/dentist/nsw/gosford'),
    ('Wagga Wagga', 'https://www.dentist.com.au/dentist/nsw/wagga-wagga')
]

qld_hubs = [
    ('Brisbane', 'https://www.dentist.com.au/dentist/qld/brisbane'),
    ('Gold Coast', 'https://www.dentist.com.au/dentist/qld/gold-coast'),
    ('Sunshine Coast', 'https://www.dentist.com.au/dentist/qld/sunshine-coast'),
    ('Townsville', 'https://www.dentist.com.au/dentist/qld/townsville'),
    ('Cairns', 'https://www.dentist.com.au/dentist/qld/cairns')
]

nsw_data = harvest_state('nsw', nsw_hubs, 300)
save_leads(nsw_data, 'Spectrum_Dental_NSW_Lead_List.csv')

qld_data = harvest_state('qld', qld_hubs, 300)
save_leads(qld_data, 'Spectrum_Dental_QLD_Lead_List.csv')

print("ALL TASKS COMPLETE.", flush=True)
