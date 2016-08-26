from mechanize import Browser
import requests
from bs4 import BeautifulSoup

asin = 'B012NODIJA'

url1 = 'http://www.amazon.co.uk/gp/offer-listing/{ASIN}/ref=dp_olp_new?ie=UTF8&condition=new'.replace('{ASIN}', asin)
url2 = 'http://www.amazon.fr/gp/offer-listing/{ASIN}/ref=dp_olp_new?ie=UTF8&condition=new'.replace('{ASIN}', asin)
url3 = 'http://www.amazon.it/gp/offer-listing/{ASIN}/ref=dp_olp_new?ie=UTF8&condition=new'.replace('{ASIN}', asin)
url4 = 'http://www.amazon.es/gp/offer-listing/{ASIN}/ref=dp_olp_new?ie=UTF8&condition=new'.replace('{ASIN}', asin)

def getPriceAmazon(url):
    """ method to get the lowest FBA price for a asin from AZ IT, FR, ES, and UK pages 
    url : url for the amazon website. ASIN is replaced.
    queue : a queue to which the value is stored
    """
    session = requests.Session()
    
    #session.headers = random_user_agent()
    proxy = 'NA'

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
    
    print url, result

getPriceAmazon(url1)
##getPriceAmazon(url2)
##getPriceAmazon(url3)
##getPriceAmazon(url4)
