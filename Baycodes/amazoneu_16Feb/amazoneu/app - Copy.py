# import the Flask class from the flask module and other required modules
from flask import Flask, render_template, request, make_response, session, url_for, jsonify
from bs4 import BeautifulSoup
import requests, threading, re, os, Queue, mechanize, logging, gc, json
from random import choice 
from threading import Thread
from mechanize import Browser
from flask.ext import excel
from unidecode import unidecode       
from logging import FileHandler
from amazon.api import AmazonAPI
from werkzeug.serving import WSGIRequestHandler
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# create the application object
app = Flask(__name__)
app.secret_key = "/\xfa-\x84\xfeW\xc3\xda\x11%/\x0c\xa0\xbaY\xa3\x89\x93$\xf5\x92\x9eW}"
app.jinja_env.add_extension('jinja2.ext.loopcontrols')
app.WTF_CSRF_SECRET_KEY  = "amazoneuapp"
app.CSRF_ENABLED = True
app.debug = True

AMAZON_ACCESS_KEY='AKIAIRGYI76BYPQZXAQQ'
AMAZON_SECRET_KEY ='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'
AMAZON_ASSOC_TAG =273589934636

AMAZON_ACCESS_KEY1='AKIAIYWGSVATZRMKAIRA'
AMAZON_SECRET_KEY1 ='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'
AMAZON_ASSOC_TAG1 =289838321798 

amazon_uk = AmazonAPI(AMAZON_ACCESS_KEY, AMAZON_SECRET_KEY, AMAZON_ASSOC_TAG, region="UK")
amazon_uk1 = AmazonAPI(AMAZON_ACCESS_KEY1, AMAZON_SECRET_KEY1, AMAZON_ASSOC_TAG1, region="UK")

try:
    if os.environ['Production'] == 'True':
        app.debug = False
except Exception,e:
    print str(e)

try:
    from captcha_solver import CaptchaBreakerWrapper
except Exception as e:
    print '!!!!!!!!Captcha breaker is not available due to: %s' % e
    class CaptchaBreakerWrapper(object):
        @staticmethod
        def solve_captcha(url):
            msg("CaptchaBreaker in not available for url: %s" % url,
                level=WARNING)
            return None
        
_cbw = CaptchaBreakerWrapper()

def _has_captcha(response):
    return '.images-amazon.com/captcha/' in response.content

def _solve_captcha(response):
    soup = BeautifulSoup(response.content, "html.parser")
    forms = soup.findAll(itemprop="image")
    assert len(forms) == 1, "More than one form found."

    captcha_img = forms[0]['src']

    return _cbw.solve_captcha(captcha_img)
    
def _handle_captcha(session, response, callback):
    response.meta = {}
    captcha_solve_try = response.meta.get('captcha_solve_try', 0)
    url = response.url
    
    captcha = self._solve_captcha(response)

    if captcha is None:            
        response = response
    else:
        meta = response.meta.copy()
        meta['captcha_solve_try'] = captcha_solve_try + 1
        response = session.post(url, params = {'field-keywords': captcha})

    return response
    
proxies = ['http://81.94.162.140:8080', 'http://197.161.150.130:8080',\
           'http://195.40.6.43:8080', 'http://198.169.246.30:80']
PROXY_MAX_TRY = 20

def random_proxy():
    """ method to return a random proxy """
    return choice(proxies)

def getConversionRate(curr_from, curr_to):
    """ method to return a conversion rate
    curr_from : from currency
    curr_to : to currency
    """
    try:
        url = ('https://currency-api.appspot.com/api/%s/%s.json') % (curr_from, curr_to)
        r = requests.get(url)
        return r.json()['rate']
    except:
        url = 'http://api.fixer.io/latest?symbols=GBP,EUR'
        r = requests.get(url)
        return float(r.json()['rates']['GBP'])

# list of available user agents
user_agents = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/600.8.9 (KHTML, like Gecko) Version/8.0.8 Safari/600.8.9',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.27 (KHTML, like Gecko) Chrome/12.0.712.0 Safari/534.27",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.24 Safari/535.1",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.874.120 Safari/535.2",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.36 Safari/535.7"]

def random_user_agent():
    """ method to return a random user agent from the above list """
    return choice(user_agents)

