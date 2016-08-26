# -*- coding: cp1252 -*-
# import the Flask class from the flask module
from flask import Flask, render_template, request
from bs4 import BeautifulSoup
import requests, random
from amazon.api import AmazonAPI
from flask_table import Table, Col
import threading, re
from selenium import webdriver
from threading import Thread
import Queue
import mechanize
from mechanize import Browser
from random import choice

PROXY_MAX_TRY = 20

proxies = [
    'http://112.25.185.171:8000'
    'http://198.169.246.30:80'
    'http://120.27.101.186:1080'
]

def random_proxy():
    return choice(proxies)

def getConversionRate(curr_from, curr_to):
    url = ('https://currency-api.appspot.com/api/%s/%s.json') % (curr_from, curr_to)
    r = requests.get(url)
    return r.json()['rate']



user_agents = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/600.8.9 (KHTML, like Gecko) Version/8.0.8 Safari/600.8.9',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.27 (KHTML, like Gecko) Chrome/12.0.712.0 Safari/534.27",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.24 Safari/535.1",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.874.120 Safari/535.2",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.36 Safari/535.7",
    "Mozilla/5.0 (Windows; U; Windows NT 6.0 x64; en-US; rv:1.9pre) Gecko/2008072421 Minefield/3.0.2pre",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.10) Gecko/2009042316 Firefox/3.0.10",
    "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-GB; rv:1.9.0.11) Gecko/2009060215 Firefox/3.0.11 (.NET CLR 3.5.30729)",
    "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6 GTB5",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; tr; rv:1.9.2.8) Gecko/20100722 Firefox/3.6.8 ( .NET CLR 3.5.30729; .NET4.0E)",
    "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Mozilla/5.0 (Windows NT 5.1; rv:5.0) Gecko/20100101 Firefox/5.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0a2) Gecko/20110622 Firefox/6.0a2",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:7.0.1) Gecko/20100101 Firefox/7.0.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:2.0b4pre) Gecko/20100815 Minefield/4.0b4pre",
    "Mozilla/4.0 (compatible; MSIE 5.5; Windows NT 5.0 )",
    "Mozilla/4.0 (compatible; MSIE 5.5; Windows 98; Win 9x 4.90)",
    "Mozilla/5.0 (Windows; U; Windows XP) Gecko MultiZilla/1.6.1.0a",
    "Mozilla/2.02E (Win95; U)",
    "Mozilla/3.01Gold (Win95; I)",
    "Mozilla/4.8 [en] (Windows NT 5.1; U)",
    "Mozilla/5.0 (Windows; U; Win98; en-US; rv:1.4) Gecko Netscape/7.1 (ax)",
    "Opera/7.50 (Windows XP; U)",
    "Opera/7.50 (Windows ME; U) [en]",
    "Opera/7.51 (Windows NT 5.1; U) [en]"
]

def random_user_agent():
    return choice(user_agents)

def check_proxy(session):
    count = 0
    while True:
        count +=1
        proxy_host = random_proxy()
        #print proxy_host
        response = session.get('http://canihazip.com/s')
        returned_ip = response.text
        if returned_ip == proxy_host:
            return proxy_host
            break
        elif count == PROXY_MAX_TRY:
            return 'NA'
            break

##session = requests.Session()
##print check_proxy(session)

