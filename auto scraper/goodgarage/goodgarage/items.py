# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GoodgarageItem(scrapy.Item):
    # define the fields for your item
    url = scrapy.Field()
    compay_name = scrapy.Field()
    email = scrapy.Field()
    phone_number = scrapy.Field()
    website = scrapy.Field()
    address = scrapy.Field()
    contact_name = scrapy.Field()
    date_joined = scrapy.Field()
    business_formed = scrapy.Field()
