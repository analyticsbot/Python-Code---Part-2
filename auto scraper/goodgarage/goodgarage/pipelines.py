from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
import pandas as pd

class GoodgaragePipeline(object):
    def process_item(self, item, spider):
        return item

class MyPipeline(object):
    """Class that processes the items"""
    def __init__(self):        
        dispatcher.connect(self.spider_opened, signals.spider_opened)
        dispatcher.connect(self.spider_closed, signals.spider_closed)
        self.__hdr = ['url', 'compay_name', 'email', 'phone_number', 'website', 'address', 'contact_name', 'date_joined',\
                      'business_formed']

    def spider_opened(self, spider):
        print("Opened the file. Read the contents into a dataframe!")
        try:
            self.writer = pd.ExcelWriter('data.xlsx')
            self.df_data = pd.read_excel('data.xlsx','Sheet1')
        except:
            self.writer = pd.ExcelWriter('data.xlsx', engine='xlsxwriter')
            cols_data = self.__hdr
            self.df_data = pd.DataFrame(columns=cols_data)
        
    def spider_closed(self, spider):
        print("Data scraped writing to a file!")
        self.df_data.to_excel(self.writer,'Sheet1', index = False, header = self.__hdr)
        self.writer.save()

    def makeGood(self, text):
        return ''.join([i if ord(i) < 128 else ' ' for i in text])

    def process_item(self, item, spider):        
            print("Goodgarage spider scraping url :: " + item['url'])
            values = ['NA']*len(self.__hdr)
            for key in item.keys():
                try:
                    ix = self.__hdr.index(key)
                    values[ix] = (item[key])
                except:
                    pass
            nrow_data = self.df_data.shape[0]
            nrow_data +=1
            self.df_data.loc[nrow_data] =  values
