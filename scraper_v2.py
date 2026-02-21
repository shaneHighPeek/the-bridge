
import urllib.request
import re
import csv
import time
import json
import os
import html

def fetch_url(url, post_data=None):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded' if post_data else None
    }
    try:
        if post_data:
            data = urllib.parse.urlencode(post_data).encode('utf-8')
            req = urllib.request.Request(url, data=data, headers={k: v for k, v in headers.items() if v})
        else:
            req = urllib.request.Request(url, headers=headers)
        
        with urllib.request.urlopen(req, timeout=20) as response:
            return response.read().decode('utf-8', errors='ignore')
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

def parse_map_data(page_html):
    # Find mapData = JSON.parse("...")
    match = re.search(r'mapData = JSON\.parse\("(.*?)"\);', page_html, re.S)
    if not match: return []
    
    json_str = match.group(1).replace('\\"', '"').replace('\\/', '/')
    # Handle the escaped double quotes and other chars
    try:
        # The JSON in the HTML is double-escaped or has specific format
        # Let's try to fix common issues
        json_str = json_str.encode('utf-8').decode('unicode_escape')
        data = json.loads(json_str)
        markers = data.get('markers', [])
        results = []
        for m in markers:
            title = m.get('title', '')
            html_content = m.get('html', '')
            # html_content: <strong><a href='(URL)' target='_blank'>(NAME)</a></strong><br/>(ADDRESS)
            url_match = re.search(r"href='([^']+)'", html_content)
            addr_match = re.search(r"<br/>(.*)", html_content)
            
            results.append({
                'Name': html.unescape(title),
                'DetailURL': url_match.group(1) if url_match else "",
                'Address': html.unescape(addr_match.group(1).strip()) if addr_match else ""
            })
        return results
    except Exception as e:
        print(f"Error parsing map data: {e}")
        return []

def extract_premium_dentists(page_html):
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
    if not page_html: return None, None
    
    # Phone: tel:(...)
    phone_match = re.search(r'href="tel:([^"]+)"', page_html)
    phone = phone_match.group(1).strip() if phone_match else ""
    
    # Website: class="...loggerable-external-link..." data="..."
    website_match = re.search(r'class="[^"]*loggerable-external-link[^"]*" data="([^"]+)"', page_html)
    website = website_match.group(1) if website_match else ""
    
    return phone, website

def scrape_region(state, region_name, region_url):
    print(f"Processing region: {region_name}")
    all_dentists = {}
    
    html_content = fetch_url(region_url)
    if not html_content: return {}, []
    
    # 1. Get Premium dentists (already have phone/website)
    premium = extract_premium_dentists(html_content)
    for d in premium:
        key = (d['Name'], d['Address'][:20]) # Key by name and start of address
        all_dentists[key] = d
        
    # 2. Get all dentists from Map Data
    all_from_map = parse_map_data(html_content)
    for d in all_from_map:
        key = (d['Name'], d['Address'][:20])
        if key not in all_dentists:
            all_dentists[key] = {
                'Name': d['Name'],
                'Address': d['Address'],
                'Phone': "",
                'Website': "",
                'DetailURL': d['DetailURL']
            }
            
    # 3. Get Suburbs for future use (if we wanted to crawl deeper)
    suburbs = re.findall(rf'https://www.dentist.com.au/dentist/{state}/[a-z0-9-]+', html_content)
    
    return all_dentists, suburbs

def harvest(state, start_hubs):
    results = {}
    visited_urls = set()
    queue = start_hubs
    
    hub_count = 0
    while queue and hub_count < 20: # Limit number of major hubs/suburbs to process
        hub_name, hub_url = queue.pop(0)
        if hub_url in visited_urls: continue
        visited_urls.add(hub_url)
        
        hub_dentists, new_suburbs = scrape_region(state, hub_name, hub_url)
        for key, data in hub_dentists.items():
            if key not in results:
                results[key] = data
        
        # Add discovered suburbs to queue if they look like the same state
        for s in new_suburbs:
            if s not in visited_urls:
                # queue.append((s.split('/')[-1], s)) # Disabled for speed, using fixed hubs
                pass
        
        hub_count += 1
        time.sleep(1)

    # Final Pass: Fetch missing phones/websites for a sample or all
    print(f"Total dentists found in {state}: {len(results)}. Fetching missing details...")
    final_list = []
    detail_fetches = 0
    for i, (key, d) in enumerate(results.items()):
        if not d['Phone'] and detail_fetches < 300: # Limit detail fetches to avoid getting blocked
            print(f"Fetching details for {d['Name']}...")
            phone, website = get_details(d['DetailURL'])
            d['Phone'] = phone
            d['Website'] = website
            detail_fetches += 1
            time.sleep(0.5)
        
        final_list.append({
            'Practice Name': d['Name'],
            'Phone Number': d['Phone'],
            'Full Address': d['Address'],
            'Website URL': d['Website']
        })
        if i % 50 == 0: print(f"Processed {i}/{len(results)}")
        
    return final_list

# Main Hubs
nsw_hubs = [
    ('Sydney', 'https://www.dentist.com.au/dentist/nsw/sydney'),
    ('Newcastle', 'https://www.dentist.com.au/dentist/nsw/newcastle'),
    ('Wollongong', 'https://www.dentist.com.au/dentist/nsw/wollongong'),
    ('Parramatta', 'https://www.dentist.com.au/dentist/nsw/parramatta'),
    ('Gosford', 'https://www.dentist.com.au/dentist/nsw/gosford'),
    ('Penrith', 'https://www.dentist.com.au/dentist/nsw/penrith'),
    ('Albury', 'https://www.dentist.com.au/dentist/nsw/albury'),
    ('Wagga Wagga', 'https://www.dentist.com.au/dentist/nsw/wagga-wagga'),
    ('Coffs Harbour', 'https://www.dentist.com.au/dentist/nsw/coffs-harbour')
]

qld_hubs = [
    ('Brisbane', 'https://www.dentist.com.au/dentist/qld/brisbane'),
    ('Gold Coast', 'https://www.dentist.com.au/dentist/qld/gold-coast'),
    ('Sunshine Coast', 'https://www.dentist.com.au/dentist/qld/sunshine-coast'),
    ('Townsville', 'https://www.dentist.com.au/dentist/qld/townsville'),
    ('Cairns', 'https://www.dentist.com.au/dentist/qld/cairns'),
    ('Toowoomba', 'https://www.dentist.com.au/dentist/qld/toowoomba'),
    ('Mackay', 'https://www.dentist.com.au/dentist/qld/mackay'),
    ('Rockhampton', 'https://www.dentist.com.au/dentist/qld/rockhampton'),
    ('Bundaberg', 'https://www.dentist.com.au/dentist/qld/bundaberg')
]

nsw_leads = harvest('nsw', nsw_hubs)
with open('Spectrum_Dental_NSW_Lead_List.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['Practice Name', 'Phone Number', 'Full Address', 'Website URL'])
    writer.writeheader()
    writer.writerows(nsw_leads)

qld_leads = harvest('qld', qld_hubs)
with open('Spectrum_Dental_QLD_Lead_List.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['Practice Name', 'Phone Number', 'Full Address', 'Website URL'])
    writer.writeheader()
    writer.writerows(qld_leads)

print("Harvest complete.")
