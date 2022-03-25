"""
1. Написать программу, которая собирает входящие письма из своего или тестового почтового ящика и сложить
данные о письмах в базу данных (от кого, дата отправки, тема письма, текст письма полный)
Логин тестового ящика: study.ai_172@mail.ru
Пароль тестового ящика: NextPassword172#

"""

from pymongo import MongoClient
from pprint import pprint
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import exceptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import re

client = MongoClient('localhost', 27017)
db = client['mail']
collection = db.letter

def check_id(find_elem, id, find_elem2: str, id2: str, data={}):
    pass
    print({'$and': [{find_elem: {'$regex': id}}, {find_elem2: {'$regex': id2}}]})
    f_one = collection.find_one({'$and': [{find_elem: {'$regex': id}}, {find_elem2: {'$regex': id2}}]})

    if not f_one:
        collection.insert_one(data)
        print('ок')
    else:
        print('Элемент уже существует')


chrome_options = Options()
chrome_options.add_argument("start-maximized")

service = Service("C:/Users/User/chromedriver")
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.get('https://account.mail.ru/')

driver.implicitly_wait(10)
# wait = WebDriverWait(driver, 30)

elem = driver.find_element(By.NAME, 'username')
elem.send_keys("study.ai_172@mail.ru")

# button = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'base-0-2-87 primary-0-2-101 auto-0-2-113')))
button = driver.find_element(By.TAG_NAME, 'button')
button.click()

elem = driver.find_element(By.XPATH, "//input[contains(@name,'password')]")
elem.send_keys("NextPassword172#")
elem.send_keys(Keys.ENTER)

driver.implicitly_wait(30)


messege = []
for i in range(1):
    try:
        articles = driver.find_elements(By.XPATH, "//a[contains(@class,'llc')]")
        for el in articles:
            massege_option = {}
            massege_option['NameSender'] = el.find_element(By.XPATH, ".//span[contains(@class,'ll-crpt')]").text
            massege_option['EmailSender'] = el.find_element(By.XPATH, ".//span[contains(@class,'ll-crpt')]").get_attribute('title')
            massege_option['Desciption'] = el.find_element(By.XPATH, ".//span[contains(@class,'ll-sj__normal')]").text
            massege_option['Time'] = el.find_element(By.XPATH, ".//div[contains(@class,'llc__item_date')]").text
            massege_option['link'] = el.get_attribute('href')

            print(massege_option)
            messege.append(massege_option)
        actions = ActionChains(driver)
        actions.move_to_element(articles[-1])
        actions.perform()
        time.sleep(4)
    except exceptions.TimeoutException:
        break

pprint(messege)

for elem in messege:
    letter = {}
    driver.get(elem['link'])
    driver.implicitly_wait(30)
    letter['NameSender'] = elem['NameSender']
    email = re.findall(r"<(\S+)+[>$]", elem['EmailSender'])
    letter['EmailSender'] = email[0] if email else elem['EmailSender']
    letter['Desciption'] = elem['Desciption']
    letter['Time'] = elem['Time']
    letter['link'] = elem['link']
    # link_number = re.findall("0:(\d+)", elem['link'])[0]
    letter['link_number'] = re.findall("0:(\d+)", elem['link'])[0]
    letter['Text'] = driver.find_element(By.XPATH, "//div[contains(@class,'letter__body')]").text
    # pprint(letter)

    check_id('EmailSender', letter['EmailSender'], 'link_number', letter['link_number'], letter)
driver.close()