def getAmazonProducts(product, pg_max):
    url = 'http://www.amazon.co.uk/s/ref=nb_sb_noss?url=search-alias%3Daps&field-keywords=' +  '+'.join(product.split())
    pg_num = 1
    #pg_max = 1
    prod = {}
    prod['numProducts'] = 0
    count = 0
    while True:
        if pg_num == 1:
            url = url
            pg_num += 1
        else:
            if pg_num == pg_max + 1:
                break
            url = 'http://www.amazon.co.uk/s/ref=sr_pg_' + str(pg_num) + '?rh=i%3Aaps%2Ck%3A' + '+'.join(product.split()) + '&page=' + str(pg_num) + '&keywords'+  '+'.join(product.split())
            pg_num += 1
        #print url
        session = requests.Session()
        session.headers = random_user_agent()# will imported with "from user_agents import random_user_agent"
        proxy = check_proxy(session)
        if proxy != 'NA':
            session.proxies = {'http': proxy}
            print session.headers, session.proxies
        #check_proxy(session, proxy['host'])  # will be proxies.check_proxy(session, proxy['host'])

        #response = session.get(url, headers={'User-agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36'})
        response = session.get(url)
        soup = BeautifulSoup(response.content, "lxml")

        elements = soup.findAll(attrs = {'class': 's-result-item celwidget'})
        #print elements
        prod['numProducts'] += len(elements)
    
        for elem in elements:
            try:
                title = elem.find(attrs = {'class' : 'a-size-medium a-color-null s-inline s-access-title a-text-normal'}).getText()
            except Exception,e:
                #print str(e)
                title = 'NA'
            try:
                url = elem.find(attrs = {'class' : 'a-link-normal s-access-detail-page  a-text-normal'}).attrs['href']
            except Exception,e:
                #print str(e)
                url = 'NA'
            try:
                price_old = re.findall(r'\d+.\d+', elem.find(attrs = {'class' : 'a-size-small a-color-secondary a-text-strike'}).getText())[0]
            except Exception,e:
                #print str(e)
                price_old = 'NA'
            try:
                price_new = re.findall(r'\d+.\d+', elem.find(attrs = {'class': 'a-size-base a-color-price s-price a-text-bold'}).getText())[0]
            except Exception,e:
                #print str(e)
                price_new = 'NA'
            try:
                image = elem.find(attrs = {'class' : 'a-column a-span12 a-text-center'}).find(attrs = {'class' : 's-access-image cfMarker'}).attrs['src']
            except Exception,e:
                #print str(e)
                image = 'NA'
            try:
                asin = re.findall(r'dp\/(.*?)\/', url)[0]
            except Exception,e:
                #print str(e)
                asin =  'NA'

            prod['product' + str(count)] = {'title':title, 'url':url, 'price_old':price_old, 'price_new':price_new, 'image':image,\
                                                       'asin': asin}
            count +=1
    return prod


def getSalesRank(salesRankFrom, asin, salesRankTo):
    url = 'http://www.amazon.co.uk/dp/' + asin
    print url
    mech = Browser()
    #proxy = random_proxy()  # will be proxies.random_proxy()
    session = requests.Session()
    proxy = check_proxy(session)  # will be proxies.random_proxy()
    
    #mech.addheaders = [('User-agent', random_user_agent())]  # will imported with "from user_agents import random_user_agent"
    if proxy !='NA':
        mech.set_proxies({'http': proxy})
    #mech.set_proxies({'http': 'http://190.98.162.22:8080'})
    page = mech.open(url)
    html = page.read()
    try:
        soup = BeautifulSoup(str(html))
        data = BeautifulSoup.extract((soup))
        salesRankElem = data.find(attrs = {'id':'SalesRank'}).find(attrs = {'class' : 'value'}).getText()
        salesRank =  re.findall(r'\n(.*?)\sin', salesRankElem)[0].replace('in','').replace(',','').strip()
        print salesRank
        return salesRankFrom <= int(salesRank) <= salesRankTo
    except Exception,e:
        print str(e)
        return True
    
def getPriceAmazon(url, queue):
    print url
    session = requests.Session()
    proxy = check_proxy(session)  # will be proxies.random_proxy()
    session.headers = random_user_agent()  # will imported with "from user_agents import random_user_agent"
    if proxy!='NA':
        session.proxies = {'http': proxy}
    #check_proxy(session, proxy['host'])  # will be proxies.check_proxy(session, proxy['host'])
    #response = requests.get(url, headers={'User-agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36'})
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "lxml")
    #print soup
    try:
        price =  soup.find(attrs = {'class': 'a-row a-spacing-mini olpOffer'}).\
            find(attrs = {'class' : 'a-size-large a-color-price olpOfferPrice a-text-bold'}).getText().strip()[1:].replace('UR', '')
    
        result = float(price.replace(',','.'))
    except:
        result = 'NA'
    queue.put(result)

def combine(asin):
    q1 = Queue.Queue()
    q2 = Queue.Queue()
    q3 = Queue.Queue()
    q4 = Queue.Queue()

    url1 = 'http://www.amazon.co.uk/gp/offer-listing/{ASIN}/ref=dp_olp_new?ie=UTF8&condition=new'.replace('{ASIN}', asin)
    url2 = 'http://www.amazon.fr/gp/offer-listing/{ASIN}/ref=dp_olp_new?ie=UTF8&condition=new'.replace('{ASIN}', asin)
    url3 = 'http://www.amazon.it/gp/offer-listing/{ASIN}/ref=dp_olp_new?ie=UTF8&condition=new'.replace('{ASIN}', asin)
    url4 = 'http://www.amazon.es/gp/offer-listing/{ASIN}/ref=dp_olp_new?ie=UTF8&condition=new'.replace('{ASIN}', asin)

    t1 = Thread(target = getPriceAmazon, args=(url1, q1))
    t2 = Thread(target = getPriceAmazon, args=(url2, q2))
    t3 = Thread(target = getPriceAmazon, args=(url3, q3))
    t4 = Thread(target = getPriceAmazon, args=(url4, q4))
    
    t1.start()
    t2.start()
    t3.start()
    t4.start()

    t1.join()
    t2.join()
    t3.join()
    t4.join()

    return [q1.get(),q2.get(),q3.get(),q4.get()]

