# Parser for foodrepo.org

This parser collects product data from [foodrepo.org](https://www.foodrepo.org) and outputs it in the format required by the Barbase project.

## Output format

The parser saves data in JSON format with the following structure:

```json
{
    "barcode": "string",
    "name": "string",
    "image_links": ["url_1", "url_2"]
}
```

## How to run
1. Make sure you have Python 3 installed.

2. Install required packages (if not already installed):

```bash

pip install selenium beautifulsoup4
```
3. Make sure ChromeDriver is installed and the path in parser.py is correct:

```python
service = Service("C:\\Program Files (x86)\\chromedriver-win64\\chromedriver.exe")
```
4. Run the parser:

```bash

python parser.py
```
5. The parser will generate a JSON file foodrepo.json in the same folder.

## Notes
The parser uses Selenium to load pages dynamically.

All product links are collected without duplicates.

Only products with a barcode are included; if barcode is not found, "Not found" is used.