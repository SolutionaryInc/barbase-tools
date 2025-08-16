const { MongoClient } = require('mongodb');
const fetch = (...args) => import('node-fetch').then(({default: fetch}) => fetch(...args));
const fs = require('fs');

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}


const PROGRESS_FILE = './progress.json';


async function main() {
    const client = new MongoClient("mongodb://localhost:27017");
    try {
        await client.connect();
        console.log("Подключение к MongoDB успешно!");

        const db = client.db("openfoodfacts");

        const collection = db.collection("products");
        
        await collection.createIndex({ code: 1 }, { unique: true });
        
        let page = 1;
        if (fs.existsSync(PROGRESS_FILE)) {
            const progress = JSON.parse(fs.readFileSync(PROGRESS_FILE, 'utf-8'));
            page = progress.page || 1;
        }

        const pageSize = 1000;
        let totalProcessed = 0;

        while (true) {
            try {
                const url = `https://world.openfoodfacts.org/api/v2/search?fields=code,product_name&page=${page}&page_size=${pageSize}`;
                const response = await fetch(url);
                const data = await response.json();

                if (!data.products || data.products.length === 0) {
                    console.log("Все продукты загружены.");
                    break;
                }

                const products = data.products
                    .filter(item => item.product_name)
                    .map(item => ({ code: item.code, name: item.product_name }));

                if (products.length > 0) {
                    let updatedOrInserted = 0;

                    for (const product of products) {
                        try {
                            const result = await collection.updateOne(
                                { code: product.code },   
                                { $set: product },        
                                { upsert: true }          
                            );
                            if (result.upsertedCount === 1 || result.modifiedCount === 1) {
                                updatedOrInserted++;
                            }
                        } catch (err) {
                            console.log(`Ошибка с продуктом ${product.code}:`, err.message);
                        }
                    }

                    totalProcessed += updatedOrInserted;
                    console.log(`Страница ${page}: обновлено/добавлено ${updatedOrInserted} товаров, всего обработано: ${totalProcessed}`);
                } else {
                    console.log(`Страница ${page}: нет продуктов с названием.`);
                }

                
                fs.writeFileSync(PROGRESS_FILE, JSON.stringify({ page: page + 1 }));
                
                page++;
                await sleep(500); 
            } catch (err) {
                console.error(`Ошибка на странице ${page}:`, err.message);
                console.log("Повтор через 5 секунд...");
                await sleep(5000);
            }
        }
    } catch (err) {
        console.error(err);
    } finally {
        await client.close();
        console.log("Подключение к MongoDB закрыто.");
    }
}

main();