###################################################
def checkPrice(priceFrom, actualPrice, priceTo):
    return priceFrom <= actualPrice <= priceTo

def getDataAmazon(prod, queue, conversionRate, priceFrom, priceTo, salesRankFrom, salesRankTo):
    temp = []
    asin = prod['asin']
    image = prod['image']
    temp.extend([asin, image])
    print asin, image
    if asin !='NA':
        sales_rank_check = getSalesRank(salesRankFrom, asin, salesRankTo)
        print sales_rank_check
        if sales_rank_check:            
            prices = combine(asin)
            print prices
            finalPrices = [p if prices.index(p)==0 else p*conversionRate for p in prices]
            print finalPrices
            pricecheck = checkPrice(priceFrom, finalPrices[0], priceTo)
            if pricecheck:
                temp.extend(finalPrices)
                roi = (finalPrices[0] - min(finalPrices))/min(finalPrices)
                temp.append(roi)
                
        queue.put(temp)
    else:
        queue.put(temp)

def main(products, priceFrom, priceTo, salesRankFrom, salesRankTo):
    conversionRate = getConversionRate('EUR', 'GBP')
    print conversionRate
    queue_list = []
    numProducts = products['numProducts']
    for i in range(numProducts):
        queue_list.append(Queue.Queue())

    threads= []
    
    for i in range(numProducts):
        threads.append(Thread(target = getDataAmazon, args=(products['product' + str(i)], queue_list[i], conversionRate,\
                                                            priceFrom, priceTo, salesRankFrom, salesRankTo)))
    
    for t in threads:
        t.start()

    for t in threads:
        t.join()

    queue_data = []
    for q in queue_list:
        queue_data.append(q.get())
    return queue_data

def search():    
    searchterm = 'lego'
    priceFrom = 1
    priceTo = 100
    salesRankFrom = 10
    salesRankTo = 1000
    maxPages = 1
    currency = 'GBP'

    table = []
    errors = {}

    if (searchterm != ''):
        products = getAmazonProducts(searchterm, maxPages)
        table = main(products, priceFrom, priceTo, salesRankFrom, salesRankTo)
    print table
##        print products.keys()
##        numProducts = products['numProducts']
##        print numProducts
##        for i in range(numProducts):
##            temp = []
##            asin = products['product' + str(i)]['asin']
##            image = products['product' + str(i)]['image']
##            temp.append(asin), temp.append(image)
##            print asin, image
##            if asin !='NA':
##                sales_rank_check = getSalesRank(salesRankFrom, asin, salesRankTo)
##                print sales_rank_check
##                if sales_rank_check:
##                    
##                    prices = combine(asin)
##                    print prices
##                    finalPrices = [p if prices.index(p)==0 else p*conversionRate for p in prices]
##                    print finalPrices
##                    pricecheck = checkPrice(priceFrom, finalPrices[0], priceTo)
##                    if pricecheck:
##                        temp.extend(finalPrices)
##                        roi = (finalPrices[0] - min(finalPrices))/min(finalPrices)
##                        temp.append(roi)
##                        table.append(temp)
        
######################
def search11():    
    searchterm = 'lego'
    priceFrom = 1
    priceTo = 100
    salesRankFrom = 10
    salesRankTo = 1000
    maxPages = 1
    currency = 'GBP'

    table = []
    errors = {}

    if (searchterm != ''):
        products = getAmazonProducts(searchterm, maxPages)
        print products.keys()
        numProducts = products['numProducts']
        print numProducts
        for i in range(numProducts):
            temp = []
            asin = products['product' + str(i)]['asin']
            image = products['product' + str(i)]['image']
            temp.append(asin), temp.append(image)
            print asin, image
            if asin !='NA':
                sales_rank_check = getSalesRank(salesRankFrom, asin, salesRankTo)
                print sales_rank_check
                if sales_rank_check:
                    
                    prices = combine(asin)
                    print prices
                    finalPrices = [p if prices.index(p)==0 else p*conversionRate for p in prices]
                    print finalPrices
                    pricecheck = checkPrice(priceFrom, finalPrices[0], priceTo)
                    if pricecheck:
                        temp.extend(finalPrices)
                        roi = (finalPrices[0] - min(finalPrices))/min(finalPrices)
                        temp.append(roi)
                        table.append(temp)
        print table
                    

##products = getAmazonProducts('lego', 2)
##print products.keys()
##print getSalesRank(100, 'B00NVDNDUW', 200)
##print getSalesRank(100, 'B00NVDOWUW', 200)
##print combine('B00NVDNDUW')
search()
        
