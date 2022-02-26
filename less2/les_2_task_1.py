"""
1. Необходимо собрать информацию о вакансиях на вводимую должность
 (используем input или через аргументы получаем должность) с сайтов HH(обязательно) и/или Superjob(по желанию).
 Приложение должно анализировать несколько страниц сайта (также вводим через input или аргументы).
 Получившийся список должен содержать в себе минимум:
Наименование вакансии.
Предлагаемую зарплату (разносим в три поля: минимальная и максимальная и валюта. цифры преобразуем к цифрам).
Ссылку на саму вакансию.
Сайт, откуда собрана вакансия.
По желанию можно добавить ещё параметры вакансии (например, работодателя и расположение).
Структура должна быть одинаковая для вакансий с обоих сайтов.
Общий результат можно вывести с помощью dataFrame через pandas. Сохраните в json либо csv
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


def connect_url(job, count_page=0):

    # headers = {r'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'}
    headers = {'User-Agent': 'Mozilla/5.0 (Widnows NT 5.1; rv:47.0) Gecko/20100101 FireFox/47.0',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
    base_url = r'https://hh.ru/'
    url = f'{base_url}search/vacancy?text={job}&page={str(count_page)}'
    print(url)
    data_job = []
    try:
        response = requests.get(url, headers=headers)
        # print(response.status_code)
        if response.status_code == 404:
            raise BaseException(f'Ошибка подключения 404')
        dom = BeautifulSoup(response.text, 'html.parser')
        # pprint(dom)
        articles = dom.find_all('div', {'class': 'vacancy-serp-item'})
        # print(articles)
        for art in articles:
            data_json = {}

            job_url = art.find('a', {'class': 'bloko-link'})
            salary = art.find('div', {'class': 'bloko-v-spacing bloko-v-spacing_base-3'})
            company_url = art.find('a', {'class': 'bloko-link bloko-link_kind-tertiary'})
            data_ = art.find('span', {'class': 'bloko-text'})
            local = art.find('div', {'class': 'bloko-text bloko-text_no-top-indent'})

            url_job_ = job_url['href'] if job_url else None
            job_name = job_url.getText() if job_url else None
            get_salary = salary.previousSibling.getText()  if salary.previousSibling else None
            company_name = company_url.getText() if company_url else None
            company_url = company_url['href'] if company_url else None
            date_send = data_.getText() if data_ else None
            place_work = local.getText() if local else None

            data_json['page'] = count_page
            data_json['url_web'] = base_url
            data_json['url_job_'] = url_job_
            data_json['job_name'] = job_name
            data_json['get_salary'] = get_salary
            data_json['company_name'] = company_name
            data_json['company_url'] = base_url + company_url if company_url else None
            data_json['date_send'] = date_send
            data_json['place_work'] = place_work
            data_job.append(data_json)

            # print(url_job_, job_name, str(get_salary).encode('utf-8').decode('utf-8'), company_name, company_url, date_send, place_work)
            # print(job_url['href'], job_url.getText(), salary.previousSibling.getText(), company_url.getText(), company_url['href']) # company_url['href']

            # print(data_json)
        df = pd.json_normalize(data_job)
        return df

    except Exception as exp:
        print(exp, '\n', response.status_code)

# Программист
job = str(input('Введите профессию, должность, компанию: ').encode('UTF-8')).replace(r'\x','%').upper()[2:-1]


df = pd.DataFrame()
count_n = 0
while True:
    if count_n == 5:
        break
    else:
        df = df.append(connect_url(job, count_n))

    count_n += 1
# df.to_html(encodin='utf-8')
html_res = pretty_html_table.build_table(df, 'blue_light')


path = 'hh.json'
with open(path, 'w', encoding='utf-8') as f:
    json.dump(df.to_json(orient="split"), f)


path = 'temp.html'
with open(path, 'w', encoding='utf-8') as f:
    f.write(str(html_res))
webbrowser.open(path)

