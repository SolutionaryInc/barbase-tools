import asyncio
import aiohttp
from bs4 import BeautifulSoup as BS

BASE_URL = "https://arbuz.kz/ru/almaty/catalog/cat/225209-morozhenoe"
HEADERS = {"User-Agent": "Mozilla/5.0"}

async def main():
    async with aiohttp.ClientSession() as session:
        async with session.get(BASE_URL, headers=HEADERS, timeout=60) as response:
            r = await response.text()
            soup = BS(r, "html.parser")

            items = soup.find_all("article", {"class": "product-item product-card"})
            for item in items:
                title_tag = item.find("a", {"class": "product-card__title"})
                if title_tag:
                    link = f"https://arbuz.kz{title_tag.get('href')}"
                    price_tag = item.find("b")

                    title = title_tag.text.strip()
                    price = price_tag.text.strip() if price_tag else "Бағасы жоқ"

                    print(f"{title} | {price} | {link}")

if __name__ == "__main__":
    asyncio.run(main())
