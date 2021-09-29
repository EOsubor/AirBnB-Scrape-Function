# Import necessary packages
#pip install selenium
#pip install pandas

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
#from selenium.webdriver import ActionChains

import time

import pandas as pd
import csv

AIRBNB_LINK_1 = 'https://www.airbnb.co.uk/rooms/33090114?source_impression_id=p3_1632322518_zv%2FqxckI7Ri8mMRE&check_in=2021-09-26&guests=1&adults=1&check_out=2021-09-27'
AIRBNB_LINK_2 = 'https://www.airbnb.co.uk/rooms/50633275?source_impression_id=p3_1632394330_rzA6oBfAM9a6YfNE&check_in=2021-11-01&guests=1&adults=1&check_out=2021-11-03'


def create_amenities_url(link_href):
    url = 'https://www.airbnb.co.uk'
    
    wd = webdriver.Chrome()

    try:
        wd.get(link_href)
    except:
        print(f"Invalid URL: {link_href}")
        return BeautifulSoup('', features='html.parser')
    

    time.sleep(5)

    page = wd.page_source

    wd.quit()

    soup = BeautifulSoup(page, features='html.parser')

    url_append = soup.find('a', 'b1sec48q v7aged4 dir dir-ltr').get('href')

    return url + url_append


def extract_amenities(listing):
    "Extract amenities from link"

    amenities_url = create_amenities_url(listing)

    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--blink-settings=imagesEnabled=false')
    chrome_options.add_argument("window-size=1200x600")
    chrome_options.add_argument('--no-sandbox')

    wd = webdriver.Chrome(options=chrome_options)

    try:
        wd.get(amenities_url)
    except:
        print(f"Invalid URL: {amenities_url}")
        return BeautifulSoup('', features='html.parser')
    

    time.sleep(5)

    page = wd.page_source

    wd.quit()

    soup = BeautifulSoup(page, features='html.parser')

    amenities = [x.get_text() for x in soup.find_all('div', '_gw4xx4')]

    return amenities


def extract_soup_js(listing_url):
    """Extracts HTML from JS(Dynamic) pages"""

    link_info = {}
    # Chrome options to speed up page loading and increase viewport
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--blink-settings=imagesEnabled=false')
    chrome_options.add_argument("window-size=1200x600")
    chrome_options.add_argument('--no-sandbox')


    wd = webdriver.Chrome(options=chrome_options)

    # if the URL is not valid - return an empty soup
    try:
        wd.get(listing_url)
    except:
        print(f"Invalid URL: {listing_url}")
        return BeautifulSoup('', features='html.parser')
    

    # Wait for page to load before scraping
    time.sleep(5)

    # Extract page html
    page = wd.page_source

    wd.quit()

    # Create soup object from extracted page source
    soup = BeautifulSoup(page, features='html.parser')

    # looking for listing details
    
    link_info['price_per_night'] = soup.find('span', '_tyxjp1').get_text()
    link_info['price_total'] = soup.find('span', '_1k4xcdh').get_text()
    link_info['name'] = soup.find('span', '_1n81at5').get_text()
    link_info['name_alt'] = soup.find('div', '_tqmy57').get_text().split(',')[0]
    link_info['bedrooms'] = soup.find('div', '_tqmy57').get_text().split(',')[2].strip()
    link_info['bathrooms'] = soup.find('div', '_tqmy57').get_text().split(',')[1].strip()
    link_info['amenities'] = extract_amenities(listing_url)
    link_info['home_type'] = soup.find('div', '_1qsawv5').get_text()

    return link_info


def write_file(airbnb_dict):
    """Write dictionary to csv file"""

    # Extract column names 
    cols = list(airbnb_dict.keys())

    with open('airbnb_file.csv', mode='w') as csv_file:
        fieldnames = cols
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerow(airbnb_dict)



if __name__ == "__main__":
    scraped_dict = extract_soup_js(AIRBNB_LINK_1)
    df = write_file(scraped_dict, optn='pd')
