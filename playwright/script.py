from playwright.sync_api import sync_playwright
import requests, os, time
from urllib.parse import urlparse, parse_qs, unquote

p = sync_playwright().start()
browser = p.firefox.launch(headless=False)
page = browser.new_page()
page.goto("https://sssinstagram.com/")

page.wait_for_selector("input.form__input")
page.fill("input.form__input", "https://www.instagram.com/reel/DG21dFUtx3D")
page.click("button.form__submit")

download_selector = "a.button__download[href^='https://media.sssinstagram.com']"
page.wait_for_selector(download_selector)

# Get the download link from the page
download_link = page.get_attribute(download_selector, "href")
print("Download link:", download_link)

url = download_link

parsed_url = urlparse(url)
query_params = parse_qs(parsed_url.query)

# Attempt to retrieve the filename from the query parameters
if 'filename' in query_params:
    file_name = unquote(query_params['filename'][0])
else:
    file_name = os.path.basename(parsed_url.path)
    if not file_name:
        file_name = "downloaded_file"

# Sanitize the filename to remove invalid characters (Windows example)
def sanitize_filename(name):
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        name = name.replace(char, '_')
    return name

file_name = sanitize_filename(file_name)

# Download the file
response = requests.get(url)
if response.status_code == 200:
    with open(file_name, "wb") as file:
        file.write(response.content)
    print(f"Download completed successfully. File saved as: {file_name}")
else:
    print(f"Failed to download. HTTP status code: {response.status_code}")
# Keep the browser open
time.sleep(999999)