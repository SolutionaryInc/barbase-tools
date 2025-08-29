from bs4 import BeautifulSoup

async def fetch_product_data(session, url):
    async with session.get(url) as response:
        html = await response.text()
        soup = BeautifulSoup(html, "html.parser")
        
        # Находим html где храниться имя и штрихкод
        name_tag = soup.find("h2", itemprop="name")
        barcode_tag = soup.find("span", id="barcode")
        
        # тут мы вытаскиваем только само имя и сам штрихкод, без остальной информации
        name = next(name_tag.stripped_strings)
        barcode = barcode_tag.get_text(strip=True)
        
        return {"name": name, "barcode": barcode}
