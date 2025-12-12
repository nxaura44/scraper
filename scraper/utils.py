
import os, zipfile, re, requests, time, hashlib
from urllib.parse import urlparse, unquote

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Cache-Control": "max-age=0",
}

def ensure_folder(name):
    path = os.path.join("downloads", sanitize_filename(name))
    os.makedirs(path, exist_ok=True)
    return path

def zip_folder(folder_path):
    zip_path = folder_path + ".zip"
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as z:
        for root, _, files in os.walk(folder_path):
            for f in files:
                full = os.path.join(root, f)
                z.write(full, os.path.relpath(full, folder_path))
    return zip_path

def sanitize_filename(s):
    s = str(s)
    s = s.strip().replace(" ", "_")
    return re.sub(r'[^A-Za-z0-9_\-\.]+', '', s)

def download_image(url, out_dir, prefix='img', idx=0, max_retries=2):
    # returns saved filepath or None
    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
        if resp.status_code != 200:
            return None
        ext = ".jpg"
        # try to detect extension
        parsed = urlparse(url)
        name = os.path.basename(unquote(parsed.path)) or f"{prefix}_{idx}"
        if '.' in name and len(name.split('.')[-1]) <= 4:
            ext = '.' + name.split('.')[-1]
            name = os.path.splitext(name)[0]
        fname = sanitize_filename(f"{prefix}_{idx}_{name}{ext}")
        out_path = os.path.join(out_dir, fname)
        with open(out_path, "wb") as f:
            f.write(resp.content)
        return out_path
    except Exception:
        return None

def dedupe_keep_order(seq):
    seen = set()
    out = []
    for x in seq:
        if x not in seen:
            seen.add(x)
            out.append(x)
    return out
