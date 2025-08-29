from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import json

# Path to chromedriver
service = Service("C:\\Program Files (x86)\\chromedriver-win64\\chromedriver.exe")
driver = webdriver.Chrome(service=service)

# URL of the page with the list of products
base_url = "https://www.foodrepo.org/en/products"
driver.get(base_url)
time.sleep(5)

# Receive HTML
soup = BeautifulSoup(driver.page_source, 'html.parser')

# Find all links to product pages
product_links = list(set([a['href'] for a in soup.find_all('a', href=True) if '/en/products/' in a['href']]))

products_data = []

# Going through each link
for link in product_links:
    product_url = f"https://www.foodrepo.org{link}"
    driver.get(product_url)
    time.sleep(3)

    product_soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Product name
    title_tag = product_soup.find('h1')
    title_text = title_tag.get_text(strip=True) if title_tag and not title_tag.get_text(strip=True).isdigit() else "Not found"

    # Images
    img_tags = product_soup.find_all('img', alt=lambda x: x and x.startswith("Image #"))
    img_urls = [img['src'] for img in img_tags if img.get('src')]

    # Barcode (EAN)
    barcode_div = product_soup.find('span', class_='font-weight-bold', string='Barcode')
    if barcode_div and barcode_div.parent:
        barcode_text = barcode_div.parent.get_text(strip=True).replace('Barcode', '').strip()
        barcode = barcode_text if barcode_text.isdigit() else 'Not found'
    else:
        barcode = 'Not found'

    products_data.append({
        "barcode": barcode,
        "name": title_text,
        "image_links": img_urls
    })

driver.quit()

# Save in JSON
with open("foodrepo.json", "w", encoding="utf-8") as f:
    json.dump(products_data, f, ensure_ascii=False, indent=4)

print("Data successfully saved in 'foodrepo.json'")
