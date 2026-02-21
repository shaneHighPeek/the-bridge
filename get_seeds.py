
import urllib.request
import re

def get_suburbs(state_code):
    url = f"https://www.dentist.com.au/dentist/{state_code.lower()}"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            html = response.read().decode('utf-8')
    except urllib.error.HTTPError as e:
        html = e.read().decode('utf-8')
    except:
        return []
    
    # Extract links like /dentist/nsw/suburb
    pattern = rf'/dentist/{state_code.lower()}/([a-z0-9-]+)'
    suburbs = re.findall(pattern, html)
    return [f"https://www.dentist.com.au/dentist/{state_code.lower()}/{s}" for s in set(suburbs)]

print("VIC seeds:", get_suburbs('VIC'))
print("NSW seeds:", get_suburbs('NSW'))
print("QLD seeds:", get_suburbs('QLD'))
