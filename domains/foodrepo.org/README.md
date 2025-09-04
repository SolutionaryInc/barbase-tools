# FoodRepo Product Parser
A Python script for extracting product data from the [FoodRepo API](https://www.foodrepo.org/api-docs/swaggers/v3). It supports Cloudflare bypassing, customizable parameters, and periodic progress saving.

## How It Works
The script sends paginated requests to FoodRepo’s public API and collects product data including:
- Barcode
- Product name (with multilingual support)
- Image URLs (large format only)

Each page can contain up to 200 products, which is the maximum allowed by the API.

## Setup Instructions
1. Install dependencies:
```bash
pip install cloudscraper
```
- Get your API key: Sign up at [FoodRepo](https://www.foodrepo.org/en) and generate your personal API token (on the upper right button - API Keys -> Generate key).
- Insert your API key: In the script, replace the placeholder:
```python
API_KEY = "YOUR_API_KEY" # Insert your API-key here
```

## How to Run
To run the script with default settings:
```bash
python parser.py
```

To customize parameters, modify the call like this:
```python
# Run the parser
if __name__ == "__main__":
    fetch_all_products(page_size=100, delay=0.5, max_pages=None, output_file="foodrepo.json", lang="de")
```

## Customization Options
`page_size` — Number of products per page (max: 200) `default: 100`

`delay` — Delay between requests (in seconds) `default: 0.5`

`max_pages` — Limit total number of pages (useful for testing) `default: None`

`lang` — Language for product name ("en", "de", "fr", etc.) `default: "en"`

`output_file` — Filename for final JSON output `default: foodrepo_all.json`

## Output Format
Each product is saved as a dictionary with the following structure:
```json
{
    "barcode": "7611654884033",
    "name": "Naturaplan - Milk chocolate with hazelnuts",
    "image_links": [
      "https://d2v5oodgkvnw88.cloudfront.net/uploads_production/image/data/3941/large_myImage.jpg?v=1572355321",
      "https://d2v5oodgkvnw88.cloudfront.net/uploads_production/image/data/3939/large_myImage.jpg?v=1572355321",
      "https://d2v5oodgkvnw88.cloudfront.net/uploads_production/image/data/67319/large_myImage.jpg?v=1572355321",
      "https://d2v5oodgkvnw88.cloudfront.net/uploads_production/image/data/43904/large_myImage.jpg?v=1572354856"
    ]
}
```

## Features
- Cloudflare bypass via cloudscraper
- Retry logic with exponential backoff (up to 5 attempts)
- Auto-save every 100 pages to prevent data loss
- Multilingual product name support
- Flexible configuration for automation and debugging

## Best Practices
- Keep page_size at or below 200 to comply with API limits.
- Use a delay of 1.0 seconds or more for large-scale scraping to avoid being blocked (you can try 0.5).