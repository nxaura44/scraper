import re

with open("scripts_dump.txt", "r", encoding="utf-8") as f:
    content = f.read()

# Pattern for ["http...", number, number]
# This signifies ["URL", width, height] or similar
pattern = r'\["(http[^"]+)",(\d+),(\d+)\]'
matches = re.finditer(pattern, content)

count = 0
for match in matches:
    url = match.group(1)
    w = match.group(2)
    h = match.group(3)
    
    # Filter out small images or thumbnails
    if int(w) > 300 and int(h) > 300:
        print(f"Found High-Res Candidate: {w}x{h}")
        print(f"URL: {url}")
        count += 1
        if count >= 10:
            break

if count == 0:
    print("No high-res candidates found with pattern.")

