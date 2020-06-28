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

#------------------------------------------------------------------------------
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
#------------------------------------------------------------------------------
        

finished_auctions = 'https://www.sarc.auction/auctionlist.aspx?dv=2&so=2&ps=200'

r = requests.get(finished_auctions)

r.status_code

soup = BeautifulSoup(r.text, 'html.parser')

row_pages = soup.find_all('div', class_='row_pages')

page_links = [link.get('href') 
              for page in row_pages 
              for link in page.find_all('a')]
# Create basic auction info 
columns = ['auctionName', 'sessionInfo', 'raw']
sarc = pd.DataFrame(columns=columns)
spans = soup.find_all('span', class_='title')
for n, span in enumerate(spans):
    span_strings = list(span.strings)
    #print(f"debug span_strings {span_strings}")
    auctionName = span_strings[0]
    #print(f"debug auctionName {auctionName}")
    sessionInfo = span_strings[1]
    #print(f"debug sessionInfo {sessionInfo}")
    raw = str(span)
    #print(f"debug raw {str(span)}")
    row = pd.DataFrame([[auctionName, sessionInfo, raw]],
                       columns=columns)
    sarc = sarc.append(row)
# Get auction name
#  First, strip off Stephen Album then get rid of anything like w/#33
# Then replace Internet-Only with '10000'
sarc['auction'] = sarc.auctionName.replace(
    to_replace=r'^Stephen Album Rare Coins (-|\|) ',
    value='', regex=True
    ).replace(to_replace=r'\s*\|.*$', value='', regex=True
    ).replace(to_replace=r'^Internet-Only Auction #',
    value='10000', regex=True
    ).replace(to_replace=r'^Auction ', value='0000', regex=True
    ).replace(to_replace=r'00009', value='000009', regex=True)




# Save sarc as sarc_auction_info.gzip efforts
# save_df = Path(r'C:/Users/Cire/Downloads/SARC/20200614_sarc_auction_info.gzip')
# sarc.to_parquet(save_df, compression='gzip')

test_page_link = page_links[46]
# picked # 46 since it has a Danishmendid I bought, lot 528

r = requests.get(test_page_link)
r.status_code
soup = BeautifulSoup(r.text, 'html.parser')
items = soup.find_all('div', class_='gridItem')

len(items)
columns = ['lotnum', 'raw', 'partial_description', 'currency', 'total',
           'quantity', 'hammer', 'premium', 'estimates', 'low_est',
           'hi_est', 'lot_link']
sarc_lots = pd.DataFrame(columns=columns)
for item in items:
    raw = item
    lotnum = int(item.find('span', class_='gridView_heading')
                     .find('i', class_ = 'gridView_lotnum')
                     .text
                     .rstrip(' - ')
                     )
    description = item.find('div', 
                            class_='description gridView_description').text
    currency = 'USD'
    try:
        winbid = item.find('div', 
                           class_='gridView_winningbid linkinfo bidinfo').text
        win_patt = r'Sold for \((\d+.*\.00)\s*\+?\s*(\d+.*\.00)?\)\s*x\s*(\d*)\s*=\s*(\d+.*\.00)'
        win = re.search(win_patt, winbid)
    except AttributeError:
        win = None
    if win:
        hammer, premium, quantity, total = win.groups()
    else:
        hammer = premium = quantity = total = None
    est_patt = r'Estimates\s*:\s*(\d+.*\.00)\s*-\s*(\d+.*\.00)?'
    estimates = item.find('div', class_='startpriceestimates').text
    low_est, hi_est = re.search(est_patt, estimates).groups()
    info = item.find('a')
    lot_link = info.get('href')
    thumbnail = info.find('img').get('src').split('?')[0]
    row = pd.DataFrame([[lotnum, raw, description, currency, total, quantity, 
                         hammer, premium, estimates, low_est, hi_est, lot_link]],
                       columns=columns
                        )
    sarc_lots = sarc_lots.append(row)

# Now go get all the info from each lot... can skip several items, but images
#   and description are probably needed

# iterate over the lot_links
#   But I'm not doing it for now... just do one

r = requests.get(lot_link)
r.status_code
soup = BeautifulSoup(r.text, 'html.parser')
item = soup.find('ul', id="item_media_thumbnails")
images_as = item.find_all('a')
images_links = [a.get('href') for a in images_as]
description = soup.find('span', id="cphBody_cbItemDescription").string

#------------------------- Works above here... below is old from tyf ---------
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
save_df = Path(r'C:/Users/Cire/Downloads/TaulerYFau60/20200624_Auction_000060.gzip')
tyf.to_parquet(save_df, compression='gzip')

# Saving images to disk

