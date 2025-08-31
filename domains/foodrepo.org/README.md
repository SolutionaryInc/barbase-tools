# Parser for foodrepo.org

This parser collects product data from [foodrepo.org](https://www.foodrepo.org/en/products)
 and saves it in the format required by the Barbase project.

## Output format

The parser saves data in JSON format with the following structure:

```json
{
    "barcode": "string",
    "name": "string",
    "image_links": ["url_1", "url_2"]
}
```
## Installation & Usage
### 1. Requirements
- Python 3.9+
- Google Chrome browser

### 2. Install dependencies
If you don’t have a requirements.txt, install directly:
```bash
pip install selenium beautifulsoup4 webdriver-manager
```
### 3. Run the parser
#### Windows
```bash
python parser.py
```
#### macOS / Linux
```bash
python3 parser.py
```
### 4. Output

The parser will generate a file foodrepo.json in the same folder.

## How it works

- Uses Selenium to render product pages dynamically.

- Collects unique product links.

- Extracts: 
  - Product name
  - Product barcode
  - All image links

- If a barcode is missing, "Not found" is used.

## Notes

- No need to manually download ChromeDriver — it is automatically managed by webdriver-manager.

- Tested on Windows 10/11, Ubuntu Linux, and macOS Sonoma.