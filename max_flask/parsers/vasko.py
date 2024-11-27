from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

# product = "F2J3NS1W"
def parse_by_name_vasko(product):

    driver = webdriver.Chrome()
    driver.set_window_size(1920,1080) # открывается сайт и делается на весь экран (это важно, иначе нет окна поиска)

    driver.get("https://vasko.ru/#")

    search_field = driver.find_element(By.ID, "headerSearchInput")
    search_field.send_keys(product)
    search_field.send_keys(Keys.RETURN) # отправляет название товара в строку поиска

    # заглушка - если выдается несколько товаров по запросу выбирает первый
    first_tile = driver.find_element(By.CLASS_NAME, "catalog-tile__image")
    first_tile.click()

    # получаем название товара, цену, ссылку на его страницу и фотку
    product_name = driver.find_element(By.CLASS_NAME, 'product-detail__title')
    product_price = driver.find_element(By.CLASS_NAME, 'product-detail__price')
    product_image = driver.find_element(By.CLASS_NAME, 'product-images__detail-image').get_attribute("href")
    print(product_image)
    product_name_txt = product_name.text
    product_price_txt = product_price.text
    product_url_txt = str(driver.current_url)

    # закрывает окно парсера. ВАЖНО: не писать brower.close, иначе перестанет работать абсолютно весь сайт
    driver.quit()


    return [{'name' : product_name_txt,
            'price' : product_price_txt,
            'href': product_url_txt,
            'pic': str(product_image)
             }]
