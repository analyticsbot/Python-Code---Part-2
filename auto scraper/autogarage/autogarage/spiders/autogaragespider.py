from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from autogarage.items import AutogarageItem
from scrapy.selector import Selector
from scrapy.http import Request
import requests, re, hashlib
import pandas as pd

class AutoGarageView(CrawlSpider):
    name = "autogarage"
    allowed_domains = ["autogarage.nl"]
    start_urls = [
        "http://www.autogarage.nl/auto/"
]
    
    rules = [Rule(LinkExtractor(allow = ['bedrijf']),                   
                  callback='parse_file_page',                   
                   follow=False)]
    
    def parse_file_page(self, response):
        #item passed from request
        item = AutogarageItem()
        
        def getItem(elem):
            infoItemElems = sel.xpath('//*[@class="infoItem"]//label/text()').extract()
            print infoItemElems
            print sel.xpath('//*[@class="infoItem"]/span/a/@href').extract()
            print sel.xpath('//*[@class="infoItem"]/span/text()').extract()
            
            if ('Website address:' in infoItemElems) and ('Email address:' in infoItemElems):
                infoItemElemsVals = sel.xpath('//*[@class="infoItem"]/span/a/@href').extract()[:2] + \
                                    sel.xpath('//*[@class="infoItem"]/span/text()').extract() + \
                                    sel.xpath('//*[@class="infoItem"]/span/a/@href').extract()[2:]
                
            else:
                infoItemElemsVals = sel.xpath('//*[@class="infoItem"]/span/a/@href').extract()[:1] + \
                                    sel.xpath('//*[@class="infoItem"]/span/text()').extract() + \
                                    sel.xpath('//*[@class="infoItem"]/span/a/@href').extract()[1:]

            item_dict = {}
            for i in infoItemElems:
                item_dict[i] = infoItemElemsVals[infoItemElems.index(i)]
            print item_dict
            try:
                return item_dict[elem]
            except:
                return None
                
        #selector
        sel = Selector(response)
        item['url'] = response.url
        item['compay_name'] = str(sel.xpath('//*[@class="garagename"]/text()').extract()[0])
        item['email'] = str(getItem('Email address:')).replace('mailto:','')
        item['phone_number'] = str(getItem('Telephone:')).replace('tel:','')
        item['website'] = str(getItem('Website address:'))
        item['address'] = str(sel.xpath('//*[@class="address"]/text()').extract()[0])
        item['contact_name'] = str(getItem('Contact:'))
        item['date_joined'] = str(getItem('Date joined:'))
        item['business_formed'] = str(getItem('Business formed in:'))

                
        return item
