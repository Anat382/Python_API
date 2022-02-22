"""
1. Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев для
конкретного пользователя, сохранить JSON-вывод в файле *.json.
"""

import json
import requests

username = 'Anat382'
url = f"https://api.github.com/users/{username}/repos"
repos = requests.get(url).json()
print(repos)

with open(r'repos.json',
          'w', encoding='utf-8') as f:
    json.dump(repos, f)
