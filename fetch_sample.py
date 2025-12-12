import requests

headers = {
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
url = "https://www.google.com/search?q=cute+cats&tbm=isch&udm=2" # udm=2 forces the new "web" layout sometimes, but simple tbm=isch is standard. Let's stick to standard but maybe add safe=active.
url = "https://www.google.com/search?q=cute+cats&tbm=isch"

try:
    response = requests.get(url, headers=headers, timeout=20)
    print(f"Status Code: {response.status_code}")
    print(f"Content length: {len(response.text)}")
    with open("google_sample.html", "w", encoding="utf-8") as f:
        f.write(response.text)
    print("Successfully saved google_sample.html")
except Exception as e:
    print(f"Error: {e}")
