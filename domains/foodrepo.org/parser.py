import os
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Driver setup: try env var, else webdriver-manager
driver_path = os.getenv("CHROMEDRIVER_PATH")
if driver_path:
    service = Service(driver_path)
else:
    # save drivers in ./ .wdm and disable logging
    os.environ.setdefault("WDM_LOCAL", "1")
    os.environ.setdefault("WDM_LOG", "0")
    service = Service(ChromeDriverManager().install())

products_data = []

with webdriver.Chrome(service=service) as driver:
    # URL of the page with the list of products
    base_url = "https://www.foodrepo.org/en/products"
    driver.get(base_url)

    # Wait until at least one link to the product appears on the page
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a[href*='/en/products/']")))

    # Receive HTML
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Find all links to product pages
    product_links = list(set([a['href'] for a in soup.find_all('a', href=True) if '/en/products/' in a['href']]))

    # Going through each link
    for link in product_links:
        product_url = f"https://www.foodrepo.org{link}"
        driver.get(product_url)

        # Wait of h1 to appear
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1")))
        product_soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Product name
        title_tag = product_soup.find('h1')
        if title_tag:
            text = title_tag.get_text(strip=True)
            title_text = text if not text.isdigit() else "Not found"
        else:
            title_text = "Not found"

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

# Save in JSON
with open("foodrepo.json", "w", encoding="utf-8") as f:
    json.dump(products_data, f, ensure_ascii=False, indent=4)

print("Data successfully saved in 'foodrepo.json'")
