from bs4 import BeautifulSoup

try:
    with open("google_sample.html", "r", encoding="utf-8") as f:
        html = f.read()
    
    soup = BeautifulSoup(html, "html.parser")
    scripts = soup.find_all("script")
    
    print(f"Found {len(scripts)} scripts.")
    
    with open("scripts_dump.txt", "w", encoding="utf-8") as out:
        for i, script in enumerate(scripts):
            if script.string:
                out.write(f"\n--- SCRIPT {i} ---\n")
                out.write(script.string)
    print("Dumped scripts to scripts_dump.txt")
except Exception as e:
    print(f"Error: {e}")
