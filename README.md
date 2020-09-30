# Amazon_Web_Scraper

## Feature of the script

- Gets url of the website where products are displayed.
- Gets url of each individual product on the page.
- Extracts information(eg. product_id,url,seller,price) of each product.
- Stores the information of all products in a json file.

### Selenium Documentation- Python
https://selenium-python.readthedocs.io/api.html

## Link to download chrome driver
Downlaod correct chrome driver after checking version of your chrome. 
## Download chrome driver and check chrome version
[Chrome-driver](https://chromedriver.chromium.org/downloads)

chrome version: Settings-> About
## Installation Steps

#### make a folder
```
mkdir amazon_web_scrapper
cd amazon_web_scrapper
```

#### Setup a Virtual Enviornment
```
python3 -m venv venv
source venv/bin/activate
```
#### Install the requirements
```
pip install -r requirements.txt
```

#### Run the script
```
python simple_tracker.py
```
