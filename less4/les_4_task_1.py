"""
1. Написать приложение, которое собирает основные новости с сайта на выбор news.mail.ru, lenta.ru, yandex-новости.
Для парсинга использовать XPath. Структура данных должна содержать:
название источника;
наименование новости;
ссылку на новость;
дата публикации.
Сложить собранные новости в БД

"""

from pymongo import MongoClient
from pprint import pprint
from lxml import html
import requests
import time
import re

client = MongoClient('localhost', 27017)

db = client['mail']
collection = db.news


def check_id(find_elem, id,  find_elem2: str, id2: str, data={}):

    print({'$and': [{find_elem: {'$regex': id}}, {find_elem2: {'$regex': id2}}]})
    f_one = collection.find_one({'$and': [{find_elem: {'$regex': id}}, {find_elem2: {'$regex': id2}}]})

    if not f_one:
        collection.insert_one(data)
    else:
        print('Элемент уже существует')

def request_to_yandex(url):
    try:
        response = requests.get(url, headers=header)
        root = html.fromstring(response.text)
        name_title = root.xpath("//span[contains(@class,'hdr__inner')]/text()")
        link_title = list(map(lambda el: ''.join([url, el]), root.xpath("//a[contains(@class,'hdr__text')]/@href")))
        main_body = root.xpath("//div[@class = 'cols__inner']")
        item_list = []
        for i, link in enumerate(main_body):
            response_news = requests.get(link_title[i], headers=header)
            news = html.fromstring(response_news.text)
            news_item = news.xpath("//div[contains(@class,'newsitem')]")
            for new in news_item:
                data_news = {}
                name_news = list(map(lambda el: str(el).replace('\xa0', ' '),
                                     new.xpath(".//span[contains(@class,'newsitem__title-inner')]/text()")))
                if name_news:
                    link_news = new.xpath(".//a[contains(@class,'newsitem__title')]/@href")
                    date_news = new.xpath(".//span[contains(@class,'newsitem__param')]/@datetime")
                    description_news = list(map(lambda el: str(el).replace('\xa0', ' '),
                                                new.xpath(".//span[contains(@class,'newsitem__text')]/text()")))
                    number_news = re.findall(r'\d+', link_news[0])

                    data_news['name_title'] = name_title[i]
                    data_news['link_title'] = link_title[i]
                    data_news['name_news'] = name_news[0]
                    data_news['link_news'] = link_news[0] if 'https' in link_news[0] else url + link_news[0]
                    data_news['number_news'] = number_news[0] if number_news else None
                    data_news['date_news'] = date_news[0] if date_news else None
                    data_news['description_news'] = description_news[0]

                    item_list.append(data_news)

                    if data_news['number_news'] and data_news['date_news']:
                        check_id('date_news', data_news['date_news'], 'number_news', data_news['number_news'], data_news)
                    elif data_news['name_news'] and data_news['date_news']:
                        check_id('date_news', data_news['date_news'], 'name_news', data_news['name_news'], data_news)

        pprint(item_list)

    except Exception as exp:
        print('Ошибка запроса', exp)


header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}

url = r'https://news.mail.ru/'

request_to_yandex(url)
