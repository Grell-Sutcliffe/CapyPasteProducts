from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from IPython.display import Image
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import logging

logging.basicConfig(level=logging.DEBUG)
# product = "F2J3NS1W"


def parse_by_name_vasko(product):
    try:
        options = Options()
        options.add_argument("--headless")
        driver = webdriver.Chrome(service=Service(
            ChromeDriverManager().install()), options=options)
        # открывается сайт и делается на весь экран (это важно, иначе нет окна поиска)
        driver.set_window_size(1920, 1080)

        driver.get("https://vasko.ru/#")

        search_field = driver.find_element(By.ID, "headerSearchInput")
        search_field.send_keys(product)
        # отправляет название товара в строку поиска
        search_field.send_keys(Keys.RETURN)

        # заглушка - если выдается несколько товаров по запросу выбирает первый
        first_tile = driver.find_element(By.CLASS_NAME, "catalog-tile__image")
        first_tile.click()

        # получаем название товара, цену, ссылку на его страницу и фотку
        product_name = driver.find_element(
            By.CLASS_NAME, 'product-detail__title')
        product_price = driver.find_element(
            By.CLASS_NAME, 'product-detail__price')
        product_image = driver.find_element(
            By.CLASS_NAME, 'product-images__detail-image').get_attribute("href")
        print(product_image)
        product_name_txt = product_name.text
        product_price_txt = product_price.text
        product_url_txt = str(driver.current_url)
        driver.save_screenshot("FKN_example_0.png")
        # закрывает окно парсера. ВАЖНО: не писать brower.close, иначе перестанет работать абсолютно весь сайт
        driver.quit()
        return [{'name': product_name_txt,
                 'price': product_price_txt,
                 'href': product_url_txt,
                 'pic': str(product_image)
                 }]
    except:
        try:
            driver.quit()
        except:
            logging.debug("Селениум поставь, умник")
        return []
