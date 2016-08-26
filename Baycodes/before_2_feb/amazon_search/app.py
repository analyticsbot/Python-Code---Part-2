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

# create the application object
app = Flask(__name__)

http_proxy  = "http://198.169.246.30:80"
https_proxy = "https://198.169.246.30:80"
ftp_proxy   = "ftp://198.169.246.30:80"

proxyDict = { 
              "http"  : http_proxy, 
              "https" : https_proxy, 
              "ftp"   : ftp_proxy
            }

def getAmazonProducts(product, pg_max):
    url = 'http://www.amazon.co.uk/s/ref=nb_sb_noss?url=search-alias%3Daps&field-keywords=' +  '+'.join(product.split())
    pg_num = 1
    pg_max = 1

    while True:
        if pg_num == 1:
            url = url
            pg_num += 1
        else:
            if pg_num == pg_max + 1:
                break
            url = 'http://www.amazon.co.uk/s/ref=sr_pg_' + str(pg_num) + '?rh=i%3Aaps%2Ck%3A' + '+'.join(product.split()) + '&page=' + str(pg_num) + '&keywords'+  '+'.join(product.split())
            pg_num += 1
        print url    
        response = requests.get(url, headers={'User-agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36'})
        soup = BeautifulSoup(response.content, "lxml")

        elements = soup.findAll(attrs = {'class': 's-result-item celwidget'})
        print elements
        prod = {'numProducts' : len(elements)}

        for elem in elements:
            try:
                title = elem.find(attrs = {'class' : 'a-size-medium a-color-null s-inline s-access-title a-text-normal'}).getText()
            except Exception,e:
                print str(e)
                title = 'NA'
            try:
                url = elem.find(attrs = {'class' : 'a-link-normal s-access-detail-page  a-text-normal'}).attrs['href']
            except Exception,e:
                print str(e)
                url = 'NA'
            try:
                price_old = re.findall(r'\d+.\d+', elem.find(attrs = {'class' : 'a-size-small a-color-secondary a-text-strike'}).getText())[0]
            except Exception,e:
                print str(e)
                price_old = 'NA'
            try:
                price_new = re.findall(r'\d+.\d+', elem.find(attrs = {'class': 'a-size-base a-color-price s-price a-text-bold'}).getText())[0]
            except Exception,e:
                print str(e)
                price_new = 'NA'
            try:
                image = elem.find(attrs = {'class' : 'a-column a-span12 a-text-center'}).find(attrs = {'class' : 's-access-image cfMarker'}).attrs['src']
            except Exception,e:
                print str(e)
                image = 'NA'
            try:
                asin = re.findall(r'dp\/(.*?)\/', url)[0]
            except Exception,e:
                print str(e)
                asin =  'NA'

            prod['product' + str(elements.index(elem))] = {'title':title, 'url':url, 'price_old':price_old, 'price_new':price_new, 'image':image,\
                                                       'asin': asin}
    return prod

def getConversionRate(curr_from, curr_to):
    url = ('https://currency-api.appspot.com/api/%s/%s.json') % (curr_from, curr_to)
    r = requests.get(url)
    return r.json()['rate']

def getSalesRank(salesRankFrom, asin, salesRankTo):
    url = 'http://www.amazon.co.uk/dp/' + asin
    mech = Browser()
    page = mech.open(url)
    html = page.read()
    soup = BeautifulSoup(html)
    data = BeautifulSoup.extract(soup)
    salesRankElem = data.find(attrs = {'id':'SalesRank'}).find(attrs = {'class' : 'value'}).getText()
    salesRank =  re.findall(r'\d+\sin', salesRankElem)[0].replace('in','').strip()
    return salesRankFrom <= int(salesRank) <= salesRankTo
    
def getPriceAmazon(url, queue):
    response = requests.get(url, headers={'User-agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36'})
    soup = BeautifulSoup(response.content, "lxml")
    price =  soup.find(attrs = {'class': 'a-row a-spacing-mini olpOffer'}).\
            find(attrs = {'class' : 'a-size-large a-color-price olpOfferPrice a-text-bold'}).getText().strip()[1:].replace('UR', '')
    
    result = float(price.replace(',','.'))
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

def checkPrice(priceFrom, actualPrice, priceTo):
    return priceFrom <= actualPrice <= priceTo


