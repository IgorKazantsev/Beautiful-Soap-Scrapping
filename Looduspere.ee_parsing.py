from bs4 import BeautifulSoup
import requests
import os
import json
from datetime import datetime
import pandas as pd

# Страница, которую будем парсить

url = "https://www.looduspere.ee/shop/"

headers = {
    "Accept": "*/*",
    "User-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Safari/605.1.15"
}

# Функция, которая парсит главную страницу

def scrape_categories_from_main_page(url, headers):
    
    req = requests.get(url, headers = headers)
    srq = req.text
    links_from_index = []
    soup = BeautifulSoup(srq, 'lxml')

    categories_container = soup.find(class_='toggle-product-cats nav')


    if categories_container: 
        all_categories_hrefs = categories_container.find('ul').find_all('a')

        for item in all_categories_hrefs:
            item_href = item.get('href')
            if item_href:
                links_from_index.append(item_href)

    with open('C:/Users/igor/Desktop/Parsing Pet Project/Looduspere.ee/links_from_index.json', 'w') as new_file:
        json.dump(links_from_index, new_file, indent = 4)

scrape_categories_from_main_page(url, headers)


# Функция для добавления ссылок категорий в json

file_path_1 = 'C:/Users/igor/Desktop/Parsing Pet Project/Looduspere.ee/all_categories_links_pagination.json'

def add_json_category_links(data):
    

    if not os.path.exists(file_path_1):
        with open(file_path_1, 'w') as new_file:
            json.dump([], new_file, indent = 4)

    with open(file_path_1, 'r') as product_data:
        product_data_info = json.load(product_data)

    if data not in product_data_info:
        product_data_info.append(data)

        with open(file_path_1, 'w') as product_data:
            json.dump(product_data_info, product_data, indent = 4)


# Достаем категории из главной страницы 

file_path_2 = 'C:/Users/igor/Desktop/Parsing Pet Project/Looduspere.ee/links_from_index.json'
with open(file_path_2, 'r') as file:
    main_categories = json.load(file)
    
# Достаем страницы пагинаций из категорий из главной страницы 
    
def get_all_pagination_links(base_url, headers):
    all_links = []
    current_url = base_url

    while current_url:
        response = requests.get(current_url, headers = headers)
        soup = BeautifulSoup(response.text, 'lxml')

        if current_url not in all_links:
            all_links.append(current_url)

   
        next_page = soup.find('a', class_='next page-numbers')
        if next_page:
            next_url = next_page.get('href')
            if next_url and next_url not in all_links:
                current_url = next_url
            else:
                break
        else:
            break

    add_json_category_links(all_links)   


for item in main_categories:
    get_all_pagination_links(item, headers)


file_path_3 = 'C:/Users/igor/Desktop/Parsing Pet Project/Looduspere.ee/all_products_links.json'

# Функция для парсинга всех ссылок на все товары

def get_product_links(link, headers):

    req = requests.get(link, headers)
    src = req.text
    soup = BeautifulSoup(src, 'lxml')

    product_container = soup.find_all('div', class_='mf-product-thumbnail')
    product_links = [product.find("a").get("href") for product in product_container if product.find("a")]


    if not os.path.exists(file_path_3):
        with open(file_path_3, 'w') as new_file:
            json.dump([], new_file, indent = 4)

    with open(file_path_3, 'r') as product_data:
        product_links_info = json.load(product_data)

    for link in product_links:
        if link not in product_links_info:
            product_links_info.append(link)

        with open(file_path_3, 'w') as product_data:
            json.dump(product_links_info, product_data, indent = 4)


with open(file_path_1, 'r') as file:
    all_categories_links = json.load(file)

    for categories in all_categories_links:
        for link in categories:
            get_product_links(link, headers)

# Составляем финальный словарь 

def get_product_data(link, headers):

    req = requests.get(link, headers)
    src = req.text
    soup = BeautifulSoup(src, 'lxml')

    data = {}

    data['Время обновления'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    product_link = link

    if product_link:
        data['Ссылка'] = product_link
    else:
        data['Ссылка'] = 'Ссылка не найдена!'

    product_name_tag = soup.find('h1')

    if product_name_tag:
        product_name = product_name_tag.text.strip()
        data['Название товара'] = product_name
    else:


        data['Название товара'] = 'Название товара не найдено!'


    price_container = soup.find('span', class_='woocommerce-Price-amount amount')

    if price_container:
        price_text = price_container.find('bdi').text.strip()
        data['Цена товара'] = price_text
    else:
        data['Цена товара'] = 'Цена не найдена!'



    product_category = soup.find_all('span', itemprop='name')

    if len(product_category) >= 2:
        data['Категория товара'] = product_category[-2].text.strip()
    else:
        data['Категория товара'] = 'Категория не найдена!'



    sku = soup.find('span', class_='sku')
    if sku:
        data['SKU'] = sku.text.strip()
    else:
        data['SKU'] = 'SKU не найден!'


    stock_info = soup.find('p', class_='stock in-stock')
    if stock_info:
        availability = stock_info.text.replace('Olek:', '').strip()
        data['Наличие на складе'] = availability
    else:
        data['Наличие на складе'] = 'Информация не найдена!'

    print(data)
    return(data)


file_path_4 = 'C:/Users/igor/Desktop/Parsing Pet Project/Looduspere.ee/final_dictionary.json'

# Проверка существующего файла и загрузка данных
if not os.path.exists(file_path_4):
    with open(file_path_4, 'w', encoding='utf-8') as new_file:
        json.dump([], new_file, indent=4, ensure_ascii=False)

with open(file_path_4, 'r', encoding='utf-8') as product_data:
    try:
        product_data_info = json.load(product_data)
    except json.JSONDecodeError:
        product_data_info = []

# Собираем данные о продуктах
with open(file_path_3, 'r') as file:
    all_products_links = json.load(file)

for product_link in all_products_links:
    data = get_product_data(product_link, headers)
    if data not in product_data_info:
        product_data_info.append(data)

# Записываем данные в файл один раз после цикла
with open(file_path_4, 'w', encoding='utf-8') as product_data:
    json.dump(product_data_info, product_data, indent=4, ensure_ascii=False)





with open(file_path_4, 'r', encoding = 'utf-8') as file:
    data = json.load(file)

df = pd.DataFrame(data)

df.rename(columns={
    'Название товара': 'product_name',
    'Цена товара': 'price',
    'Категория товара': 'category',
    'SKU': 'sku',
    'Наличие на складе': 'stock',
    'Ссылка': 'link'
}, inplace = True)

df = df[['product_name', 'price', 'category', 'sku', 'stock', 'link']]

output_path = 'C:/Users/igor/Desktop/Parsing Pet Project/Looduspere.ee/products_table.xlsx'

df.to_excel(output_path, index = False)

print(f'Таблица успешно создана: {output_path}')
