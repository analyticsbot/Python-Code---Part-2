# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AutogarageItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    email = scrapy.Field()
    mobile = scrapy.Field()
    address = scrapy.Field()
    website = scrapy.Field()
    rating = scrapy.Field()
