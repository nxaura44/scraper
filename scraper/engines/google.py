
import requests, json, time, re
from bs4 import BeautifulSoup
from scraper.utils import HEADERS, download_image

def scrape_google(keyword, count, out_dir, prefix='img', progress_callback=None):
    q = keyword.replace(" ", "+")
    # udm=2 sometimes forces the new web-search-like images interface, but let's stick to standard tbm=isch
    url = f"https://www.google.com/search?tbm=isch&q={q}" 
    
    status_code = 0
    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
        status_code = resp.status_code
        html = resp.text
    except Exception as e:
        print(f"Error fetching Google: {e}")
        return []

    imgs = []
    
    # Regex to find ["http...", width, height]
    # We look for the pattern ["http://...", 1234, 1234]
    pattern = r'\["(http[^"]+)",(\d+),(\d+)\]'
    matches = re.finditer(pattern, html)
    
    candidates = []
    for match in matches:
        link = match.group(1)
        w = int(match.group(2))
        h = int(match.group(3))
        
        # Filter for high quality (e.g., > 300px)
        if w > 300 and h > 300:
            candidates.append(link)

    # Dedup right away to avoid downloading same URL found multiple times in script
    # (Use dict to preserve order)
    candidates = list(dict.fromkeys(candidates))
    
    print(f"Found {len(candidates)} high-res candidates for '{keyword}'")

    idx = 0
    for src in candidates:
        if len(imgs) >= count:
            break
            
        saved = download_image(src, out_dir, prefix=prefix, idx=idx)
        if saved:
            imgs.append(saved)
            idx += 1
            if progress_callback:
                try:
                    progress_callback(int(len(imgs)/count*100))
                except:
                    pass
    
    return imgs
