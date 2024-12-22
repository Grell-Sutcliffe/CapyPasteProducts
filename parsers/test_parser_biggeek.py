import pytest
import requests
from unittest.mock import patch, Mock
from bs4 import BeautifulSoup
from parser_biggeek import Parser_Biggeek
import json


@pytest.fixture
def parser():
    with patch('requests.get') as mock_get:
        mock_response = Mock()
        mock_response.text = '<html><ul class="dropdown-header__list"><li><a href="/catalog/apple">Apple</a></li></ul></html>'
        mock_get.return_value = mock_response
        return Parser_Biggeek()


def test_extract_price():
    assert Parser_Biggeek.extract_price('1 234 руб.') == 1234
    assert Parser_Biggeek.extract_price('Цена: 56 789 руб.') == 56789
    assert Parser_Biggeek.extract_price('No price') == -1


def test_save_html(tmp_path):
    html_content = '<html></html>'
    filename = tmp_path / 'test.html'
    Parser_Biggeek.save_html(html_content, filename)
    with open(filename, 'r', encoding='utf-8') as file:
        assert file.read() == html_content


def test_get_paggination_num(parser):
    with patch('requests.get') as mock_get:
        mock_response = Mock()
        mock_response.text = '<html><div class="prod-pagination"><a class="prod-pagination__item">1</a><a class="prod-pagination__item">2</a></div></html>'
        mock_get.return_value = mock_response
        assert parser.get_paggination_num(
            'https://biggeek.ru/catalog/apple') == 2


def test_parse_category(parser):
    with patch.object(parser, 'get_paggination_num', return_value=2):
        with patch.object(parser, 'parse_page') as mock_parse_page:
            parser.parse_category('https://biggeek.ru/catalog/apple')
            assert mock_parse_page.call_count == 2


def test_parse_page(parser):
    with patch('requests.get') as mock_get:
        mock_response = Mock()
        mock_response.text = '''
        <html>
            <div class="catalog-content__prods-list">
                <div class="catalog-card">
                    <div class="catalog-card__price-row">
                        <b class="cart-modal-count">1 234 руб.</b>
                    </div>
                    <a class="catalog-card__title cart-modal-title" href="/product/1">Product 1</a>
                    <img class="cart-modal-image" src="image1.jpg"/>
                </div>
            </div>
        </html>
        '''
        mock_get.return_value = mock_response
        parser.parse_page('https://biggeek.ru/catalog/apple?page=1')
        assert len(parser.all_products) == 1
        assert parser.all_products[0]['name'] == 'Product 1'
        assert parser.all_products[0]['price'] == 1234
        assert parser.all_products[0]['href'] == 'https://biggeek.ru/product/1'
        assert parser.all_products[0]['pic'] == 'image1.jpg'


def test_put_to_json(parser, tmp_path):
    parser.all_products = [{'name': 'Product 1', 'price': 1234,
                            'href': 'https://biggeek.ru/product/1', 'pic': 'image1.jpg'}]
    filename = tmp_path / 'biggeek.json'
    parser.put_to_json()
    with open('biggeek.json', 'r') as file:
        data = json.load(file)
        assert data == parser.all_products
