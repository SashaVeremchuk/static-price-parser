import requests
from bs4 import BeautifulSoup
import pandas as pd
import gspread
import json
from pathlib import Path

from datetime import datetime

base_dir = Path.cwd()
cred_path = base_dir / 'secrets'/ 'cred.json'

gc = gspread.service_account(filename=str(cred_path))
wks = gc.open("web_parsing_report").sheet1

data = []
page = 1
max_page = 1

while page <= max_page:
    res = requests.get(f'https://ryvok.ru/instrumenty/shlifmashiny/?page={page}')
    soup = BeautifulSoup(res.text, 'html')

    elements = soup.find_all('div', class_='app-product-card app-product-card_with-horizontal')

    for e in elements:
        data.append({
            'titele': e.find('div', class_='app-product-card__title').text.strip(),
            'status': e.find('div', class_='app-product-card__status').text.strip(),
            'price ': e.find('div', class_='app-product-card__price').text.strip().replace('\xa0', '').replace(' ₽', ''),
        })
    
    pagination = soup.find('div', class_ = 'ui-pagination__numbers')
    
    pages = [p.text.strip() for p in pagination.find_all('div', class_ = 'ui-pagination__number')]
    int_pages = []
    
    for p in pages:
        try:
            n = int(p)
            int_pages.append(n)
        except:
            continue

    max_page = max(int_pages)
    page += 1


df = pd.DataFrame(data)
df['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

current_df = pd.DataFrame(wks.get_all_records())

merged_df = pd.concat([df, current_df])
res = wks.update([merged_df.columns.values.tolist()] + merged_df.values.tolist())

print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {json.dumps(res)}")