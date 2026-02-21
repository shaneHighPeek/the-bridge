import sys
import re

def parse_markdown(content):
    # Regex to find practice entries by splitting on the practice name pattern
    # Looking for ### [Name](URL)Dentist IN
    entries = re.split(r'### ', content)[1:]
    
    results = []
    for entry in entries:
        try:
            # Name
            name_match = re.match(r'\[(.*?)\]', entry)
            if not name_match: continue
            name = name_match.group(1).strip()
            
            # Address - often the first non-empty line after the header line
            lines = [l.strip() for l in entry.split('\n') if l.strip()]
            address = ""
            for i in range(len(lines)):
                if 'Dentist IN' in lines[i] and i+1 < len(lines):
                    # The next line should be the address
                    address = lines[i+1]
                    break
            
            # Phone
            phone_match = re.search(r'\[Call Us\]\(tel:(.*?)\)', entry)
            phone = phone_match.group(1).strip() if phone_match else ""
            if phone.startswith('(') and ')' not in phone:
                # Handle cases where the regex might have cut off early
                # or find the full phone number in the entry
                full_phone_match = re.search(r'tel:(\(03\) \d{4}-\d{4})', entry)
                if full_phone_match:
                    phone = full_phone_match.group(1)
                elif phone_match:
                    # Try to reconstruct from the text if it's there
                    tel_text_match = re.search(r'tel:(.*?)\)', entry)
                    if tel_text_match:
                        phone = tel_text_match.group(1)
            
            # Website
            website_match = re.search(r'\[Website\]\((.*?)\)', entry)
            website = website_match.group(1).strip() if website_match else ""
            
            if name and address:
                results.append({'name': name, 'address': address, 'phone': phone, 'website': website})
        except Exception:
            continue
            
    return results

if __name__ == "__main__":
    content = sys.stdin.read()
    practices = parse_markdown(content)
    for p in practices:
        # Use a more reliable separator
        print(f"{p['name']}|||{p['address']}|||{p['phone']}|||{p['website']}")
