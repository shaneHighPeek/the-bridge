
import subprocess
import re
import csv
import time
import json
import os
import html

def fetch_url(url, post_data=None):
    cmd = ['curl', '-s', '-L', '-A', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36']
    if post_data:
        for k, v in post_data.items():
            cmd.extend(['-d', f'{k}={v}'])
    cmd.append(url)
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        return result.stdout
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

def parse_map_data(page_html):
    if not page_html: return []
    match = re.search(r'mapData = JSON\.parse\("(.*?)"\);', page_html, re.S)
    if not match: return []
    
    json_str = match.group(1).replace('\\"', '"').replace('\\/', '/')
    try:
        # Decode the escaped string
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

def harvest(state, start_hubs):
    results = {}
    visited_urls = set()
    
    for hub_name, hub_url in start_hubs:
        if hub_url in visited_urls: continue
        visited_urls.add(hub_url)
        print(f"Scraping {state.upper()} - {hub_name}...")
        
        html_content = fetch_url(hub_url)
        if not html_content: continue
        
        # Premium
        premium = extract_premium_dentists(html_content)
        for d in premium:
            key = (d['Name'], d['Address'][:20])
            results[key] = d
            
        # All from Map
        all_from_map = parse_map_data(html_content)
        for d in all_from_map:
            key = (d['Name'], d['Address'][:20])
            if key not in results:
                results[key] = {
                    'Name': d['Name'], 'Address': d['Address'],
                    'Phone': "", 'Website': "", 'DetailURL': d['DetailURL']
                }
        
        # Suburbs
        sub_links = re.findall(rf'https://www.dentist.com.au/dentist/{state}/[a-z0-9-]+', html_content)
        for sl in sub_links[:5]: # Add a few suburbs from each hub to broaden
            if sl not in visited_urls and len(visited_urls) < 30:
                visited_urls.add(sl)
                # We'll just fetch these too
                h_content = fetch_url(sl)
                if h_content:
                    for d in extract_premium_dentists(h_content) + [{'Name': m['Name'], 'Address': m['Address'], 'Phone': "", 'Website': "", 'DetailURL': m['DetailURL']} for m in parse_map_data(h_content)]:
                        k = (d['Name'], d['Address'][:20])
                        if k not in results: results[k] = d
        
        time.sleep(1)

    print(f"Total {state.upper()} dentists: {len(results)}. Fetching details for first 150...")
    final_list = []
    detail_fetches = 0
    for i, (key, d) in enumerate(results.items()):
        if not d['Phone'] and detail_fetches < 150:
            p, w = get_details(d['DetailURL'])
            d['Phone'] = p
            d['Website'] = w
            detail_fetches += 1
            if detail_fetches % 10 == 0: print(f"Fetched {detail_fetches} details...")
            time.sleep(0.5)
        
        final_list.append({
            'Practice Name': d['Name'],
            'Phone Number': d['Phone'],
            'Full Address': d['Address'],
            'Website URL': d['Website']
        })
    return final_list

def save(data, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=['Practice Name', 'Phone Number', 'Full Address', 'Website URL'])
        w.writeheader()
        w.writerows(data)
    print(f"Saved {len(data)} to {filename}")

nsw_hubs = [('Sydney', 'https://www.dentist.com.au/dentist/nsw/sydney'), ('Newcastle', 'https://www.dentist.com.au/dentist/nsw/newcastle'), ('Wollongong', 'https://www.dentist.com.au/dentist/nsw/wollongong')]
qld_hubs = [('Brisbane', 'https://www.dentist.com.au/dentist/qld/brisbane'), ('Gold Coast', 'https://www.dentist.com.au/dentist/qld/gold-coast'), ('Townsville', 'https://www.dentist.com.au/dentist/qld/townsville')]

save(harvest('nsw', nsw_hubs), 'Spectrum_Dental_NSW_Lead_List.csv')
save(harvest('qld', qld_hubs), 'Spectrum_Dental_QLD_Lead_List.csv')
