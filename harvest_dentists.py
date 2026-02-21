
import urllib.request
import re
import csv
import os
import time

def fetch_url(url):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            return response.read().decode('utf-8', errors='ignore')
    except Exception as e:
        return None

def extract_dentists(html):
    listings = []
    chunks = html.split('<div class="info-row">')[1:]
    for chunk in chunks:
        name_match = re.search(r'class="p_profile"[^>]*>(.*?)</a>', chunk)
        addr_match = re.search(r'<address>(.*?)</address>', chunk, re.DOTALL)
        phone_match = re.search(r'href="tel:([^"]*)"', chunk)
        profile_match = re.search(r'class="p_profile" href="([^"]*)"', chunk)
        
        if name_match:
            name = name_match.group(1).strip()
            name = re.sub(r'<[^>]+>', '', name)
            address = addr_match.group(1).strip() if addr_match else ""
            address = re.sub(r'\s+', ' ', address)
            address = re.sub(r'<[^>]+>', '', address)
            phone = phone_match.group(1).strip() if phone_match else ""
            profile_url = profile_match.group(1).strip() if profile_match else ""
            if profile_url and not profile_url.startswith('http'):
                profile_url = 'https://www.dentist.com.au' + profile_url
            
            listings.append({
                'Practice Name': name,
                'Address': address,
                'Phone': phone,
                'Website': profile_url 
            })
    return listings

def extract_suburbs(html, state_code):
    pattern = rf'https://www.dentist.com.au/dentist/{state_code.lower()}/[a-z0-9-]+'
    links = re.findall(pattern, html)
    rel_pattern = rf'href="/dentist/{state_code.lower()}/([a-z0-9-]+)"'
    rel_links = re.findall(rel_pattern, html)
    for rl in rel_links:
        links.append(f'https://www.dentist.com.au/dentist/{state_code.lower()}/{rl}')
    return list(set(links))

def harvest(state_code, seed_urls, source_file, target_file, target_count):
    seen_names = set()
    for fpath in [source_file, target_file]:
        if os.path.exists(fpath):
            with open(fpath, 'r', newline='', encoding='utf-8') as f:
                try:
                    reader = csv.DictReader(f)
                    for row in reader:
                        name = row.get('Practice Name') or row.get('Name')
                        if name:
                            seen_names.add(name)
                except: pass

    if not os.path.exists(target_file) or os.path.getsize(target_file) == 0:
        with open(target_file, 'w', newline='', encoding='utf-8') as f_out:
            fieldnames = ['Practice Name', 'Address', 'Phone', 'Website']
            writer = csv.DictWriter(f_out, fieldnames=fieldnames)
            writer.writeheader()
            if os.path.exists(source_file):
                with open(source_file, 'r', newline='', encoding='utf-8') as f_in:
                    try:
                        reader = csv.DictReader(f_in)
                        for row in reader:
                            writer.writerow({
                                'Practice Name': row.get('Practice Name') or row.get('Name') or "",
                                'Address': row.get('Full Address') or row.get('Address') or "",
                                'Phone': row.get('Phone Number') or row.get('Phone') or "",
                                'Website': row.get('Website URL') or row.get('Website') or ""
                            })
                    except: pass
    
    count = len(seen_names)
    print(f"Starting {state_code}: {count} existing, target {target_count}")
    if count >= target_count:
        print(f"{state_code} target reached.")
        return

    queue = list(seed_urls)
    visited = set(seed_urls)
    with open(target_file, 'a', newline='', encoding='utf-8') as f:
        fieldnames = ['Practice Name', 'Address', 'Phone', 'Website']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        while queue and count < target_count:
            url = queue.pop(0)
            print(f"[{state_code}] {count}/{target_count} - {url}")
            html = fetch_url(url)
            if not html: continue
            dentists = extract_dentists(html)
            new_found = 0
            for d in dentists:
                if d['Practice Name'] not in seen_names:
                    writer.writerow(d)
                    f.flush() # Flush to disk
                    seen_names.add(d['Practice Name'])
                    count += 1
                    new_found += 1
                    if count >= target_count: break
            print(f"  Found {new_found} new.")
            if count >= target_count: break
            suburbs = extract_suburbs(html, state_code)
            for s in suburbs:
                if s not in visited:
                    visited.add(s)
                    queue.append(s)
            time.sleep(0.01)
    print(f"Finished {state_code}. Total: {count}")

