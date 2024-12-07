import pytest
from parser_technodeus import Parser_Technodeus
import requests
import random
from time import sleep


def random_sleep():
    sleep(0.2 + random.randint(1, 100) / 100)


@pytest.fixture(scope='module')
def parser():
    return Parser_Technodeus()


@pytest.mark.parametrize("price, expected", [
    ('1 000 руб', 1000),
    ('1 000 руб.', 1000),
    ('1 000', 1000),
    ('1 000.', 1000),
    ('1 000.000', 1000),
    ('1 000.000000000000000000000', 1000)
])
def test_extract_price_zeros(parser: Parser_Technodeus, price: str, expected: int):
    assert parser.extract_price(price) == expected


@pytest.mark.parametrize("price, expected", [
    ("Fisting is 300 руб", 300),
    ("Цена: 100500 руб", 100500),
    ("от рублей 152 300", 152300),
    ("От 1000000 руб", 1000000),
    ("от 163 990 ₽", 163990)
])
def test_extract_price_text(parser: Parser_Technodeus, price: str, expected: int):
    assert parser.extract_price(price) == expected


@pytest.mark.parametrize("price, expected", [
    ("", -1),
    ("Fisting is asdasd", -1),
    ("Цена: asdasd", -1),
    ("от рублей asdasd", -1),
    ("От asdasd руб", -1),
    ("от asdasd ₽", -1)
])
def test_extract_price_fail(parser: Parser_Technodeus, price: str, expected: int):
    assert parser.extract_price(price) == expected


def test_get_categories_count(parser: Parser_Technodeus):
    assert len(parser.category_links) == 17


def test_get_categories(parser: Parser_Technodeus):
    random_category = random.choice(parser.category_links)
    random_sleep()
    response = requests.get(random_category)

    assert response.status_code == 200


def test_get_pagination_right(parser: Parser_Technodeus):
    random_sleep()
    assert parser.get_paggination_num(
        parser.category_links[0]) == 77  # Может измениться


def test_get_no_pagination(parser: Parser_Technodeus):
    random_sleep
    assert parser.get_paggination_num(
        "https://technodeus.ru/collection/iphone-16-pro-max") == 1
