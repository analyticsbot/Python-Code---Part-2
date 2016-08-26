from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from goodgarage.items import GoodgarageItem
from scrapy.selector import Selector
from scrapy.http import Request
import requests, re, hashlib
import pandas as pd

class GoodGarageView(CrawlSpider):
    name = "goodgarage"
    allowed_domains = ["goodgaragescheme.com"]
    start_urls = [
        "http://www.goodgaragescheme.com/pages/search.aspx?type=garage&term=a",
        "http://www.goodgaragescheme.com/pages/search.aspx?type=garage&term=b",
        "http://www.goodgaragescheme.com/pages/search.aspx?type=garage&term=c",
        "http://www.goodgaragescheme.com/pages/search.aspx?type=garage&term=d",
        "http://www.goodgaragescheme.com/pages/search.aspx?type=garage&term=e",
        "http://www.goodgaragescheme.com/pages/search.aspx?type=garage&term=f",
        "http://www.goodgaragescheme.com/pages/search.aspx?type=garage&term=g",
        "http://www.goodgaragescheme.com/pages/search.aspx?type=garage&term=h",
        "http://www.goodgaragescheme.com/pages/search.aspx?type=garage&term=i",
        "http://www.goodgaragescheme.com/pages/search.aspx?type=garage&term=j",
        "http://www.goodgaragescheme.com/pages/search.aspx?type=garage&term=k",
        "http://www.goodgaragescheme.com/pages/search.aspx?type=garage&term=l",
        "http://www.goodgaragescheme.com/pages/search.aspx?type=garage&term=m",
        "http://www.goodgaragescheme.com/pages/search.aspx?type=garage&term=n",
        "http://www.goodgaragescheme.com/pages/search.aspx?type=garage&term=o",
        "http://www.goodgaragescheme.com/pages/search.aspx?type=garage&term=p",
        "http://www.goodgaragescheme.com/pages/search.aspx?type=garage&term=q",
        "http://www.goodgaragescheme.com/pages/search.aspx?type=garage&term=r",
        "http://www.goodgaragescheme.com/pages/search.aspx?type=garage&term=s",
        "http://www.goodgaragescheme.com/pages/search.aspx?type=garage&term=t",
        "http://www.goodgaragescheme.com/pages/search.aspx?type=garage&term=u",
        "http://www.goodgaragescheme.com/pages/search.aspx?type=garage&term=v",
        "http://www.goodgaragescheme.com/pages/search.aspx?type=garage&term=w",
        "http://www.goodgaragescheme.com/pages/search.aspx?type=garage&term=x",
        "http://www.goodgaragescheme.com/pages/search.aspx?type=garage&term=y",
        "http://www.goodgaragescheme.com/pages/search.aspx?type=garage&term=z"
]
    start_urls = ["http://www.goodgaragescheme.com/pages/search.aspx?type=garage&term=z"]
    rules = [Rule(LinkExtractor(allow = ['pages/garage.aspx']),                   
                  callback='parse_file_page',                   
                   follow=False)]
    
    def parse_file_page(self, response):
        #item passed from request
        item = GoodgarageItem()
        
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