def check_proxy(session):
    """ method to return a working proxy else return NA. No proxy will be used then.
    Code looks at the current ip at http://canihazip.com/s and compares with the random ip picked.
    if both match, proxy is returned, else retry is done until PROXY_MAX_TRY times
    session : request module's session
    """
    return 'NA'
        
def getAmazonProducts(searchterm, pg_max):
    """ method to return the products on amazon.co.uk for the product searched
    product : search term entered by the user
    pg_max : maximum number of search results to be scraped
    """
    url = 'http://www.amazon.co.uk/s/ref=nb_sb_noss?url=search-alias%3Daps&field-keywords=' + '+'.join(searchterm.split())
    pg_num = 1
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
            url = 'http://www.amazon.co.uk/s/ref=sr_pg_' + str(pg_num) + '?rh=i%3Aaps%2Ck%3A' + '+'.join(searchterm.split()) + '&page=' + str(pg_num) + '&keywords'+  '+'.join(searchterm.split())
            pg_num += 1

        session = requests.Session()
        session.headers = random_user_agent()
        
        proxy = check_proxy(session) # checks for a working proxy, else proceeds with the current ip
        if proxy != 'NA':
            session.proxies = {'http': proxy}

        # retreived the response and pass to beautifulsoup
        response = session.get(url)

        while True:
            # handle captcha if present
            if _has_captcha(response):
                response = _handle_captcha(session, response, callback)
            else:
                break
        soup = BeautifulSoup(response.content, "html.parser")
        
        # get all the products on the search page
        elements = soup.findAll(attrs = {'class': 's-result-item'})
        prod['numProducts'] += len(elements) # increment the number of products

        # loop through the elements and get title, url, price_old, price_new, image url, asin and add to a dict object
        for elem in elements:
            try:
                title = elem.find(attrs = {'class' : 'a-size-medium a-color-null s-inline s-access-title a-text-normal'}).getText()
            except Exception,e:
                try:
                    title = elem.find(attrs = {'class' : 'a-link-normal s-access-detail-page  a-text-normal'}).getText()
                except:
                    title = 'NA'
            try:
                url = elem.find(attrs = {'class' : 'a-link-normal s-access-detail-page  a-text-normal'}).attrs['href']
            except Exception,e:
                url = 'NA'
            try:
                price_old = re.findall(r'\d+.\d+', elem.find(attrs = {'class' : 'a-size-small a-color-secondary a-text-strike'}).getText())[0]
            except Exception,e:
                price_old = 'NA'
            
            try:
                image = elem.find(attrs = {'class' : 's-access-image cfMarker'}).attrs['src']
            except Exception,e:
                image = 'NA'
                
            try:
                asin = re.findall(r'dp\/(.*?)\/', url)[0]
            except Exception,e:
                asin =  'NA'
            try:
                price_new = re.findall(r'\d+.\d+', elem.find(attrs = {'class': 'a-size-base a-color-price s-price a-text-bold'}).getText())[0]
            except Exception,e:
                try:
                    product = amazon_uk.lookup(ItemId=unidecode(asin))
                    price_new = str(product.price_and_currency[0])
                    if price_new is not None:
                        price_new = price_new
                    else:
                        price_new = 'NA'
                except:
                    try:
                        product = amazon_uk1.lookup(ItemId=unidecode(asin))
                        price_new = str(product.price_and_currency[0])
                        if price_new is not None:
                            price_new = price_new
                        else:
                            price_new = 'NA'
                    except:
                        try:
                            price_new = re.findall(r'\d+.\d+', elem.find(attrs = {'class': 'a-color-price'}).getText())[0]
                        except:
                            price_new = 'NA'

            prod['product' + str(count)] = {'title':title, 'url':url, 'price_old':price_old, 'price_new':price_new, 'image':image,\
                                                       'asin': asin}
            count +=1
    return prod

