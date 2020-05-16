# -*- coding: utf-8 -*-
"""
Scrapes pdfs from Numismatica Ars Classica

"""

from pathlib import Path

import requests as r
import pandas as pd

def nac_downloader():
    ''' Downloads pdfs from Numismatica Ars Classica Web Site '''
    nac_urls = [
        'http://www.arsclassicacoins.com/wp-content-nasecure/uploads/2020/04/',
        'http://www.arsclassicacoins.com/wp-content-nasecure/uploads/2020/05/',
        ]

    pdfs = {}

    for url in nac_urls:
        page = pd.read_html(url)
        page = page[0]
        pdfs[url] = []
        for name in page.Name:
            try:
                if name.endswith('.pdf'):
                    pdfs[url].append(name)
            except:
                # Not all the names are strings...
                pass

    save_path = Path('//dt/Springer/NAC')

    for base_url in pdfs:
        for pdf in pdfs[base_url]:
            dld = r.get(base_url+pdf)
            with open(save_path.joinpath(pdf), 'wb') as wrt:
                wrt.write(dld.content)
