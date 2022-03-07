"""
1. Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB и реализовать функцию,
 которая будет добавлять только новые вакансии/продукты в вашу базу.

"""


import json
from bs4 import BeautifulSoup
import requests
from pprint import pprint
import base64
import pandas as pd
import re
import pretty_html_table
import os
import webbrowser
from time import perf_counter
from pymongo import MongoClient


client = MongoClient('localhost', 27017)

db = client['HH']
collection = db.jobs


def check_id(id: str, data):
    f_one = collection.find_one({'url_job_': {'$regex': id}})
    if not f_one:
        collection.insert_one(data)
    else:
        print('Элемент уже существует')



def connect_url(job):

    # headers = {r'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'}
    headers = {'User-Agent': 'Mozilla/5.0 (Widnows NT 5.1; rv:47.0) Gecko/20100101 FireFox/47.0',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
    base_url = r'https://hh.ru/'
    count_n = 0
    while True:
        url = f'{base_url}search/vacancy?text={job}&page={count_n}'
        numer = requests.get(url, headers=headers)
        print(count_n, numer.status_code)
        if numer.status_code != 200 or not BeautifulSoup(numer.text, 'html.parser'):
            print(f'По запросу «{job}» ничего не найдено, код {numer.status_code}')
            break
        elif count_n == 5:
            break
        count_n += 1
    print(count_n)

    for num in range(count_n):
        url = f'{base_url}search/vacancy?text={job}&page={num}'
        print(url)
        data_job = []
        try:
            response = requests.get(url, headers=headers)
            dom = BeautifulSoup(response.text, 'html.parser')
            # pprint(dom)
            articles = dom.find_all('div', {'class': 'vacancy-serp-item vacancy-serp-item_redesigned'})
            # print(articles)
            for n, art in enumerate(articles):
                data_json = {}

                job_url = art.find('a', {'class': 'bloko-link'})
                salary = art.find('div', {'class': 'bloko-v-spacing bloko-v-spacing_base-3'})
                company_url = art.find('a', {'class': 'bloko-link bloko-link_kind-tertiary'})
                data_ = art.find('span', {'class': 'bloko-text'})
                local = art.find('div', {'class': 'bloko-text bloko-text_no-top-indent'})

                url_job_ = job_url['href'] if job_url else None
                job_name = job_url.getText() if job_url else None
                get_salary = str(salary.previousSibling.getText()).replace('\u202f', '') if salary.previousSibling else None
                company_name = company_url.getText() if company_url else None
                company_url = company_url['href'] if company_url else None
                date_send = data_.getText() if data_ else None
                place_work = local.getText() if local else None

                salary_num = re.findall(r'\d+', get_salary)
                world_simb = re.compile(r'[а-я]\w+|[А-Я]\w+|[A-Z]\w+|[a-z]\w+')
                world = re.findall(world_simb, get_salary)
                currency = world[-1] if world and len(salary_num) >= 1 else None
                befor = 'от' if 'от' in world else None
                after = 'до' if 'до' in world else None
                data_json['page'] = num
                data_json['url_web'] = base_url
                data_json['url_job_'] = url_job_
                data_json['job_name'] = job_name
                data_json['min_salary'] = int(salary_num[0]) if len(salary_num) == 2 or (salary_num and befor) else 0
                data_json['max_salary'] = int(salary_num[-1]) if len(salary_num) == 2 or (salary_num and after) else 0
                data_json['currency'] = currency
                data_json['company_name'] = str(company_name).replace('\xa0', ' ') #  'ООО\xa0ХеленФуд',
                data_json['company_url'] = base_url + company_url if company_url else None
                data_json['date_send'] = date_send
                data_json['place_work'] = str(place_work).replace('\xa02\xa0', '').replace('\xa01\xa0', '')\
                    .replace('\xa03\xa0', '')
                id_job = re.findall(r"vacancy/(\d+)", str(url_job_))[0]
                print(id_job)
                check_id(id_job, data_json) if data_json else None
                print(num, url_job_, job_name, str(get_salary).encode('utf-8').decode('utf-8'), company_name,
                      company_url, date_send, place_work)

        except Exception as exp:
            print(exp, '\n', exp.args)


# Data Engineer
job = str(input('Введите профессию, должность, компанию: ').encode('UTF-8')).replace(r'\x','%')\
          .upper()[2:-1].replace(' ', '+')

start = perf_counter()
connect_url(job)
print(perf_counter() - start)

