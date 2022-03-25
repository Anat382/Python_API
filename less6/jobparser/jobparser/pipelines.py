# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient
import re


class JobparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.HH

    @staticmethod
    def str_x(string):
        return string.replace('\xa0', '').replace('\xa01', '').replace('\xa02', '').replace('\xa03', ''). \
            replace('\xa04', '').replace('\u202f', '')

    @staticmethod
    def currency_value(string):
        string = str(string).lower()
        if 'руб' in string:
            return 'руб'
        elif 'eur' in string:
            return 'eur'
        elif 'usd' in string:
            return 'usd'
        else:
            return None

    @staticmethod
    def salary_pars(dict_data):
        salary_extr = JobparserPipeline.str_x(' '.join(dict_data['salary']))
        salary_num = re.findall(r'\d+', salary_extr)
        currency_ = JobparserPipeline.currency_value(salary_extr)
        befor = 'от' if 'от' in salary_extr else None
        after = 'до' if 'до' in salary_extr else None
        dict_data['salary_min'] = int(salary_num[0]) if len(salary_num) == 2 or (salary_num and befor) else 0
        dict_data['salary_max'] = int(salary_num[-1]) if len(salary_num) == 2 or (salary_num and after) else 0
        dict_data['currency'] = currency_

    def process_item(self, item, spider):
        JobparserPipeline.salary_pars(item)
        collection = self.mongo_base[spider.name]
        collection.insert_one(item)

        return item
