import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse ,unquote
import os
import time

# base_url = "https://stritstax.com"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}
visited_urls = set()
output_folder_name = "scraped_pages"

os.makedirs(output_folder_name, exist_ok=True)

def create_filename(url):
    parsed_url = urlparse(unquote(url))
    path = parsed_url.path.strip("/")
    filename = path.replace("/","_") if path else "index"
    return f"{filename}.txt"

def save_page(url, content):
    file_name = create_filename(url)
    try:
        file_path = os.path.join(output_folder_name, file_name)
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(content)
        print(f"Page saved: {file_name}")
    except IOError as e:
        print(f"Failed to save page: {file_name}")

def get_links(url, content):
    soup = BeautifulSoup(content, "html.parser")
    links = set()
    for link in soup.find_all("a"):
        href = link.get("href")
        if href is not None and base_url in href:
            full_url = urljoin(url, href)
            links.add(full_url)
    return links

def fetch_page(url):
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            page_content = BeautifulSoup(response.text, "html.parser")
            return page_content.prettify()
        else:
            print(f"Failed to fetch page: {url}")
            return None
    except requests.RequestException as e:
        print(f"Failed to fetch page: {url}")
        return None
    

def scrape_page(url):
    if url in visited_urls:
        return
    visited_urls.add(url)
    content = fetch_page(url)
    if content:
        save_page(url, content)
        for link in get_links(url, content):
            scrape_page(link)
        time.sleep(1)


base_url = input("Enter the base URL: ")
print("Starting to scrape pages...")
scrape_page(base_url)
print("Scraping completed.")

