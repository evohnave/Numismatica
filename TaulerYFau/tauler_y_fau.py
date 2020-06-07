# -*- coding: utf-8 -*-
"""
Created on Sat Jun  6 10:24:50 2020

@author: Cire
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

base = 'https://www.tauleryfau.com/'

lot1img = 'img/thumbs/700/001/997/001-997-27_01.jpg'

all_coins = 'https://www.tauleryfau.com/en/auctions/all-categories?_token=iNfGYfH8AQgptPuIWd9rXpWeJCxvQ6ROnW1p9VZY&s=2141&order=ref&total=603&reference=&description='
all_no_token = 'https://www.tauleryfau.com/en/auctions/all-categories?s=2141&order=ref&total=603&reference=&description='

#  Tauler y Fau has all their coins available at all_no_token
#  Each lot is at https://www.tauleryfau.com/en/lot/<auction id>/lot#-###-category
#    The lot can be read from the main page all_no_token

#  After getting the list of lots, we can download the appropriate data

r = requests.get(all_no_token)

r.status_code

soup = BeautifulSoup(r.text, 'html.parser')

lot_pattern = r'Lot\s+(\d{1,4})'
lot_no_pattern = r'/(\d{1,4})-.*$'
columns = ['Lot', 'Link']

tyf = pd.DataFrame(columns=columns)

for n, item in enumerate(soup.find_all('div')):
    # The items we want are in lot-large-block-content
    if item.has_attr('class'):
        if 'lot-large-block-content' in item['class']:
            # Get the link
            links = []
            for link in item.find_all('a'):
                links.append(link.get('href'))
            print(links)

            links = set(links)
            print(links)
            link = links.pop()
            if link:
                # Withdrawn lots may not have any links
                # Get lot number from link
                lot = re.search(lot_no_pattern, link)
                print(lot)
                if lot:
                    lot = lot.groups()[0]
                else:
                    lot = -1
                    break
                # add to df
                row = pd.DataFrame([[lot, link]], columns=columns)
                
                tyf = tyf.append(row)



del( columns,link,lot,lot_no_pattern, lot_pattern, n,row, tyf)




















