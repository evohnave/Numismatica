# -*- coding: utf-8 -*-
"""
Created on Sat Jun  6 10:24:50 2020

@author: Cire
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import json
from time import sleep

base = 'https://www.tauleryfau.com'

lot1img = 'img/thumbs/700/001/997/001-997-27_01.jpg'

all_coins = 'https://www.tauleryfau.com/en/auctions/all-categories?_token=iNfGYfH8AQgptPuIWd9rXpWeJCxvQ6ROnW1p9VZY&s=2141&order=ref&total=603&reference=&description='
all_no_token = 'https://www.tauleryfau.com/en/auctions/all-categories?s=2141&order=ref&total=603&reference=&description='

lot2 = 'https://www.tauleryfau.com/en/lot/24062020-2141-2141/2-997-greek-coins'
lot1 = 'https://www.tauleryfau.com/en/lot/24062020-2141-2141/1-997-greek-coins'

r = requests.get(all_no_token)

r.status_code

soup = BeautifulSoup(r.text, 'html.parser')

lot_pattern = r'Lot\s+(\d{1,4})'
lot_no_pattern = r'\/(\d{1,4})-.*$'
category_pattern = r'\/\d{1,4}-\d{1,4}-(.*$)'
columns = ['Lot', 'Link', 'Category']
columns2 = ['images', 'description', 'currency', 'price']

tyf = pd.DataFrame(columns=columns+columns2)

for item in soup.find_all('div', class_='lot-large-block-content'):
    links = []
    for link in item.find_all('a'):
        links.append(link.get('href'))

    links = set(links)
    link = links.pop()
    if link:
        # Withdrawn lots may not have any links
        # Get lot number from link
        lot = re.search(lot_no_pattern, link)
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

tyf.set_index('Lot', inplace=True)

for lot in tyf.index:
    coin_url = base + tyf.Link.loc[lot]
    r = requests.get(coin_url)
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, 'html.parser')   

        for item in soup.find_all('script', 
                                  attrs={"type": "application/ld+json"}):
            b = json.loads(item.contents[0])
            tyf.images.loc[lot] = b['image']
            tyf.description.loc[lot] = b['description']
            tyf.currency.loc[lot] = b['offers']['priceCurrency']
            tyf.price.loc[lot] = b['offers']['price']
    sleep(5)

            
    
    
#    break
#
#
#img_pattern = r'https.*\.jpg'
#
#r = requests.get(lot1)
#
#r.status_code
#
#soup = BeautifulSoup(r.text, 'html.parser')
#
#columns2 = ['images', 'description', 'currency', 'price']
#tyf2 = pd.DataFrame(columns=columns2)
#
#columns2 = ['images', 'description', 'currency', 'price']
#tyf2 = pd.DataFrame(columns=columns2)
#
## Will loop over tyf for each row...
#for item in soup.find_all('script', attrs={"type": "application/ld+json"}):
#    b = json.loads(item.contents[0])
#    row = pd.DataFrame(columns=columns2)
#    images = b['image']
#    description = b['description']
#    currency = b['offers']['priceCurrency']
#    price = b['offers']['price']
#    row = pd.DataFrame([images, description, currency, price],
#                       columns=columns2
#           )
#    tyf2 = tyf2.append(row)
#
#
#n=0
#for item in soup.find_all('script', attrs={"type": "application/ld+json"}):
#    n +=1
#print(n)
#
#
#
##    
###    print(item)
###    print ("\n\n\n")
###    print(f"{dir(item)}")
###    print ("\n\n\n")
###    print(item.contents)
##    print("\n\n\n Item Contents as json?")
##    b = json.loads(item.contents[0])
##    print(b)
##    print ("\n\n\n")    
##    print(b['image'])
##    print ("\n\n\n")
##    print(b['description'])
##    print ("\n\n\n")
#<<<<<<< HEAD
##    print(b['offers']['priceCurrency'])
##    print(b['offers']['price'])
##
#=======
##    print(item.contents)
#    # print("\n\n\n Item Contents as json?")
#    b = json.loads(item.contents[0])
#    # print(b)
#    # print ("\n\n\n")    
#    images = b['image']
#    # print ("\n\n\n")
#    description = b['description']
#    # print ("\n\n\n")
#    currency = b['offers']['priceCurrency']
#    # print ("\n\n\n")
#    price = b['offers']['price']
#    # print ("\n\n\n")
#    row = pd.DataFrame([[images, description, currency, price]],
#                       columns=columns2)
#    print(row)
#    
#
#
#>>>>>>> d3e76bf62ec4c20dfe0f6b6f4a1182e89a8ebc15
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