def getSalesRank(salesRankFrom, asin, salesRankTo):
    """ method to check if the sales rank of the product lies in the range provided by the user
    salesRankFrom : lower limit for sales rank entered by the user
    asin : asin of the product
    salesRankTo : upper limit for sales rank entered by the user
    """
    salesRank = 'NA'
    
    url = 'http://www.amazon.co.uk/dp/' + unidecode(asin)
    mech = Browser()
    session = requests.Session()
    proxy = check_proxy(session)

    if proxy !='NA':
        mech.set_proxies({'http': proxy})
    
    page = mech.open(url)
    if page.code ==503:
        print page.geturl()
    html = page.read()

    # try to get the sales rank else return True. Does not work sometimes. Need to be more robust.
    try:
        soup = BeautifulSoup(str(html))
        data = BeautifulSoup.extract((soup))
        salesRankElem = data.find(attrs = {'id':'SalesRank'}).find(attrs = {'class' : 'value'}).getText()
        salesRank =  re.findall(r'\n(.*?)\sin', salesRankElem)[0].replace('in','').replace(',','').strip()
        if salesRankFrom and salesRankTo:
            return (salesRankFrom <= int(salesRank) <= salesRankTo), salesRank
        else:
            return True, salesRank
    except Exception,e:
        try:
            salesRankElem = data.find(attrs = {'class':'zg_hrsr_item'}).getText()
            salesRank =  salesRankElem.split()[0].replace('#','').strip()
            if salesRankFrom and salesRankTo:
                return (salesRankFrom <= int(salesRank) <= salesRankTo), salesRank
            else:
                return True, salesRank
        except:
            try:
                product = amazon_uk.lookup(ItemId=unidecode(asin))
                salesRank = product.sales_rank
                if salesRank is not None:
                    return (salesRankFrom <= int(salesRank) <= salesRankTo), salesRank
                else:
                    return True, 'NA'
            except:
                return True, salesRank
    
def getPriceAmazon(url, queue):
    """ method to get the lowest FBA price for a asin from AZ IT, FR, ES, and UK pages 
    url : url for the amazon website. ASIN is replaced.
    queue : a queue to which the value is stored
    """
    session = requests.Session()
    
    session.headers = random_user_agent()
    proxy = check_proxy(session)  

    if proxy!='NA':
        session.proxies = {'http': proxy}
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    elements = soup.findAll(attrs = {'class': 'a-row a-spacing-mini olpOffer'})
    result = 'NA'
    for elem in elements:
        if not ((elem.find(attrs = {'class':'a-icon a-icon-prime'}) or  \
                elem.find(attrs = {'class':'a-icon a-icon-premium'})) \
                or 'premium' in str(elem.contents).lower() or \
                (elem.find(attrs = {'class':'supersaver'}))):
            continue
        try:
            price =  elem.find(attrs = {'class' : 'a-size-large a-color-price olpOfferPrice a-text-bold'}).getText().strip()[1:].replace('UR', '')
            result = float(price.replace(',','.'))
            break
        except:
            result = 'NA'
    
    queue.put(result)

def combine(asin):
    """ method to get the prices from az uk, fr, it, and es websites for an asin using multithreading
    asin : asin of the product
    """
    q1 = Queue.Queue()
    q2 = Queue.Queue()
    q3 = Queue.Queue()
    q4 = Queue.Queue()
    q5 = Queue.Queue()

    url1 = 'http://www.amazon.co.uk/gp/offer-listing/{ASIN}/ref=dp_olp_new?ie=UTF8&condition=new'.replace('{ASIN}', asin)
    url2 = 'http://www.amazon.fr/gp/offer-listing/{ASIN}/ref=dp_olp_new?ie=UTF8&condition=new'.replace('{ASIN}', asin)
    url3 = 'http://www.amazon.it/gp/offer-listing/{ASIN}/ref=dp_olp_new?ie=UTF8&condition=new'.replace('{ASIN}', asin)
    url4 = 'http://www.amazon.es/gp/offer-listing/{ASIN}/ref=dp_olp_new?ie=UTF8&condition=new'.replace('{ASIN}', asin)
    url5 = 'http://www.amazon.de/gp/offer-listing/{ASIN}/ref=dp_olp_new?ie=UTF8&condition=new'.replace('{ASIN}', asin)

    t1 = Thread(target = getPriceAmazon, args=(url1, q1))
    t2 = Thread(target = getPriceAmazon, args=(url2, q2))
    t3 = Thread(target = getPriceAmazon, args=(url3, q3))
    t4 = Thread(target = getPriceAmazon, args=(url4, q4))
    t5 = Thread(target = getPriceAmazon, args=(url5, q5))
    
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()
    

    t1.join()
    t2.join()
    t3.join()
    t4.join()
    t5.join()

    return [q1.get(),q2.get(),q3.get(),q4.get(),q5.get()]

