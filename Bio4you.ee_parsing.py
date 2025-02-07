from bs4 import BeautifulSoup
import requests
import os
import json
from datetime import datetime
import pandas as pd

# Страница, которую будем парсить

url = 'https://bio4you.eu/et/'

headers = {
    "Accept": "*/*",
    "User-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Safari/605.1.15"
}

main_links_from_index = set()

# Функция, которая парсит главную страницу

def scrape_categories_from_main_page(url, headers):
    req = requests.get(url, headers = headers)
    srq = req.text

    soup = BeautifulSoup(srq, 'lxml')

    links = soup.find_all('a', class_ = 'menu_item_title')

    for link in links:
        if 'HULGI' not in link.text:
            link_href = link.get('href')
            main_links_from_index.add(link_href)
            
    return(main_links_from_index)

scrape_categories_from_main_page(url, headers)

# Функция, которая парсит все подкатегории

file_path = 'C:/Users/igor/Desktop/Parsing Pet Project/bio4you.ee/all_categories_links.json'

def adding_all_categories_to_json(data):

    if not os.path.exists(file_path):
        with open (file_path, 'w') as new_file:
            json.dump([], new_file, indent = 4)

    with open (file_path, 'r') as categories_data:
        categories_data_info = json.load(categories_data)

    if data not in categories_data_info:
        categories_data_info.append(data)

        with open(file_path, 'w') as categories_data:
            json.dump(categories_data_info, categories_data, indent = 4)


def scrape_subcategories (url, headers):

    all_categories_links = []

    req = requests.get(url, headers = headers)
    srq = req.text

    soup = BeautifulSoup(srq, 'lxml')

    links = soup.find_all('li', class_ = 'cat_list_item')

    for li in links:
        a_tag = li.find('a')
        if a_tag:
            link = a_tag.get('href')
            all_categories_links.append(link)

    adding_all_categories_to_json(all_categories_links)
        


for link in main_links_from_index:
    scrape_subcategories(link, headers)

# Функция, которая парсит страницы пагинации
all_links = []
def scrape_categories_pagination(base_url, headers):

    current_url = base_url

    while current_url:
        response = requests.get(current_url, headers = headers)
        soup = BeautifulSoup(response.text, 'lxml')

        if current_url not in all_links:
            all_links.append(current_url)

        next_page = soup.find('nav', class_ = 'pagination')
        if next_page:
            next_link = next_page.find('a', rel = 'next')
            if next_link:
                next_url = next_page.get('href')
                if next_url and next_url not in all_links:
                    current_url = next_url
                else:
                    break
            else:
                break
        else:
            break


with open (file_path, 'r') as categories_data:
    categories_links = json.load(categories_data)

for links in categories_links:
    for link in links:
        scrape_categories_pagination(link, headers)

print(all_links)