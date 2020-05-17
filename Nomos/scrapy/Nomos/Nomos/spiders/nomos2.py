# -*- coding: utf-8 -*-
"""
Nomos Spider

"""

from re import findall

import scrapy
from scrapy.item import Field, Item
from scrapy.loader import ItemLoader

NOMOS = 'https://nomosag.com/default.aspx?page=ucPastAuctions'
BASE_URL = 'https://nomosag.com'

class NomosSpider(scrapy.Spider):
    ''' Class for scraping Nomos Auction Results '''
    name = "auction_results2"
    allowed_domains = ["web"]
    start_urls = (
            NOMOS,
        )

    def parse(self, response):
        ''' parses response '''
        item = Item()
        loader = ItemLoader(item=item, response=response)
        ctls = findall(r'(ctl\d{2})_lblDescription', str(response.text))
        self.log(f"\nThere are {len(ctls)} items.\n")
        item.fields['ctls'] = Field()
        item.fields['urls'] = Field()
        item.fields['descr'] = Field()
        item.fields['date'] = Field()
        item.fields['loc'] = Field()
        for ctl in ctls:
            xpth = '//*[(@id = "' + ctl + '_lblDescription")]'
            loader.add_xpath('ctls', xpth)
            xapth = xpth + '//a/@href'
            loader.add_xpath('urls', xapth)
            xpath = xpth + '[1]/text()[1]'
            loader.add_xpath('date', xpath)
            xpath = xpth + '[1]/text()[2]'
            loader.add_xpath('loc', xpath)
            xpath = xpth + '/b[1]/text()'
            loader.add_xpath('descr', xpath)
        return loader.load_item()