def checkPrice(priceFrom, actualPrice, priceTo):
    """ method to check if the price of the asin lies within the range entered by the user
    priceFrom : lower limit of the price in GBP
    actualPrice : actual price in GBP
    priceTo : upper limit of the price in GBP
    """
    if priceFrom and priceTo:
        return priceFrom <= actualPrice <= priceTo
    else:
        return True

def getDataAmazon(prod, queue, conversionRate, priceFrom, priceTo, salesRankFrom, salesRankTo):
    """ method to get all the required data for a search term results and put into a queue
    prod: a dict object that has asin, image, price, sales rank info for an asin
    queue: instance of a queue
    conversionRate: conversion rate as of the search time
    priceFrom: lower limit of the price entered by the user
    priceTo: upper limit of the price entered by the user
    salesRankFrom: lower limit of the sales rank entered by the user
    salesRankTo: upper limit of the sales rank entered by the user
    """
    temp = []
    asin = (prod['asin'])
    image = prod['image']
    title = prod['title']
    try:
        price = float((prod['price_new']))
    except:
        price = 'NA'
    temp.extend([asin, title, image])
    if asin !='NA':
        sales_rank_check, salesRank = getSalesRank(salesRankFrom, asin, salesRankTo)
        if sales_rank_check:
            temp.append(salesRank)
            prices = [price] + combine(asin)[1:]
            finalPrices = []
            for p in prices:
                if prices.index(p) == 0:
                    finalPrices.append(p)
                else:
                    if p == 'NA':
                        finalPrices.append(p)
                    else:
                        finalPrices.append(float("%.2f" % (p*conversionRate)))
                    
            pricecheck = checkPrice(priceFrom, finalPrices[0], priceTo)
            if pricecheck:
                temp.extend(finalPrices)
                if (finalPrices[0] != 'NA') and (min(finalPrices) != 'NA') and (finalPrices[0] != 0) and (min(finalPrices) != 0):
                    roi = ((((finalPrices[0])) - min(finalPrices))/min(finalPrices))*100
                    roi = float("%.2f" % (roi))
                else:
                    roi = 'NA'
                temp.extend([roi, finalPrices.index(min(finalPrices))+4])  
        queue.put(temp)
    else:
        queue.put(['NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA'])

def main(products, priceFrom, priceTo, salesRankFrom, salesRankTo):
    """ method to get info using multi threading
    products: nested dict containing all the search result data
    priceFrom: lower limit of the price entered by the user
    priceTo: upper limit of the price entered by the user
    salesRankFrom: lower limit of the sales rank entered by the user
    salesRankTo: upper limit of the sales rank entered by the user
    """
    conversionRate = getConversionRate('EUR', 'GBP')
    queue_list = []
    numProducts = len(products.keys())
    for i in range(numProducts):
        queue_list.append(Queue.Queue())

    threads= []
    
    for i in products.keys():
        threads.append(Thread(target = getDataAmazon, args=(products[i], queue_list[products.keys().index(i)], conversionRate,\
                                                            priceFrom, priceTo, salesRankFrom, salesRankTo)))
     
    for t in threads:
        t.start()

    for t in threads:
        t.join()

    queue_data = []
    for q in queue_list:
        queue_data.append(q.get())
        
    return queue_data

@app.route('/', methods=['GET'])
def home():
    """ flask view for the home page"""
    return render_template('index.html')

@app.route('/previous', methods=['GET', 'POST'])
def previous():
    session['page'] -=1
    return jsonify({'data':'aa', 'status':'aa'})

