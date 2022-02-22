"""
2. Изучить список открытых API. Найти среди них любое, требующее авторизацию (любого типа).
Выполнить запросы к нему, пройдя авторизацию. Ответ сервера записать в файл.
"""

import json
import requests
import vk

access_token = ''
url = f"https://api.vk.com/method/friends.getOnline?v=5.131&access_token={access_token}"
v = '5.95'
repos = requests.get(url).json()
print('access_token', repos)

# Пример с бибоиотекой vk
session = vk.Session(access_token=access_token)
api = vk.API(session, v=v)

Cities = api.database.getCities(country_id=1, q=1)['items']
print('import vk', Cities)

with open(r'E:\Mail_ru geekbrains DATAINGENEER\Методы сбора и обработки данных из сети Интернет\_lesson\vk.json',
          'w', encoding='utf-8') as f:
    json.dump(repos, f)

with open(r'E:\Mail_ru geekbrains DATAINGENEER\Методы сбора и обработки данных из сети Интернет\_lesson\vk2.json',
          'w', encoding='utf-8') as f:
    json.dump(Cities, f)
