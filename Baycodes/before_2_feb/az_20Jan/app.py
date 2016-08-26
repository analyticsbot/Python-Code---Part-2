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

# create the application object
app = Flask(__name__)
app.secret_key = "/\xfa-\x84\xfeW\xc3\xda\x11%/\x0c\xa0\xbaY\xa3\x89\x93$\xf5\x92\x9eW}"
app.jinja_env.add_extension('jinja2.ext.loopcontrols')
try:
    file_handler = FileHandler("/var/www/amazoneu/debug.log","a")
except Exception,e:
    print str(e)
    file_handler = FileHandler("debug.log","a")
file_handler.setLevel(logging.DEBUG)
app.logger.addHandler(file_handler)
#app.WTF_CSRF_SECRET_KEY  = "amazoneuapp"
#app.CSRF_ENABLED = True
app.debug = True

try:
    if os.environ['Production'] == 'True':
        app.debug = False
except Exception,e:
    print str(e)

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
    url = ('https://currency-api.appspot.com/api/%s/%s.json') % (curr_from, curr_to)
    r = requests.get(url)
    return r.json()['rate']

# list of available user agents
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
    """ method to return a random user agent from the above list """
    return choice(user_agents)

def check_proxy(session):
    """ method to return a working proxy else return NA. No proxy will be used then.
    Code looks at the current ip at http://canihazip.com/s and compares with the random ip picked.
    if both match, proxy is returned, else retry is done until PROXY_MAX_TRY times
    session : request module's session
    """
    count = 0
    while True:
        count +=1
        proxy_host = random_proxy()
        response = session.get('https://api.ipify.org')
        returned_ip = response.text
        if returned_ip == proxy_host:
            return proxy_host
            break
        elif count == PROXY_MAX_TRY:
            return 'NA'
            break
        
def getAmazonProducts(product, pg_max):
    """ method to return the products on amazon.co.uk for the product searched
    product : search term entered by the user
    pg_max : maximum number of search results to be scraped
    """
    url = 'http://www.amazon.co.uk/s/ref=nb_sb_noss?url=search-alias%3Daps&field-keywords=' +  '+'.join(product.split())
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
            url = 'http://www.amazon.co.uk/s/ref=sr_pg_' + str(pg_num) + '?rh=i%3Aaps%2Ck%3A' + '+'.join(product.split()) + '&page=' + str(pg_num) + '&keywords'+  '+'.join(product.split())
            pg_num += 1

        session = requests.Session()
        session.headers = random_user_agent()
        
        proxy = check_proxy(session) # checks for a working proxy, else proceeds with the current ip
        if proxy != 'NA':
            session.proxies = {'http': proxy}

        # retreived the response and pass to beautifulsoup
        response = session.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        
        # get all the products on the search page
        elements = soup.findAll(attrs = {'class': 's-result-item celwidget'})
        prod['numProducts'] += len(elements) # increment the number of products

        # loop through the elements and get title, url, price_old, price_new, image url, asin and add to a dict object
        for elem in elements:
            try:
                title = elem.find(attrs = {'class' : 'a-size-medium a-color-null s-inline s-access-title a-text-normal'}).getText()
            except Exception,e:
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
                price_new = re.findall(r'\d+.\d+', elem.find(attrs = {'class': 'a-size-base a-color-price s-price a-text-bold'}).getText())[0]
            except Exception,e:
                price_new = 'NA'
            try:
                image = elem.find(attrs = {'class' : 'a-column a-span12 a-text-center'}).find(attrs = {'class' : 's-access-image cfMarker'}).attrs['src']
            except Exception,e:
                image = 'NA'
            try:
                asin = re.findall(r'dp\/(.*?)\/', url)[0]
            except Exception,e:
                asin =  'NA'

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

    try:
        price =  soup.find(attrs = {'class': 'a-row a-spacing-mini olpOffer'}).\
            find(attrs = {'class' : 'a-size-large a-color-price olpOfferPrice a-text-bold'}).getText().strip()[1:].replace('UR', '')
    
        result = float(price.replace(',','.'))
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
    temp.extend([asin, title, image])
    if asin !='NA':
        sales_rank_check, salesRank = getSalesRank(salesRankFrom, asin, salesRankTo)
        if sales_rank_check:
            temp.append(salesRank)
            prices = combine(asin)
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
                if (finalPrices[0] != 'NA') and (min(finalPrices) != 'NA'):
                    roi = ((finalPrices[0] - min(finalPrices))/min(finalPrices))*100
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
            table = [t  for t in table if ((t.count('NA')<3) and (len(t)==10))]
            print len(table)
            session['table'] = table
            

        else:
            errors =  {'error': 'search term required'}
        
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
    logging.basicConfig(filename='/var/www/amazoneu/debug.log',level=logging.DEBUG, format='%(asctime)s.%(msecs)d %(levelname)s %(module)s - %(funcName)s: %(message)s', datefmt="%Y-%m-%d %H:%M:%S")
    app.run(debug=True)