@app.route('/search', methods=['POST'])
def search(numrows=10):
    """ flask view for the search page"""
    if request.method == "POST":
        errors = {}
        searchterm = request.form['searchterm']
        try:
            priceFrom = int(request.form['priceFrom'])
        except:
            priceFrom = None
        try:
            priceTo = int(request.form['priceTo'])
        except:
            priceTo = None
        try:
            salesRankFrom = int(request.form['salesRankFrom'])
        except:
            salesRankFrom = None
        try:
            salesRankTo = request.form['salesRankTo']
        except:
            salesRankTo = None
        maxPages = int(request.form['maxPages'])
        currency = str(request.form['currency'])
        session['searchterm'] = searchterm
        session['priceFrom'] = priceFrom
        session['priceTo'] = priceTo
        session['salesRankFrom'] = salesRankFrom
        session['salesRankTo'] = salesRankTo
        session['maxPages'] = maxPages
        session['currency'] = currency
        dd['status'] = False
        
        if (searchterm != ''):
            #print searchterm
            threads= []
            threads.append(Thread(target = scrapeData, args=(searchterm, maxPages, priceFrom, priceTo, \
                          salesRankFrom, salesRankTo)))
     
            for t in threads:
                t.start()
                print 'thread started'
        else:
            errors =  {'error': 'search term required'}
            

        return render_template('index.html', title = 'Search Results for ' + searchterm + ' | Page ', errors = errors,
                           searchterm = searchterm, maxPages = maxPages, priceFrom = priceFrom, priceTo = priceTo,
                           salesRankFrom = salesRankFrom, salesRankTo = salesRankTo, message = "Please Wait...")

@app.route('/checkData', methods = ['GET', 'POST'])
def checkData():
    print 'checkdata'
    searchterm = session['searchterm'] 
    priceFrom = session['priceFrom']
    priceTo = session['priceTo']
    salesRankFrom = session['salesRankFrom']
    salesRankTo = session['salesRankTo']
    maxPages = session['maxPages']
    currency = session['currency']
    errors = {}
    if request.method == 'GET':
        if dd['status']:
            table = dd['table']
            stop = True
            dd['status'] = False
            return jsonify(table=str(returnTableHTMl(table)),
                   stop=True )
            #return str(returnTableHTMl(table))
        else:
            continue_ = True
            return render_template('index.html', title = 'Search Results for ' + searchterm + ' | Page ', errors = errors,
                               searchterm = searchterm, maxPages = maxPages, priceFrom = priceFrom, priceTo = priceTo,
                               salesRankFrom = salesRankFrom, salesRankTo = salesRankTo, message = "Please Wait...", continue_ = continue_)
##    else:
##        return render_template('index.html', title = 'Search Results for ' + searchterm + ' | Page ', errors = errors,
##                               searchterm = searchterm, maxPages = maxPages, priceFrom = priceFrom, priceTo = priceTo,
##                               salesRankFrom = salesRankFrom, salesRankTo = salesRankTo, message = "Please Wait...")
    
