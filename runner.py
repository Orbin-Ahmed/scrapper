from scrapper import PinterestImageScraper
from downloader import DownloadImage

# Define your search keyword
keyword = "Master+Bed+Room"

# Set optional parameters
max_images = 200
output_folder = "scraped_images"
proxies = {}
threads = 10

scraper = PinterestImageScraper()
DownloadObject = DownloadImage()

# Scrape image URLs
data = scraper.scrape(key=keyword, max_images=max_images, output_folder=output_folder, proxies=proxies)

# Check if any URLs were found
if data["url_list"]:
    print(f"Found {len(data['url_list'])} image URLs for '{keyword}'.")

    # Download the scraped images
    DownloadObject.download(data["url_list"], threads, output_folder)
    print(f"Downloaded images to '{output_folder}'.")
else:
    print(f"No images found for '{keyword}'.")
