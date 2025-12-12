
import requests
from bs4 import BeautifulSoup
from scraper.utils import HEADERS, download_image

def scrape_from_page(url, count, out_dir, prefix='img', progress_callback=None):
    """Attempt to scrape images from a public page URL (facebook, twitter, instagram public pages)."""
    html = requests.get(url, headers=HEADERS, timeout=15).text
    soup = BeautifulSoup(html, "html.parser")
    imgs = []
    idx = 0
    # try og:image
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

def scrape_from_post(url, count, out_dir, prefix='img', progress_callback=None):
    """Special attempt to extract images from a single post URL (public)."""
    return scrape_from_page(url, count, out_dir, prefix=prefix, progress_callback=progress_callback)
