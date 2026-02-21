
import urllib.request
import re
import csv
import time
import json
import os

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
        
        with urllib.request.urlopen(req, timeout=15) as response:
            return response.read().decode('utf-8', errors='ignore')
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

def extract_suburbs(html, state):
    # Pattern: https://www.dentist.com.au/dentist/[state]/[suburb-slug]
    pattern = rf'https://www.dentist.com.au/dentist/{state}/[a-z0-9-]+'
    return re.findall(pattern, html)

def extract_dentists(html):
    dentists = []
    # Premium listings pattern
    # <h3><a class="p_profile" href="(DETAIL_URL)" ...>(NAME)</a><span>(LABEL)</span></h3>
    # <address>(ADDRESS)</address>
    # <a class="callus-btn" ... href="tel:(PHONE)">
    
    # We'll use a more flexible regex to find the blocks
    blocks = re.split(r'<div class="info-row">', html)
    for block in blocks[1:]: # Skip first part
        name_match = re.search(r'<h3><a[^>]+href="([^"]+)"[^>]*>([^<]+)</a>', block)
        address_match = re.search(r'<address>(.*?)</address>', block, re.S)
        phone_match = re.search(r'href="tel:([^"]+)"', block)
        
        if name_match:
            detail_url = name_match.group(1)
            name = name_match.group(2).strip()
            address = address_match.group(1).strip() if address_match else ""
            phone = phone_match.group(1).strip() if phone_match else ""
            
            # Check if there is a website link
            website_match = re.search(r"loggerable-external-link\" data=\"([^\"]+)\"", block)
            website = website_match.group(1) if website_match else ""
            
            # Sometimes the website is just "Website" link pointing to detail page
            # We need to check if the detail page has the real URL
            
            dentists.append({
                'Name': name,
                'Address': address,
                'Phone': phone,
                'Website': website,
                'DetailURL': detail_url
            })
    return dentists

def get_real_website(detail_url):
    html = fetch_url(detail_url)
    if html:
        # Pattern: <a class="coffsd-link loggerable-external-link" data="http://www.paramountdentalsydney.com.au" ...
        match = re.search(r'class="[^"]*loggerable-external-link[^"]*" data="([^"]+)"', html)
        if match:
            return match.group(1)
    return ""

def scrape_state(state, start_url):
    all_dentists = {} # Keyed by Name + Phone to avoid duplicates
    suburb_queue = [start_url]
    visited_suburbs = set()
    
    count = 0
    max_suburbs = 50 # Limit for now to test, will increase if it works well
    
    while suburb_queue and count < max_suburbs:
        url = suburb_queue.pop(0)
        if url in visited_suburbs: continue
        visited_suburbs.add(url)
        
        print(f"Scraping {url}...")
        html = fetch_url(url)
        if not html: continue
        
        # Extract dentists from main page (Premium)
        found = extract_dentists(html)
        for d in found:
            key = (d['Name'], d['Phone'])
            if key not in all_dentists:
                all_dentists[key] = d
        
        # Extract dentists from AJAX (Standard)
        # We need the address/suburb name for the AJAX call
        # It's usually in the <h2>: 23 Dentists found in WOOLLOOMOOLOO NSW 2011
        addr_match = re.search(r'<h2>\d+ Dentists found in (.*?) and close by</h2>', html)
        if addr_match:
            suburb_addr = addr_match.group(1)
            ajax_html = fetch_url("https://www.dentist.com.au/index.php/ajax/processing_module", 
                                 post_data={
                                     'module': 'dsearch',
                                     'cmd': 'dentist:results:standard_list:search',
                                     'current_page': 1,
                                     'address': suburb_addr,
                                     'type': '',
                                     'value': ''
                                 })
            if ajax_html:
                std_found = extract_dentists(ajax_html)
                for d in std_found:
                    key = (d['Name'], d['Phone'])
                    if key not in all_dentists:
                        all_dentists[key] = d

        # Add new suburbs to queue
        new_suburbs = extract_suburbs(html, state)
        for s in new_suburbs:
            if s not in visited_suburbs:
                suburb_queue.append(s)
        
        count += 1
        time.sleep(1) # Be nice
        
    # Second pass: get real websites for those that don't have them
    # To save time, we'll only do a few or skip if requested
    print(f"Found {len(all_dentists)} dentists in {state}. Fetching websites...")
    final_list = []
    for i, d in enumerate(all_dentists.values()):
        if not d['Website'] and d['DetailURL']:
            # d['Website'] = get_real_website(d['DetailURL'])
            # time.sleep(0.5)
            pass
        final_list.append({
            'Practice Name': d['Name'],
            'Phone Number': d['Phone'],
            'Full Address': d['Address'],
            'Website URL': d['Website']
        })
        if i % 10 == 0: print(f"Processed {i}/{len(all_dentists)}")
        if i >= 500: break # Safety limit for this task run

    return final_list

def save_csv(data, filename):
    if not data: return
    keys = data[0].keys()
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        dict_writer = csv.DictWriter(f, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)
    print(f"Saved {len(data)} rows to {filename}")

# Main execution
nsw_data = scrape_state('nsw', 'https://www.dentist.com.au/dentist/nsw/sydney')
save_csv(nsw_data, 'Spectrum_Dental_NSW_Lead_List.csv')

qld_data = scrape_state('qld', 'https://www.dentist.com.au/dentist/qld/brisbane')
save_csv(qld_data, 'Spectrum_Dental_QLD_Lead_List.csv')
