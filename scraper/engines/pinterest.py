
import requests, re, json
from bs4 import BeautifulSoup
from scraper.utils import HEADERS, download_image

def scrape_pinterest(query_or_url, count, out_dir, prefix='img', progress_callback=None):
    # If URL provided, fetch that page; otherwise do a search
    if query_or_url.startswith("http"):
        url = query_or_url
    else:
        q = query_or_url.replace(" ", "%20")
        url = f"https://www.pinterest.com/search/pins/?q={q}"
    html = requests.get(url, headers=HEADERS, timeout=15).text
    soup = BeautifulSoup(html, "html.parser")
    imgs = []
    idx = 0
    # Look for og:image or meta images
    og = soup.find("meta", property="og:image")
    if og and og.get("content"):
        saved = download_image(og.get("content"), out_dir, prefix=prefix, idx=idx)
        if saved:
            imgs.append(saved)
            idx += 1
    # find <img> tags
    for img in soup.find_all("img"):
        if len(imgs) >= count:
            break
        src = img.get("src") or img.get("data-src")
        if not src or src.startswith("data:"):
            continue
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
