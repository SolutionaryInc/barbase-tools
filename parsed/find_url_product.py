from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

async def fetch_product_urls(base_url, page_number):
    page_url = f"{base_url}/{page_number}"
    product_urls = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(page_url)
        
        # Ждем, пока список продуктов загрузится (в течении 10 секунд)
        await page.wait_for_selector("a.list_product_a", timeout=10000) 
        
        # Получаем HTML страницы после выполнения JavaScript
        html = await page.content()
        soup = BeautifulSoup(html, "html.parser")
        
        # Извлекаем ссылки
        links = soup.select("a.list_product_a")
        for link in links:
            url = link.get("href")
            if url.startswith("http"):
                product_urls.append(url)
            else:
                product_urls.append(base_url + url)
        
        await browser.close()
    return product_urls