
import streamlit as st
import os
from scraper.utils import ensure_folder, zip_folder, sanitize_filename, download_image, dedupe_keep_order
from scraper.engines.google import scrape_google
from scraper.engines.bing import scrape_bing
from scraper.engines.pinterest import scrape_pinterest
from scraper.engines.social import scrape_from_page, scrape_from_post

st.set_page_config(layout="wide", page_title="Image Scraper (Multi-source)")
st.title("Image Scraper — Multiple Sources")

col1, col2 = st.columns([2,1])
with col1:
    keyword = st.text_input("Search keyword or Page/Post URL", placeholder="e.g. cute cats OR https://www.facebook.com/....")
    count = st.number_input("Number of images (max 500)", min_value=1, max_value=500, value=30)
    source = st.selectbox("Source", ["Google Images", "Bing Images", "Pinterest", "Facebook (public page/post)", "Custom URL (single page)"])
    folder_name = st.text_input("Save folder name (optional)", value="")
    filename_prefix = st.text_input("Filename prefix (optional)", value="img")
with col2:
    st.markdown("### Options")
    dedupe = st.checkbox("Remove duplicate image URLs", value=True)
    show_filenames = st.checkbox("Show filenames under images", value=False)
    zip_after = st.checkbox("Make ZIP after scraping (downloadable)", value=True)

if st.button("Start Scraping"):
    if not keyword.strip():
        st.error("Please provide a search keyword or a page/post URL.")
    else:
        out_folder = folder_name.strip() or keyword.strip().replace(" ", "_")
        out_dir = ensure_folder(out_folder)
        images = []
        progress = st.progress(0)
        status = st.empty()
        try:
            status.info("Scraping — this may take a moment.")
            if source == "Google Images":
                images = scrape_google(keyword, count, out_dir, prefix=filename_prefix, progress_callback=progress.progress)
            elif source == "Bing Images":
                images = scrape_bing(keyword, count, out_dir, prefix=filename_prefix, progress_callback=progress.progress)
            elif source == "Pinterest":
                images = scrape_pinterest(keyword, count, out_dir, prefix=filename_prefix, progress_callback=progress.progress)
            elif source == "Facebook (public page/post)":
                # try to detect if URL was given
                if keyword.startswith("http"):
                    images = scrape_from_post(keyword, count, out_dir, prefix=filename_prefix, progress_callback=progress.progress)
                    if not images:
                        images = scrape_from_page(keyword, count, out_dir, prefix=filename_prefix, progress_callback=progress.progress)
                else:
                    status.warning("For Facebook, provide a public page or post URL in the input above.")
            elif source == "Custom URL (single page)":
                images = scrape_from_page(keyword, count, out_dir, prefix=filename_prefix, progress_callback=progress.progress)
        except Exception as e:
            st.exception(e)
        finally:
            progress.progress(100)

        if dedupe:
            images = dedupe_keep_order(images)

        st.success(f"Saved {len(images)} images to {out_dir}")

        # display gallery
        cols = st.columns(4)
        for idx, img in enumerate(images):
            c = cols[idx % 4]
            try:
                c.image(img, use_container_width=True)
                if show_filenames:
                    c.caption(os.path.basename(img))
            except:
                c.write("Unable to display image")

        if zip_after:
            zip_path = zip_folder(out_dir)
            with open(zip_path, "rb") as f:
                st.download_button("Download ZIP", f, file_name=os.path.basename(zip_path))
        st.info("Note: Scraping social platforms may be limited by site policies and login requirements. This app attempts to extract public image URLs (og:image, img tags).")
