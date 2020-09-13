# Amazon_Web_Scraper

## Feature of the script

- Gets url of the website where products are displayed.
- Gets url of each individual product on the page.
- Extracts information(eg. product_id,url,seller,price) of each product.
- Stores the information of all products in a json file.

## Link to download chrome driver
Downlaod correct chrome driver after checking version of your chrome. 
### Steps to check chrome version
Settings -> About Chrome
(https://chromedriver.chromium.org/downloads).

After dowloading the zip file of the chromedriver extract it in the amazon_web_scrapper folder.

## Python Virtual Enviornment Setup
```
mkdir amazon_web_scrapper
cd amazon_web_scrapper
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
python simple_tracker.py
```
