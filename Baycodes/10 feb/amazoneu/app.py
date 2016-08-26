# import the Flask class from the flask module and other required modules
from flask import Flask, render_template, request, make_response, session, url_for, jsonify
from bs4 import BeautifulSoup
import requests, threading, re, os, Queue, mechanize, logging, gc
from random import choice 
from threading import Thread
from mechanize import Browser
from flask.ext import excel
from unidecode import unidecode       
from logging import FileHandler
from amazon.api import AmazonAPI
from werkzeug.serving import WSGIRequestHandler

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
        queue.put(['NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA'])

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
        
        if (searchterm != ''):
            gc.collect()
            products = getAmazonProducts(searchterm, maxPages)
            
            table = []
            count = 1
            while True:
                table.extend(main({k: products[k] for k in products.keys()[18*(count-1):18*(count)] if k != 'numProducts' }, priceFrom, priceTo, \
                                  salesRankFrom, salesRankTo))                
                if (count*18)>=products['numProducts']:
                    break
                count +=1
                        
            session['table'] = table
            print len(table)# , '\n', table

        else:
            errors =  {'error': 'search term required'}
        print searchterm
        return render_template('index.html', title = 'Search Results for ' + searchterm + ' | Page ', table = table, errors = errors,
                           searchterm = searchterm, maxPages = maxPages, priceFrom = priceFrom, priceTo = priceTo,
                           salesRankFrom = salesRankFrom, salesRankTo = salesRankTo)



@app.route('/downloadCSV')
def download():
    """ flask view for download CSV """
    output = excel.make_response_from_array(session['table'], 'csv')
    output.headers["Content-Disposition"] = "attachment; filename=export.csv"
    output.headers["Content-type"] = "text/csv"
    return output 
    
# start the server with the 'run()' method
if __name__ == '__main__':
    WSGIRequestHandler.protocol_version = "HTTP/1.1"
    #logging.basicConfig(filename='/var/www/amazoneu/debug.log',level=logging.DEBUG, format='%(asctime)s.%(msecs)d %(levelname)s %(module)s - %(funcName)s: %(message)s', datefmt="%Y-%m-%d %H:%M:%S")
    app.run(debug=True)
