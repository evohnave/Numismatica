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
    name = "auction_results"
    allowed_domains = ["web"]
    start_urls = (
            NOMOS,
        )

    def parse(self, response):
        ''' parses response '''
        item = Item()
        loader = ItemLoader(item=item, response=response)
        item.fields['url'] = Field()
        loader.add_value('url', NOMOS)
        item.fields['base'] = Field()
        loader.add_value('base', BASE_URL)
        ctls = findall(r'(ctl\d{2})_lblDescription', str(response.text))
        self.log(f"\nThere are {len(ctls)} items.\n")
        for ctl in ctls:
            xpth = '//*[(@id = "' + ctl + '_lblDescription")]'
            item.fields[ctl] = Field()
            loader.add_xpath(ctl, xpth)
            item.fields[ctl+'_url'] = Field()
            xapth = xpth + '//a/@href'
            loader.add_xpath(ctl + '_url', xapth)
            item.fields[ctl + '_date_loc'] = Field()
            xpath = xpth + '[1]/text()'
            loader.add_xpath(ctl + '_date_loc', xpath)
            item.fields[ctl + '_descr'] = Field()
            xpath = xpth + '/b[1]/text()'
            loader.add_xpath(ctl + '_descr', xpath)
        return loader.load_item()
