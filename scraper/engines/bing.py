
import requests
from bs4 import BeautifulSoup
from scraper.utils import HEADERS, download_image

def scrape_bing(keyword, count, out_dir, prefix='img', progress_callback=None):
    q = keyword.replace(" ", "+")
    url = f"https://www.bing.com/images/search?q={q}"
    html = requests.get(url, headers=HEADERS, timeout=15).text
    soup = BeautifulSoup(html, "html.parser")
    imgs = []
    idx = 0
    for m in soup.find_all("img"):
        if len(imgs) >= count:
            break
        src = m.get("src") or m.get("data-src")
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