global dd
dd= {}
def scrapeData(searchterm, maxPages, priceFrom, priceTo, salesRankFrom, salesRankTo):
##    products = getAmazonProducts(searchterm, maxPages)
##    #print products
##    table = []
##    count = 1
##    while True:
##        table.extend(main({k: products[k] for k in products.keys()[18*(count-1):18*(count)] if k != 'numProducts' }, priceFrom, priceTo, \
##                          salesRankFrom, salesRankTo))                
##        if (count*18)>=products['numProducts']:
##            break
##        count +=1
##    print (table)
    table = [[u'B00CH08M0G', u'Sony DSCHX50 Compact Digital Camera - Black (20.4MP, 30x Optical Zoom) 3 inch LCD', u'http://ecx.images-amazon.com/images/I/41RbnhizpbL._AA160_.jpg', '6184', 179.99, 'NA', 'NA', 'NA', 'NA', 0.0, 4], [u'B00BHXVX3M', u'Sony DSCHX300V Digital Compact Bridge Camera with High Quality Lens (Electronic View Finder, 20.4 MP, 50x Optical...', u'http://ecx.images-amazon.com/images/I/51YmG1sV5L._AA160_.jpg', '2795', 189.0, 'NA', 'NA', 'NA', 'NA', 0.0, 4], [u'B00IGL9SLW', u'Sony DSCWX220 Digital Compact Camera with Wi-Fi and NFC (18.2 MP, 10x Optical Zoom) - Black', u'http://ecx.images-amazon.com/images/I/41ziw6JlWBL._AA160_.jpg', '5659', 109.0, 157.41, 'NA', 179.45, 190.18, 0.0,4], [u'B00KW3BJ1Y', u'Sony DSCRX100M3 Advanced Digital Compact Premium Camera with Large 1-inch Sensor, Bright High Quality Lens and...', u'http://ecx.images-amazon.com/images/I/41N9s54kYNL._AA160_.jpg', '14778', 569.0, 'NA', 'NA', 'NA', 'NA', 0.0, 4], [u'B00IE9X HE0', u'Sony ILCE6000LB Compact System Camera with SELP1650 Lens Kit (Fast Auto Focus, 24.3 MP, Electronic View Finder...', u'http://ecx.images-amazon.com/image s/I/411b0fwXcPL._AA160_.jpg', '7031', 489.0, 459.21, 451.77, 463.85, 459.55, 8.24, 6], [u'B00IGL9PJC', u'Sony DSCHX400V Digital Compact Bridge Camera with High Quality Lens (Electronic View Finder, 20.4 MP, 50x Optical...', u'http://ecx.ima ges-amazon.com/images/I/519vhRU+hOL._AA160_.jpg', '4759', 287.0, 283.79, 'NA', ' NA', 'NA', 1.13, 5], [u'B00BHXVWVU', u'Sony Alpha A58 Translucent Mirror Interch angeable Lens Camera with 18-55mm Lens (20MP)', u'http://ecx.images-amazon.com/i mages/I/5136KbAqI0L._AA160_.jpg', '2471', 294.9, 271.35, 284.76, 293.0, 289.13, 8.68, 5], [u'B00HR30ZQW', u'Sony DSCW830 Digital Compact Camera - Black (20.1MP, 8x Optical Zoom) 2.7 inch LCD', u'http://ecx.images-amazon.com/images/I/41Vyu8B k12L._AA160_.jpg', '6961', 77.89, 92.5, 92.5, 92.5, 92.5, 0.0, 4], [u'B00MTZI4Y8 ', u'Sony ILCE5100L Compact System Camera with 16-50 Lens (24.3 MP, 180 Degrees Tiltable LCD, Fast Hybrid Auto Focus...', u'http://ecx.images-amazon.com/images/ I/41lZIaql15L._AA160_.jpg', '7157', 391.99, 407.34, 442.2, 439.11, 385.77, 1.61, 8], [u'B010X7TG0Y', u'Sony DSCRX100M4 Advanced Digital Compact Premium Camera w ith High Speed Shutter, 4K Recording and Super Slow Motion...', u'http://ecx.ima ges-amazon.com/images/I/41eW0C302jL._AA160_.jpg', '15164', 749.0, 'NA', 'NA', 'N A', 'NA', 0.0, 4], [u'B008CNMZDW', u'Sony DSCRX100 Advanced Digital Compact Prem ium Camera with Large 1-inch Sensor and Bright High Quality Lens', u'http://ecx. images-amazon.com/images/I/41JNvHrzCAL._AA160_.jpg', 'NA', 319.0, 'NA', 'NA', 'N A', 'NA', 0.0, 4], [u'B00HNT5NG2', u'Sony ILCE5000L Compact System Camera with S EL-1650 Zoom Lens (20.1 MP, 180 Degrees Tiltable LCD, Wi-Fi and NFC...', u'http: //ecx.images-amazon.com/images/I/41AyLhZFIVL._AA160_.jpg', '5462', 249.0, 271.74 , 224.18, 287.04, 254.34, 11.07, 6], [u'B00WSIAE4Y', u'Sony DSCWX500 Digital Com pact High Zoom Travel Camera with 180 Degrees Tiltable LCD Screen (18.2 MP, 30 x Optical...', u'http://ecx.images-amazon.com/images/I/41hl7QCZq8L._AA160_.jpg', '3690', 202.27, 'NA', 'NA', 'NA', 'NA', 0.0, 4], [u'B00HH8A60C', u'Sony ILCE5000 L Compact System Camera with SEL-1650 Zoom Lens (20.1 MP, 180 Degrees Tiltable L CD, Wi-Fi and NFC...', u'http://ecx.images-amazon.com/images/I/51Qm1udYpNL._AA16 0_.jpg', '1164', 239.0, 270.57, 228.42, 252.8, 254.34, 4.63, 6], [u'B00IGL9PQA', u'Sony DSCH400 Digital Compact Bridge Camera (20.1 MP, 63x Optical High Zoom, E lectronic View Finder) - Black', u'http://ecx.images-amazon.com/images/I/51h80Gv w12L._AA160_.jpg', '1863', 158.99, 191.72, 266.71, 199.08, 229.61, 0.0, 4], [u'B 00G37XCVI', u'Sony DSCH300 Digital Compact Bridge Camera (20.1 MP, 35x Optical H igh Zoom) - Black', u'http://ecx.images-amazon.com/images/I/51ofKTbBPnL._AA160_. jpg', '606', 111.49, 'NA', 'NA', 'NA', 'NA', 0.0, 4], [u'B00IGL9PSS', u'Sony DSC HX60 Digital Compact High Zoom Travel Camera with Wi-Fi and NFC ( 20.4 MP, 30x O ptical Zoom) - Black', u'http://ecx.images-amazon.com/images/I/41W9E7oct4L._AA16 0_.jpg', '487', 167.49, 198.65, 198.65, 198.65, 198.65, 0.0, 4], [u'B00FYPUXPI', u'Sony DSCRX10 Advanced Digital Compact Bridge Camera with Large 1-inch Sensor and High Quality Lens (Tiltable LCD...', u'http://ecx.images-amazon.com/images/I /41xfTU+o5WL._AA160_.jpg', '32115', 538.99, 705.99, 741.43, 706.83, 'NA', 0.0, 4 ], [u'B003OUX6TA', u'Sony NEX5KB Alpha Compact System Camera - 18-55mm F3.5-5.6 OSS Lens - Black', u'http://ecx.images-amazon.com/images/I/51S+IxiJhzL._AA160_.j pg', u'128', 150.0, 'NA', 'NA', 'NA', 'NA', 0.0, 4], [u'B00WJLUKKI', u'Sony DSCH X90 Digital Compact High Zoom Travel Camera with 180 Degrees Tiltable LCD Screen and View Finder (18.2...', u'http://ecx.images-amazon.com/images/I/41eDm7aZaSL. _AA160_.jpg', '11112', 294.99, 'NA', 'NA', 'NA', 'NA', 0.0, 4], [u'B00FWUDEEC', u'Sony ILCE7B Full Frame Compact System Camera with 28-70 mm Zoom Lens ( 24.3 MP , 117 Points Hybrid AutoFocus, 3.0...', u'http://ecx.images-amazon.com/images/I/ 510OOSmhdnL._AA160_.jpg', '27498', 875.0, 'NA', 'NA', 'NA', 'NA', 0.0, 4], [u'B0 0IK01PJC', u'Sony DSCW800 Digital Compact Camera (20.1 MP, 5x Optical Zoom) - Bl ack', u'http://ecx.images-amazon.com/images/I/41JRFY5W6tL._AA160_.jpg', '69', 59.99, 72.51, 'NA', 80.95, 72.51, 0.0, 4], [u'B00MTZI376', u'Sony ILCE5100L Compac t System Camera - Black', u'http://ecx.images-amazon.com/images/I/51hKen+vrXL._A A160_.jpg', '2625', 344.99, 354.52, 374.91, 374.91, 360.98, 0.0, 4], [u'B00IGL9P Q0', u'Sony DSCWX350 Digital Compact Camera with Wi-Fi and NFC (18.2 MP, 20x Opt ical Zoom) - Black', u'http://ecx.images-amazon.com/images/I/41IwBcbgU4L._AA160_ .jpg', '4004', 138.99, 'NA', 186.18, 131.42, 'NA', 5.76, 7]]
    table = [t  for t in table if t.count('NA')<6]
    dd['table'] = table
    dd['status'] = True