vic_seeds = ['https://www.dentist.com.au/dentist/vic/melbourne', 'https://www.dentist.com.au/dentist/vic/geelong', 'https://www.dentist.com.au/dentist/vic/ballarat', 'https://www.dentist.com.au/dentist/vic/bendigo']
nsw_seeds = ['https://www.dentist.com.au/dentist/nsw/haymarket', 'https://www.dentist.com.au/dentist/nsw/alexandria', 'https://www.dentist.com.au/dentist/nsw/zetland', 'https://www.dentist.com.au/dentist/nsw/potts-point', 'https://www.dentist.com.au/dentist/nsw/darlington', 'https://www.dentist.com.au/dentist/nsw/surry-hills', 'https://www.dentist.com.au/dentist/nsw/eveleigh', 'https://www.dentist.com.au/dentist/nsw/elizabeth-bay', 'https://www.dentist.com.au/dentist/nsw/rosebery', 'https://www.dentist.com.au/dentist/nsw/centennial-park', 'https://www.dentist.com.au/dentist/nsw/paddington', 'https://www.dentist.com.au/dentist/nsw/sydney-domestic-airport', 'https://www.dentist.com.au/dentist/nsw/darlinghurst', 'https://www.dentist.com.au/dentist/nsw/woolloomooloo', 'https://www.dentist.com.au/dentist/nsw/botany', 'https://www.dentist.com.au/dentist/nsw/the-rocks', 'https://www.dentist.com.au/dentist/nsw/beaconsfield', 'https://www.dentist.com.au/dentist/nsw/moore-park', 'https://www.dentist.com.au/dentist/nsw/waterloo', 'https://www.dentist.com.au/dentist/nsw/bondi-junction', 'https://www.dentist.com.au/dentist/nsw/sydney', 'https://www.dentist.com.au/dentist/nsw/eastlakes', 'https://www.dentist.com.au/dentist/nsw/redfern', 'https://www.dentist.com.au/dentist/nsw/mascot', 'https://www.dentist.com.au/dentist/nsw/ultimo', 'https://www.dentist.com.au/dentist/nsw/banksmeadow', 'https://www.dentist.com.au/dentist/nsw/broadway', 'https://www.dentist.com.au/dentist/nsw/chippendale', 'https://www.dentist.com.au/dentist/nsw/pyrmont', 'https://www.dentist.com.au/dentist/nsw/queens-park', 'https://www.dentist.com.au/dentist/nsw/rushcutters-bay', 'https://www.dentist.com.au/dentist/nsw/dawes-point', 'https://www.dentist.com.au/dentist/nsw/millers-point']
qld_seeds = ['https://www.dentist.com.au/dentist/qld/brisbane', 'https://www.dentist.com.au/dentist/qld/gold-coast', 'https://www.dentist.com.au/dentist/qld/sunshine-coast', 'https://www.dentist.com.au/dentist/qld/townsville', 'https://www.dentist.com.au/dentist/qld/cairns', 'https://www.dentist.com.au/dentist/qld/ipswich', 'https://www.dentist.com.au/dentist/qld/toowoomba', 'https://www.dentist.com.au/dentist/qld/mackay', 'https://www.dentist.com.au/dentist/qld/rockhampton']

harvest('VIC', vic_seeds, 'Spectrum_VIC_300.csv', 'Spectrum_VIC_300.csv', 305)
harvest('NSW', nsw_seeds, 'Spectrum_Dental_NSW_Lead_List.csv', 'Spectrum_NSW_300.csv', 305)
harvest('QLD', qld_seeds, 'Spectrum_Dental_QLD_Lead_List.csv', 'Spectrum_QLD_300.csv', 305)
