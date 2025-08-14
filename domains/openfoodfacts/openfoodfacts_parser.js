const fs = require('fs');
const fetch = (...args) => import('node-fetch').then(({default: fetch}) => fetch(...args));

async function fetchProducts() {
    const url = "https://world.openfoodfacts.org/api/v2/search?fields=code,product_name&limit=20";
    const response = await fetch(url);
    const data = await response.json();

    
    const jsonlData = data.products
        .filter(item => item.product_name)
        .map(item => JSON.stringify({ code: item.code, name: item.product_name }))
        .join('\n');

   
    fs.writeFileSync('products.jsonl', jsonlData, 'utf8');
 
}

fetchProducts();
