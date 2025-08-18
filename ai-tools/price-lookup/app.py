import asyncio
from crawl4ai import *

async def main():
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url="https://greenwich-shop.kz/product/batonchik-shokoladnyy-twix-55-gr",
        )
        print(result.markdown)

if __name__ == "__main__":
    asyncio.run(main())