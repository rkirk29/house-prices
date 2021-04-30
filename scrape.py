from bs4 import BeautifulSoup
import requests
import json
import time
import random
#import numpy as np
#import pandas as pd


headers = ({'User-Agent':
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.37'})
rows = []
house_urls = set()
total_pages = 0
#set min price, sort lowest first, go through all 400, -> set min price at around 400 page, go through all 400 ->s 

min_prices = ["50000", "300000", "350000", "400000", "450000", "500000", "550000", "600000", "650000", "750000", "900000", "1300000", "4250000"]
#min_prices = ["50000", "300000"]

for min_price in min_prices :

    for page in range(0,401):
        total_pages += 1
 

        #search_url = "https://www.zoopla.co.uk/for-sale/property/london/brixton/?include_sold=true&is_auction=false&is_retirement_home=false&is_shared_ownership=false&page_size=25&q=Brixton%2C%20London&radius=1&results_sort=newest_listings&search_source=refine" + "&pn" + str(page)
        #search_url = "https://www.zoopla.co.uk/for-sale/property/london/?include_sold=true&is_auction=false&is_retirement_home=false&is_shared_ownership=false&page_size=25&q=London&radius=0&results_sort=newest_listings&search_source=refine" + "&pn" + str(page)
        search_url = f"https://www.zoopla.co.uk/for-sale/property/london/?include_sold=true&is_auction=false&is_retirement_home=false&is_shared_ownership=false&price_min={min_price}&q=London&radius=0&results_sort=lowest_price&search_source=facets" + "&pn" + str(page)

        response = requests.get(search_url, headers=headers)
        #response = requests.get(search_url, headers={'User-Agent': 'Mozilla/5.0'})
        search_html = BeautifulSoup(response.text, 'html5lib')

        search_house_containers = search_html.find_all('div', class_='earci3d1 css-tk5q7b-Wrapper-ListingCard-StyledListingCard e2uk8e10')

        time.sleep(random.randint(1, 4))

        if search_house_containers != []:
            for container in search_house_containers:
                url_suffix = container.a['href'].split('?')[0]
                if len(url_suffix) == 27:
                    house_urls.update(["https://www.zoopla.co.uk" + url_suffix])
        else:
            print("No Houses on page")
            
        #print("house urls = " + house_urls)

for house_url in house_urls:
    
    try:
        house_response = requests.get(house_url, headers=headers)
        house_html = BeautifulSoup(house_response.text, 'html5lib')
        house_details = house_html.find('script', id='__NEXT_DATA__')

        details_dict = json.loads(house_details.text)

        specific_info = details_dict['props']['initialProps']['pageProps']['data']['listing']['adTargeting']

        rows.append(specific_info)

        time.sleep(random.randint(1, 3))
        #print("Next house")
    except:
        print("error on this one " + house_url)

# print("Next Page, finished page " + str(n_page))
# print(str(count) + " Houses on that page")



print('You scraped {} pages containing {} properties.'.format(total_pages, len(rows)))