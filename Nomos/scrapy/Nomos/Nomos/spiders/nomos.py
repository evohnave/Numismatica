# -*- coding: utf-8 -*-
"""
Nomos Spider

"""

from re import findall

import scrapy

from Nomos.items import NomosItem

NOMOS = 'https://nomosag.com/default.aspx?page=ucPastAuctions'

class NomosSpider(scrapy.Spider):
    ''' Class for scraping Nomos Auction Results '''
    name = "auction_results"
    allowed_domains = ["web"]
    start_urls = (
            NOMOS,
        )

    def parse(self, response):
        ''' parses response '''
        item = PropertiesItem()
        ctls = findall(r'ctl\d{2}', str(response.text))
        for ctl in ctls:
            xpth = '//*[(@id = "'+ctl+'_lblDescription")]'
            #self.log("title: %s" % response.xpath(
            #    '//*[(@id = "ctl01_lblDescription")]').extract())
            #self.log("title: %s" % response.xpath(xpth).extract())
            item[ctl] = response.xpath(xth).extract()
        return item
