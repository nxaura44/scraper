import os, shutil
from scraper.engines.google import scrape_google
from scraper.utils import ensure_folder

# Setup
out_dir = "downloads/verify_test"
if os.path.exists(out_dir):
    shutil.rmtree(out_dir)
os.makedirs(out_dir, exist_ok=True)

print("Starting scrape...")
images = scrape_google("mountain", 5, out_dir)
print(f"Downloaded {len(images)} images.")

if len(images) == 0:
    print("FAILED: No images downloaded.")
    exit(1)

# Check sizes
small_count = 0
large_count = 0
for img in images:
    size = os.path.getsize(img)
    print(f"File: {os.path.basename(img)}, Size: {size/1024:.2f} KB")
    if size < 20 * 1024:
        small_count += 1
    else:
        large_count += 1

print(f"Stats: {large_count} large images, {small_count} small images.")

if large_count > small_count:
    print("SUCCESS: Most images are high quality.")
else:
    print("WARNING: Many images are small. Check if they are actually thumbnails.")
