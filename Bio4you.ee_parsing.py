from bs4 import BeautifulSoup
import requests
import os
import json
from datetime import datetime
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# Настройки Selenium
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Запуск без графического интерфейса (можно убрать для отладки)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


# Страница, которую будем парсить

url = 'https://bio4you.eu/et/'

headers = {
    "Accept": "*/*",
    "User-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Safari/605.1.15"
}
'''
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

file_path = 'C:/Users/igor/Desktop/Parsing Pet Project/Beautiful-Soap-Scrapping/bio4you.ee/all_categories_links.json'

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





file_path_2 = 'C:/Users/igor/Desktop/Parsing Pet Project/Beautiful-Soap-Scrapping/bio4you.ee/all_pagination_links.json'


def add_all_pagination_to_json(data):

    if not os.path.exists(file_path_2):
        with open (file_path_2, 'w') as new_file:
            json.dump([], new_file, indent = 4)

    with open (file_path_2, 'r') as categories_data:
        categories_data_info = json.load(categories_data)

    if data not in categories_data_info:
        categories_data_info.append(data)

        with open(file_path_2, 'w') as categories_data:
            json.dump(categories_data_info, categories_data, indent = 4)

# Функция для парсинга страниц категорий с динамической подгрузкой товаров
def scrape_categories_pagination(base_url):
    # Открываем страницу категории в браузере Selenium
    driver.get(base_url)

    # Цикл для нажатия на кнопку "Lae veel tooted" (Загрузить ещё товары)
    while True:
        try:
            # Ожидаем, пока кнопка станет кликабельной (максимум 5 секунд ожидания)
            load_more_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.ID, "vp_infinity_button"))
            )
            # Кликаем по кнопке, чтобы подгрузить дополнительные товары
            load_more_button.click()
            # Ждем 2 секунды, чтобы страница успела обновиться и загрузить новые товары
            time.sleep(2)  
        except:
            # Если кнопка больше не появляется, значит, все товары загружены
            print("Больше товаров не загружается на", base_url)
            break  # Выходим из цикла


    # Находим все ссылки на товары после полной загрузки страницы
    product_links = [elem.get_attribute("href") for elem in driver.find_elements(By.CSS_SELECTOR, ".thumbnail.product-thumbnail")]
    
    # Добавляем ссылки на товары в JSON-файл для дальнейшей обработки
    add_all_pagination_to_json(product_links)



# Читаем категории из JSON
with open(file_path, 'r') as categories_data:
    categories_links = json.load(categories_data)

# Собираем все ссылки на товары из каждой категории

for links in categories_links:
    for link in links:
        scrape_categories_pagination(link)

# Закрываем браузер
driver.quit()
'''

file_path_2 = 'C:/Users/igor/Desktop/Parsing Pet Project/Beautiful-Soap-Scrapping/bio4you.ee/all_pagination_links.json'

def get_product_data(link, headers):

    req = requests.get(link, headers)
    src = req.text
    soup = BeautifulSoup(src, 'lxml')

    data = {}

    time_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    data['Время обновления'] = time_now

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


    price_container = soup.find('span', class_ ='product-price')
    if price_container:
        price = price_container.text.strip()
        data['Цена товара'] = price
    else:
        data['Цена товара'] = 'Цена не найдена!'

    
    product_category_container = soup.find_all('span', itemprop='name')
    if len(product_category_container) >= 2:
        product_category = product_category_container[-2].text.strip()  # Предпоследний элемент - категория
        data['Категория товара'] = product_category
    else:
        data['Категория товара'] = 'Категория не найдена!'


    sku_container = soup.find('span', itemprop='sku')
    if sku_container:
        sku = sku_container.text.strip()
        data['SKU'] = sku
    else:
        data['SKU'] = 'SKU не найден!'

    
    stock_info_container = soup.find('span', class_ = 'vp_green')
    if stock_info_container:
        stock_info = stock_info_container.text.strip()
        data['Наличие на складе'] = stock_info
    else:
        data['Наличие на складе'] = 'Информация не найдена!'

    
    print(data)
    return(data)

file_path_3 = 'C:/Users/igor/Desktop/Parsing Pet Project/Beautiful-Soap-Scrapping/bio4you.ee/final_dictionary.json'

if not os.path.exists(file_path_3):
    with open(file_path_3, 'w', encoding='utf-8') as new_file:
        json.dump([], new_file, indent = 4, ensure_ascii = False)


with open(file_path_3, 'r', encoding = 'utf-8') as product_data:
    try:
        product_data_info = json.load(product_data)
    except json.JSONDecodeError:
        product_data_info = []


with open(file_path_2, 'r') as file:
    all_products_link = json.load(file)


for product_links in all_products_link:
    for link in product_links:
        data = get_product_data(link, headers=headers)
        if data not in product_data_info:
            product_data_info.append(data)


with open(file_path_3, 'w', encoding = 'utf-8') as product_data:
    json.dump(product_data_info, product_data, indent = 4, ensure_ascii = False)


# Создаем таблицу Excel

with open(file_path_3, 'r', encoding = 'utf-8') as file:
    data = json.load(file)

df = pd.DataFrame(data)

df.rename(columns = {
    'Время обновления': 'time_now',
    'Название товара': 'product_name',
    'Цена товара': 'price',
    'Категория товара': 'category',
    'SKU': 'sku',
    'Наличие на складе': 'stock_info',
    'Ссылка': 'link'
}, inplace = True)

df = df[['time_now', 'product_name', 'price', 'category', 'sku', 'stock_info', 'link']]

output_path = 'C:/Users/igor/Desktop/Parsing Pet Project/Beautiful-Soap-Scrapping/bio4you.ee/products_table.xlsx'

df.to_excel(output_path, index = False)

print(f'Таблица успешно создана: {output_path}')