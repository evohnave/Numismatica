# -*- coding: utf-8 -*-
"""
Created on Sat Jun  6 10:24:50 2020

@author: Cire
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd

base = 'https://www.tauleryfau.com/'

lot1img = 'img/thumbs/700/001/997/001-997-27_01.jpg'

all_coins = 'https://www.tauleryfau.com/en/auctions/all-categories?_token=iNfGYfH8AQgptPuIWd9rXpWeJCxvQ6ROnW1p9VZY&s=2141&order=ref&total=603&reference=&description='
all_no_token = 'https://www.tauleryfau.com/en/auctions/all-categories?s=2141&order=ref&total=603&reference=&description='


r = requests.get(all_no_token)

r.status_code

soup = BeautifulSoup(r.text, 'html.parser')

for form in soup.find_all('form'):
    try:
        if form['id'] == 'form_lotlist':
            print(form.attrs)
            print(len(form.find_all('section')))
            for section in form.find_all('section'):
                print(section['class'])
                for item in section['class']:
                    print(item)
#                if 'body-auctions' in section['class']:
#                    print(f"Here {section['class']}")
    except:
        pass


tyf = pd.DataFrame(columns=['Lot','link'])


for n, item in enumerate(soup.find_all('div')):
    try:
        if 'lot-large-block-content' in item['class']:
            print(item['class'])
            print(item.prettify())
            for link in item.find_all('a'):
                print(link.get('href'))
            break
            
    except:
        pass
