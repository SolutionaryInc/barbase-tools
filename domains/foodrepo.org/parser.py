import cloudscraper
import json
import time
import random

API_KEY = "YOUR_API_KEY" # Insert your API-key here
BASE_URL = "https://www.foodrepo.org/api/v3/products"

HEADERS = {
    "Authorization": f"Token token={API_KEY}",
    "Accept": "application/json",
    "User-Agent": "Mozilla/5.0"
}

def fetch_all_products(page_size=100, delay=0.5, max_pages=None, output_file="foodrepo_all.json", lang="en"):
    scraper = cloudscraper.create_scraper()
    page = 1
    all_products = []
    MAX_RETRIES = 5  # Maximum retry attempts per page if request fails

    while True:
        params = {
            "page[number]": page, # current page
            "page[size]": page_size # number of products per page
        }

        # Request with retries in case of network/Cloudflare issues
        for attempt in range(MAX_RETRIES):
            try:
                response = scraper.get(BASE_URL, headers=HEADERS, params=params, timeout=30)
                response.raise_for_status() # raise error if status != 200
                break
            except Exception as e:
                print(f"Error on page {page}, attempt {attempt+1}/{MAX_RETRIES}: {e}")
                time.sleep(3 * (attempt + 1))  # exponential backoff before retry
        else:
            print(f"Failed to load page {page} after {MAX_RETRIES} retries, stopping.") # if all retries failed
            break

        # Parse JSON response
        data = response.json()
        products = data.get("data", [])

        if not products:
            print("No more products.")
            break

        # Extract required fields for each product
        for product in products:
            barcode = product.get("barcode") or "Not found"
            name = product.get("display_name_translations", {}).get(lang) or \
                   product.get("display_name_translations", {}).get("en", "Not found")
            raw_images = product.get("images", [])
            images = [img.get("large") for img in raw_images if "large" in img]

            all_products.append({
                "barcode": barcode,
                "name": name,
                "image_links": images
            })

        print(f"Page {page} loaded ({len(products)} products)")

        # Save progress every 100 pages (backup)
        if page % 100 == 0:
            temp_file = f"{output_file.rsplit('.',1)[0]}_part.json"
            with open(temp_file, "w", encoding="utf-8") as f:
                json.dump(all_products, f, ensure_ascii=False, indent=2)
            print(f"Progress saved to {temp_file} (page {page})")

        # Next page
        page += 1
        # Randomized delay to reduce chance of getting blocked
        time.sleep(delay + random.uniform(0, 0.5))

        # Optional limit for debugging
        if max_pages and page > max_pages:
            print("Max pages reached.")
            break

    # Parsed
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_products, f, ensure_ascii=False, indent=2)

    print(f"Saved {len(all_products)} products to {output_file}")

# Run the parser
if __name__ == "__main__":
    fetch_all_products(page_size=200, delay=1.0, lang="en")