def returnTableHTMl(table):
    tableString= '''<table class = "table table-bordered table-striped table-curved" id = "myTable">
                    <thead>
                                            <tr>
                                                <th>ASIN</th>
                                                <th>Title</th>
                                                <th>Image</th>
                                                <th>Sales Rank</th>
                                                <th>UK Price</th>
                                                <th>FR Price</th>
                                                <th>IT Price</th>
                                                <th>ES Price</th>
                                                <th>DE Price</th>
                                                <th>ROI (%)</th>
                                            </tr>
                                        </thead>
                    <tbody> '''
    
    for t in table:
        tableString +=""" <tr>"""
        count = -1
        for i in t:
            count +=1
            if t.index(i) !=10:
                if count ==2:
                    tableString += unidecode('''<td style='text-align:center;vertical-align:middle' height="50"><img src=''' +i+''' alt="" border="3"
                                        height="100" width="100" /></td>''')
                elif count ==4:
                    if count == t[10]:
                        tableString += unidecode('''<td style='text-align:center;vertical-align:middle' height="50" bgcolor="#66CDAA"
                                    > <a href="http://www.amazon.co.uk/dp/'''+str(t[0])+'''" target="_blank"><i>''' +returnPrice(i)+'''</i></a></td>''')
                    else:
                        tableString += unidecode('''<td style='text-align:center;vertical-align:middle' height="50" >
                                        <a href="http://www.amazon.co.uk/dp/'''+str(t[0])+'''" target="_blank"><i>''' +returnPrice(i)+'''</i></a></td>''')
                
                elif count ==5:
                    if count == t[10]:
                        tableString += unidecode('''<td style='text-align:center;vertical-align:middle' height="50" bgcolor="#66CDAA"
                                    > <a href="http://www.amazon.fr/dp/'''+str(t[0])+'''" target="_blank"><i>''' +returnPrice(i)+'''</i></a></td>''')
                    else:
                        tableString += unidecode('''<td style='text-align:center;vertical-align:middle' height="50" >
                                        <a href="http://www.amazon.fr/dp/'''+str(t[0])+'''" target="_blank"><i>''' +returnPrice(i)+'''</i></a></td>''')
                elif count ==6:
                    if count == t[10]:
                        tableString += unidecode('''<td style='text-align:center;vertical-align:middle' height="50" bgcolor="#66CDAA"
                                    > <a href="http://www.amazon.it/dp/'''+str(t[0])+'''" target="_blank"><i>''' +returnPrice(i)+'''</i></a></td>''')
                    else:
                        tableString += unidecode('''<td style='text-align:center;vertical-align:middle' height="50" >
                                        <a href="http://www.amazon.it/dp/'''+str(t[0])+'''" target="_blank"><i>''' +returnPrice(i)+'''</i></a></td>''')
                elif count ==7:
                    if count == t[10]:
                        tableString += unidecode('''<td style='text-align:center;vertical-align:middle' height="50" bgcolor="#66CDAA"
                                    > <a href="http://www.amazon.es/dp/'''+str(t[0])+'''" target="_blank"><i>''' +returnPrice(i)+'''</i></a></td>''')
                    else:
                        tableString += unidecode('''<td style='text-align:center;vertical-align:middle' height="50" >
                                        <a href="http://www.amazon.es/dp/'''+str(t[0])+'''" target="_blank"><i>''' +returnPrice(i)+'''</i></a></td>''')
                elif count ==8:
                    if count == t[10]:
                        tableString += unidecode('''<td style='text-align:center;vertical-align:middle' height="50" bgcolor="#66CDAA"
                                    > <a href="http://www.amazon.de/dp/'''+str(t[0])+'''" target="_blank"><i>''' +returnPrice(i)+'''</i></a></td>''')
                    else:
                        tableString += unidecode('''<td style='text-align:center;vertical-align:middle' height="50" >
                                        <a href="http://www.amazon.de/dp/'''+str(t[0])+'''" target="_blank"><i>''' +returnPrice(i)+'''</i></a></td>''')
                        
                else:
                    if count == t[10]:
                        tableString += unidecode('''<td style='text-align:center;vertical-align:middle' height="50"
                             bgcolor="#66CDAA" >''' + str(i) +'''</td>''')
                    else:
                        tableString += unidecode('''<td style='text-align:center;vertical-align:middle' height="50"
                                >''' + str(i) +'''</td>''')
        
        tableString += """</tr>"""   

    tableString += """</tbody></table>"""
    f = open('tableString.txt', 'wb')
    f.write(tableString)
    f.close()
    
     
    return tableString
    
def returnPrice(i):
    if i != 'NA':
        return '&pound;'+str(i)
    else:
        return str(i)
    
@app.route('/downloadCSV')
def download():
    """ flask view for download CSV """
    output = excel.make_response_from_array(dd['table'], 'csv')
    output.headers["Content-Disposition"] = "attachment; filename=export.csv"
    output.headers["Content-type"] = "text/csv"
    return output 
    
# start the server with the 'run()' method
if __name__ == '__main__':
    WSGIRequestHandler.protocol_version = "HTTP/1.1"
    #logging.basicConfig(filename='/var/www/amazoneu/debug.log',level=logging.DEBUG, format='%(asctime)s.%(msecs)d %(levelname)s %(module)s - %(funcName)s: %(message)s', datefmt="%Y-%m-%d %H:%M:%S")
    app.run(debug=True)
