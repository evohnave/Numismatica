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


lot2 = 'https://www.tauleryfau.com/en/lot/24062020-2141-2141/2-997-greek-coins'
lot1 = 'https://www.tauleryfau.com/en/lot/24062020-2141-2141/1-997-greek-coins'
#  Tauler y Fau has all their coins available at all_no_token
#  Each lot is at https://www.tauleryfau.com/en/lot/<auction id>/lot#-###-category
#    The lot can be read from the main page all_no_token

#  After getting the list of lots, we can download the appropriate data

r = requests.get(all_no_token)

r.status_code

soup = BeautifulSoup(r.text, 'html.parser')

lot_pattern = r'Lot\s+(\d{1,4})'
lot_no_pattern = r'\/(\d{1,4})-.*$'
category_pattern = r'\/\d{1,4}-\d{1,4}-(.*$)'
columns = ['Lot', 'Link', 'Category']

tyf = pd.DataFrame(columns=columns)

for item in soup.find_all('div'):
    # The items we want are in lot-large-block-content
    if item.has_attr('class'):
        if 'lot-large-block-content' in item['class']:
            # Get the link
            links = []
            for link in item.find_all('a'):
                links.append(link.get('href'))
            #print(links)

            links = set(links)
            #print(links)
            link = links.pop()
            if link:
                # Withdrawn lots may not have any links
                # Get lot number from link
                lot = re.search(lot_no_pattern, link)
                #print(lot)
                if lot:
                    lot = lot.groups()[0]
                else:
                    lot = -1
                    break
                # Get category from link
                category = re.search(category_pattern, link)
                if category:
                    category = category.groups()[0]
                else:
                    category = "Not listed"
                # add to df
                row = pd.DataFrame([[lot, link, category]], columns=columns)
                
                tyf = tyf.append(row)



del( columns,link,lot,lot_no_pattern, lot_pattern, row, tyf)
img_pattern = r'https.*\.jpg'

r = requests.get(lot2)

r.status_code

soup = BeautifulSoup(r.text, 'html.parser')

picture_links = set()

for item in soup.find_all('div', class_='item_content_img_single'):
    for link in item.find_all('img'):
        picture_links.add(link.get('src'))
    
import json

for item in soup.find_all('script', attrs={"type": "application/ld+json"}):
#    print(item)
#    print ("\n\n\n")
#    print(f"{dir(item)}")
#    print ("\n\n\n")
#    print(item.contents)
    print("\n\n\n Item Contents as json?")
    b = json.loads(item.contents[0])
    print(b)
    print ("\n\n\n")    
    print(b['image'])
    print ("\n\n\n")
    print(b['description'])
    print ("\n\n\n")
    print(b['description'])
    print ("\n\n\n")









































