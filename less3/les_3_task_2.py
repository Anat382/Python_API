"""
2. Написать функцию, которая производит поиск и выводит на экран вакансии с заработной платой больше введённой суммы
(необходимо анализировать оба поля зарплаты). Для тех, кто выполнил задание с Росконтролем - напишите запрос для поиска
продуктов с рейтингом не ниже введенного или качеством не ниже введенного (то есть цифра вводится одна,
а запрос проверяет оба поля)
"""

from pymongo import MongoClient
from pprint import pprint


def jobs_salary(number):
    client = MongoClient('localhost', 27017)
    db = client['HH']
    collection_ = db.jobs
    for elem in collection_.find({'$and': [{'min_salary': {'$gt': number}}, {'max_salary': {'$gt': number}}]}):
        pprint(elem)


number = 100_000
jobs_salary(number)