@app.route('/', methods=['GET'])
@app.route('/search', methods=['POST'])
def search():
    if request.method == "POST":
        print request.json
        searchterm = request.json['searchterm']
        priceFrom = request.json['priceFrom']
        priceTo = request.json['priceTo']
        salesRankFrom = request.json['salesRankFrom']
        salesRankTo = request.json['salesRankTo']
        maxPages = request.json['maxPages']
        currency = request.json['currency']

        table = [['B00NVDOWUW', 'http://ecx.images-amazon.com/images/I/51SvVEAaIuL._AA160_.jpg', 21.95, 21.991076456, 24.068915219999997, 9.9824994, 1.1988481161341216], ['B00NVDMREA', 'http://ecx.images-amazon.com/images/I/61GarQyjVCL._AA160_.jpg', 8.67, 7.387049556, 3.948633096, 7.882477304, 1.1956965332592653], ['B00NVDLB56', 'http://ecx.images-amazon.com/images/I/61ASrE-yS1L._AA160_.jpg'], ['B00SDTZ0QO', 'http://ecx.images-amazon.com/images/I/61XRd9128fL._AA160_.jpg'], ['B00NVDNDUW', 'http://ecx.images-amazon.com/images/I/61rfvkkvHIL._AA160_.jpg'], ['B00NGJCKS2', 'http://ecx.images-amazon.com/images/I/51VYmmAFaGL._AA160_.jpg'], ['B013GYAQ8W', 'http://ecx.images-amazon.com/images/I/51lRn5e858L._AA160_.jpg', 11.97, 15.831504604000001, 11.084271556000001, 11.823715956000001, 0.07990858393581562], ['B00PY3EYSW', 'http://ecx.images-amazon.com/images/I/61Lb7-oMXZL._AA160_.jpg'], ['B00O1G4N48', 'http://ecx.images-amazon.com/images/I/61v220zGzwL._PI_PJStripe-Prime-Only-500px,TopLeft,0,0_AA160_.jpg'], ['0241182980', 'http://ecx.images-amazon.com/images/I/51q2D0TzK1L._AA160_.jpg', 7.49, 13.029010328, 14.811071332000001, 11.927238172, 0.0], ['B012NOGVF8', 'http://ecx.images-amazon.com/images/I/61Jovsi5S7L._AA160_.jpg'], ['B013GYAPYM', 'http://ecx.images-amazon.com/images/I/61yWtE%2B4-CL._AA160_.jpg', 11.97, 14.714943559999998, 11.084271556000001, 11.823715956000001, 0.07990858393581562], ['NA', 'NA'], ['B00F3B2Y6O', 'http://ecx.images-amazon.com/images/I/61hFyduRzdL._AA160_.jpg'], ['B00SDTT1QY', 'http://ecx.images-amazon.com/images/I/61POi67xsfL._AA160_.jpg', 29.75, 29.267209352, 31.049270356, 26.412953968, 0.12634126557911396], ['B003NE5L86', 'http://ecx.images-amazon.com/images/I/41BE%2BdIfssL._AA160_.jpg', 9.99, 16.999826755999997, 20.046337684, 11.453993756000001, 0.0]]
        errors = {}
        return redirect('welcome.html', table = table, errors = errors, searchterm = searchterm, title = 'Hello')

    else:
        return render_template('index.html')
        
##        if (searchterm != ''):
##            products = getAmazonProducts(searchterm, maxPages)
##            #print products
##            numProducts = products['numProducts']
##            for i in range(numProducts):
##                temp = []
##                asin = products['product' + str(i)]['asin']
##                image = products['product' + str(i)]['image']
##                temp.append(asin), temp.append(image)
##                if asin !='NA':
##                    sales_rank_check = getSalesRank(salesRankFrom, asin, salesRankTo)
##                    print sales_rank_check
##                    if sales_rank_check:
##                        conversionRate = getConversionRate('EUR', 'GBP')
##                        prices = combine(asin)
##                        finalPrices = [p if prices.index(p)==0 else p*conversionRate for p in prices]
##                        pricecheck = checkPrice(priceFrom, finalPrices[0], priceTo)
##                        if pricecheck:
##                            temp.extend(finalPrices)
##                            roi = (finalPrices[0] - min(finalPrices))/min(finalPrices)
##                            temp.append(roi)
##                            table.append(temp)
                    
##        else:
##            error =  {'error': 'search term required'}
        
            
    #return render_template('index.html')
    
    
# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)
