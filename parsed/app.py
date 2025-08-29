import asyncio
import json
import aiohttp
from find_url_product import fetch_product_urls
from find_name_barcode import fetch_product_data

base_url = "https://world.openfoodfacts.org"
start_page = 1
end_page = 2

async def main(base_url, start_page, end_page):
    for page_number in range(start_page, end_page + 1):
        # Получаем ссылки на продукты с каждой страницы
        urls = await fetch_product_urls(base_url, page_number)

        # Создаем сессию aiohttp для асинхронных запросов
        products = []
        async with aiohttp.ClientSession() as session:
            # Обрабатываем ссылки асинхронно
            tasks = [fetch_product_data(session, url) for url in urls]
            results = await asyncio.gather(*tasks, return_exceptions=True)

            # Собираем валидные данные
            products = [result for result in results]

        ## Тут можно доделать файл, что бы он отправлял JSON файл в parse_to_mongo.js
        ## или же другую базу данных, на другом языке и тд
        # Для примера что бы видеть что происходит и работает ли файл:
        # Сохраняем данные в JSON-файл и сохраняем их
        json_file = f"products_page_{page_number}.json"

        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(products, f, ensure_ascii=False, indent=2)
            print(f"Данные сохранены в {json_file}")

if __name__ == "__main__":
    asyncio.run(main(base_url, start_page, end_page))
