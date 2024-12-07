import requests
import json
from bs4 import BeautifulSoup
import logging
import re
import random
from time import sleep

logging.basicConfig(level=logging.DEBUG)


class Parser_Technodeus:

    def __init__(self):
        self.start_url = 'https://technodeus.ru'
        self.response = requests.get(self.start_url)
        self.initial_soup = BeautifulSoup(self.response.text, 'html.parser')
        self.all_products = []
        self.category_divs = self.initial_soup.find(
            'div', class_='list-item-subs-wrapper').find_all('div', class_='list-item-part', recursive=False)
        self.category_links = [self.start_url + category_div.find('a')['href']
                               for category_div in self.category_divs[2:]]  # 2: - skip first two categories, they are not needed

    @staticmethod
    def extract_price(text) -> int:
        match = re.search(r'\d[\d\s]*\d', text)
        if match:
            return int(match.group().replace(' ', ''))
        return -1

    def get_paggination_num(self, url) -> int:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        try:
            paggination = soup.find('ul', class_='pagination')
            pagginations = paggination.find_all('a')
            return int(pagginations[-1].text)
        except (IndexError, AttributeError):
            return 1

    def parse_category(self, url) -> None:
        logging.debug(f'Parsing category {url}')
        num = self.get_paggination_num(url)
        print(url)
        print(f'num: {num}')
        for i in range(1, num + 1):
            logging.debug("Page url: " + url + f'?page={i}')
            self.parse_page(url + f'?page={i}')
            logging.debug(f'Parsed page {i} of {num}')
            sleep(0.2 + random.randint(1, 100) / 100)

    def parse_page(self, url) -> None:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        products = soup.find_all('div', class_='product_card-cell')
        for product in products:
            text_link_slot = product.find(
                'figcaption', class_='info-wrap pt-2')

            product_name = text_link_slot.find('a', class_='title').text
            product_price = self.extract_price(
                product.find('var', class_='price').text)
            product_href = self.start_url + text_link_slot.find('a')['href']
            product_pic = product.find('img')['data-src']
            logging.debug(product.find('img'))
            product_data = {
                'name': product_name,
                'price': product_price,
                'href': product_href,
                'pic': product_pic
            }

            self.all_products.append(product_data)

            logging.debug(
                f'Parsed {product_data["name"]}, link: {product_data["href"]}')

    def parse(self):
        for category in self.category_links:
            self.parse_category(category)
        self.put_to_json()

    def put_to_json(self):
        with open('technodeus.json', 'w') as file:
            json.dump(self.all_products, file)


def main():
    parser = Parser_Technodeus()
    parser.parse_category('https://technodeus.ru/collection/katalog-07f35e')
    parser.put_to_json()
    # parser = Parser_Technodeus()
    # parser.parse()


if __name__ == '__main__':
    main()
