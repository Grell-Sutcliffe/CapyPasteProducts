import requests
import json
from bs4 import BeautifulSoup
import logging
import re
import random
from time import sleep
from filter_bazhar import is_preposition
import string
import lxml

logging.basicConfig(level=logging.DEBUG)
logging.getLogger('pymorphy3').setLevel(logging.WARNING)


class Parser_Biggeek:
    def __init__(self):
        self.start_url = 'https://biggeek.ru'
        self.response = requests.get(self.start_url)
        self.initial_soup = BeautifulSoup(self.response.text, 'html.parser')
        self.all_products = []
        categories_wrapper = self.initial_soup.find(
            'ul', class_=['dropdown-header__list', 'category-dropdown-header'])
        self.category_lis = categories_wrapper.find_all('li', recursive=False)
        self.category_links = [
            self.start_url + category_li.find('a')['href'] for category_li in self.category_lis]

    @staticmethod
    def extract_price(text) -> int:
        match = re.search(r'\d[\d\s]*\d', text)
        if match:
            return int(match.group().replace(' ', ''))
        return -1

    @staticmethod
    def save_html(html_content, filename):
        """Сохраняет HTML-контент в файл."""
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(html_content)

    def get_paggination_num(self, url) -> int:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        try:
            paggination = soup.find('div', class_='prod-pagination')
            pagginations = paggination.find_all(
                'a', class_='prod-pagination__item')
            return int(pagginations[-1].text)
        except (IndexError, AttributeError):
            return 1

    def parse_category(self, url) -> None:
        logging.debug(f'Parsing category {url}')
        num = self.get_paggination_num(url)
        for i in range(1, num + 1):
            logging.debug("Page url: " + url + f'?page={i}')
            self.parse_page(url + f'?page={i}')
            logging.debug(f'Parsed page {i} of {num}')
            sleep(0.2 + random.randint(1, 100) / 100)

    def parse_page(self, url) -> None:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        products = soup.find(
            'div', class_='catalog-content__prods-list').find_all('div', class_='catalog-card')
        for product in products:
            try:
                product_price = product.find(
                    'div', class_='catalog-card__price-row').find('b', class_='cart-modal-count').text
                product_price = self.extract_price(product_price)
                product_temp = product.find(
                    'a', class_='catalog-card__title cart-modal-title')
                product_name = product_temp.text
                product_href = self.start_url + product_temp['href']
                product_img = product.find(
                    'img', class_='cart-modal-image')['src']
                product_data = {
                    'name': product_name,
                    'price': product_price,
                    'href': product_href,
                    'pic': product_img,
                    'set_words': list(set([word.lower().strip(string.punctuation + "«»‘’“”") for word in product_name.split() if not is_preposition(word)]))
                }

                self.all_products.append(product_data)
            except Exception as e:
                logging.error(f'Error parsing product: {e}')
                continue

            logging.debug(
                f'Parsed {product_data["name"]}, link: {product_data["href"]}')

    def parse(self):
        for category in self.category_links:
            self.parse_category(category)
        self.put_to_json()

    def put_to_json(self):
        with open('biggeek.json', 'w') as file:
            json.dump(self.all_products, file)


def main():
    parser = Parser_Biggeek()
    parser.parse_category('https://biggeek.ru/catalog/apple')
    parser.put_to_json()


if __name__ == '__main__':
    main()
