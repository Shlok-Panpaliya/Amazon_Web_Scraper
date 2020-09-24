from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import json
from datetime import datetime
from amazon_config import(
    get_chrome_web_driver,
    get_web_driver_options,
    set_ignore_certificate_error,
    set_browser_as_incognito,
    NAME,
    DIRECTORY,
    CURRENCY,
    FILTERS,
    BASE_URL
)
#Make it UI enabled by asking name of product,price range
#implement code to show only products within entered price range
#Check if product is in stock
#Make it read multiple pages according to number of product user wants to see.

class AmazonAPI:
    def __init__(self,search_term,filters,base_url,currency):
        options = get_web_driver_options()
        set_ignore_certificate_error(options)
        set_browser_as_incognito(options)
        self.search_term = search_term
        self.base_url = base_url
        self.driver = get_chrome_web_driver(options)
        self.currency = currency
        self.price_filter = f"&rh=p_36%3A{filters['min']}00-{filters['max']}00"


    def run_script(self):
        print("Script started executing")
        print(f"name of product is {self.search_term}")
        links = self.get_products_links()
        if not links:
            print("Stopped script.")
            return
        print(f"Got {len(links)} links to products...")
        print("Getting info about products...")
        products = self.get_products_info(links)
        print(f"Got info about {len(products)} products...")
        self.driver.quit()
        return products

    def get_products_info(self,links):
        asins = self.get_asins(links)
        products = []
        for asin in asins: 
            product = self.get_single_product_info(asin)   #loops through all producst on the page
            if product:
                products.append(product)
        return products

    def get_single_product_info(self,asin):
        print(f"Product ID : {asin} getting data")   
        product_short_url = self.base_url + 'dp/' + asin   #taking only ID as product name can change but ID will be same          
        self.driver.get(f'{product_short_url}?language=en_GB')   #Change German launguage to English
        title = self.get_title()
        seller = self.get_seller()
        price = self.get_price()
        
        if title and seller and price:
            product_info = {
                'asin' : asin,
                'url' : product_short_url,
                'title' : title,
                'seller' : seller,
                'price' : price
            }
            return product_info
        return None
    
    def get_title(self):
        try:
            return self.driver.find_element_by_id('productTitle').text
        except Exception as e:
            print(e)
            print(f"Can't get title of a product - {self.driver.current_url}")
            return None

    def get_seller(self):
        try:
            return self.driver.find_element_by_id('bylineInfo').text
        except Exception as e:
            print(e)
            print(f"Can't get seller of a product - {self.driver.current_url}")
            return None

    def get_price(self):
        price = None
        try:
            price = self.driver.find_element_by_id('priceblock_ourprice').text   #get price by inspecting the element in stock
            price = self.convert_price(price)
        except NoSuchElementException:
            try:
                availability = self.driver.find_element_by_id('availability').text   #if it is out of stock then price is displayed in other element
                if 'Available' in availability:
                    price = self.driver.find_element_by_class_name('olp-padding-right').text
                    price = price[price.find(self.currency):]
                    price = self.convert_price(price)  # converting price from string to float as required
            except Exception as e:
                print(e)
                print(f"Can't get price of a product - {self.driver.current_url}")
                return None
        except Exception as e:
            print(e)
            print(f"Can't get price of a product - {self.driver.current_url}")
            return None
        return price

    def convert_price(self,price):
        price = price.split(self.currency)[1]
        try:
            price = price.split("\n")[0] + "." + price.split("\n")[1]
        except:
            Exception()
        try:
            price = price.split(",")[0] + price.split(",")[1]
        except:
            Exception()
        return float(price)
    
    
   
    
    def get_asins(self,links):
        return [self.get_asin(link) for link in links]

    def get_asin(self,product_link):
        return product_link[product_link.find('/dp/') + 4:product_link.find('/ref')]  #taking only the product_id in the url of the product

    def get_products_links(self):
        self.driver.get(self.base_url)
        element = self.driver.find_element_by_id("twotabsearchtextbox")  # Grabbing search Box
        element.send_keys(self.search_term)     #Inserting our product name in search box
        element.send_keys(Keys.ENTER)           # Hitting Enter button in search box
        
        self.driver.get(f"{self.driver.current_url}{self.price_filter}")  #clears the url
        result_list = self.driver.find_elements_by_class_name("s-result-list")  #gets all products on the page

        links = []
        try:
            results = result_list[0].find_elements_by_xpath(
                "//div/span/div/div/div[2]/div[2]/div/div[1]/div/div/div[1]/h2/a")   #loops through each item in result_list and stores all info in div
            links = [link.get_attribute('href') for link in results]    #loops through results and stores the href i.e link of each product on page
            return links
        except Exception as e:
            print("Didn't get any products...")
            print(e)
            return links

       # products = get_products_info(self,links)
        self.driver.quit()

class GenerateReport:   # creating JSON file where data of each prodict is stored
    def __init__(self, file_name, filters, base_link, currency, data):
        self.data = data
        self.file_name = file_name
        self.filters = filters
        self.base_link = base_link
        self.currency = currency
        report = {
            'title': self.file_name,
            'date': self.get_now(),
            'best_item': self.get_best_item(),
            'currency': self.currency,
            'filters': self.filters,
            'base_link': self.base_link,
            'products': self.data
        }
        print("Creating report...")
        with open(f'{DIRECTORY}/{file_name}.json', 'w') as f: 
            json.dump(report, f)
        print("Done...")


    def get_now(self):
        now = datetime.now()
        return now.strftime("%d/%m/%Y %H:%M:%S")

    def get_best_item(self):
        try:
            return sorted(self.data, key=lambda k: k['price'])[0]  #sort data by price 
        except Exception as e:
            print(e)
            print("Problem with sorting items")
            return None

if __name__ == "__main__":
    print("Started")
    amazon = AmazonAPI(NAME,FILTERS,BASE_URL,CURRENCY)
    data = amazon.run_script()  
    GenerateReport(NAME, FILTERS, BASE_URL, CURRENCY, data)
    
