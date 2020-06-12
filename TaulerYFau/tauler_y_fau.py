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
from pathlib import Path
import shutil

def fix_desc(bad_json):
    ''' Attempt to fix description '''
    desc_pattern = r'\"description\":\s*\"(.*)\",\r\n'
#    image_pattern = r'\"image.*\r\n'
#    currency_pattern = r'\"priceCurrency.*\r\n'
#    price_pattern = r'\"price\".*\r\n'
    ret = {}
    ret['offers'] = {}
    # description
    grp = re.search(desc_pattern, bad_json)
    if grp:
        ret['description'] = grp.groups()[0]
    else:
        ret['description'] = 'Unable to parse'
    new_json = bad_json.replace(grp.group(), "")
    try:
        dct = json.loads(new_json)
        ret['image'] = dct['image']
        ret['offers']['priceCurrency'] = dct['offers']['priceCurrency']
        ret['offers']['price'] = dct['offers']['price']
    except json.JSONDecodeError:
        ret['image'] = []
        ret['offers']['priceCurrency'] = 'N/A'
        ret['offers']['price'] = None
    return ret

def download(file_name, from_link, save_to_path):
    ''' Downloads (image) file '''
    r = requests.get(from_link, stream=True)

    if r.status_code == 200:
        r.raw.decode_content = True
        with open(save_to_path.joinpath(file_name), 'wb') as f:
            shutil.copyfileobj(r.raw, f)
        return {"statusCode": 200, "path": str(save_to_path.joinpath(file_name))}
    else:
        return {"statusCode": r.status_code}



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
columns2 = ['images', 'description', 'currency',
            'price', 'file_locs', 'downloads']

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
            try:
                b = json.loads(item.contents[0])
            except json.JSONDecodeError:
                #tyf.description.loc[lot] = "Error - probably quotes inside JSON"
                b = fix_desc(item.contents[0])
            # these are only the thumbnail images... next loop will get them
            tyf.images.loc[lot] = b['image']
            tyf.description.loc[lot] = b['description']
            tyf.currency.loc[lot] = b['offers']['priceCurrency']
            tyf.price.loc[lot] = b['offers']['price']
        images = []
        imgs = soup.find_all('img', class_='img-responsive')
        for image in tyf.images.loc[lot]:
            name = image.split('/')[-1]
            for src in imgs:
                try:
                    if src['src'].endswith(name):
                        images.append(src['src'])
                except KeyError:
                    pass
        tyf.images.loc[lot] = images
        # download the images
        file_locs = []
        for image in tyf.images.loc[lot]:
            file_name = image.split('/')[-1]
            from_link = image
            save_to_path = Path(r'C:/Users/Cire/Downloads/TaulerYFau60/images/')
            file_locs.append(download(file_name, from_link, save_to_path))
        tyf['file_locs'].loc[lot] = file_locs

    sleep(3)

# Save current efforts
save_df = Path(r'C:/Users/Cire/Downloads/TaulerYFau60/Auction60.gzip')
tyf.to_parquet(save_df, compression='gzip')

# Saving images to disk

