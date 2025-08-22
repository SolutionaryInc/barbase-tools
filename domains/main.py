import asyncio
import aiohttp
from bs4 import BeautifulSoup as BS
from fake_useragent import UserAgent
import json
import re

BASE_URL = "https://ovdi.ru/shop/malysham/"
HEADERS = {"User-Agent": UserAgent().random}

async def main():
    products = []

    async with aiohttp.ClientSession() as session:


async def main():
    products = []
    ua = UserAgent()

    async with aiohttp.ClientSession() as session:
        headers = {"User-Agent": ua.random}
        async with session.get(BASE_URL, headers=headers) as response:
            html = await response.text()
            soup = BS(html, "html.parser")

            items = soup.find_all("div", {"class": "bx_catalog_item_container"})
            for item in items:
                title_tag = item.find("div", {"class": "bx_catalog_item_title"})
                title = title_tag.text.strip() if title_tag else "No title"

                link_tag = title_tag.find("a") if title_tag else None
                link = "https://ovdi.ru" + link_tag.get("href") if link_tag else None

                price_tag = item.find("div", {"class": "bx_catalog_item_price"})
                price = price_tag.text.strip() if price_tag else "No price"

                barcode = "Штрихкод табылмады"
                if link:
                    async with session.get(link, headers=HEADERS) as product_response:
                        product_html = await product_response.text()
                        product_soup = BS(product_html, "html.parser")

                        text = product_soup.get_text(" ", strip=True)
                        match = re.search(r"Штрихкод:\s*(\d+)", text)
                        if match:
                            barcode = match.group(1)

                products.append({
                    "title": title,
                    "price": price,
                    "link": link,
                    "barcode": barcode
                })

    with open("products.json", "w", encoding="utf-8") as f:
        json.dump(products, f, ensure_ascii=False, indent=4)

    print("✅ products.json дайын!")

if __name__ == '__main__':
    asyncio.run(main())
