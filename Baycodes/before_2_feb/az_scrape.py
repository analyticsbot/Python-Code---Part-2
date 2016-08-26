import requests, re
from bs4 import BeautifulSoup

product = 'lego'
product = 'papa'

url = 'http://www.amazon.co.uk/s/ref=nb_sb_noss_1?url=search-alias%3Daps&field-keywords=' +  product
response = requests.get(url, headers={'User-agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36'})
soup = BeautifulSoup(response.content)

elements = soup.findAll(attrs = {'class': 's-result-item celwidget'})

prod = {}

for elem in elements:
    try:
        title = elem.find(attrs = {'class' : 'a-size-medium a-color-null s-inline s-access-title a-text-normal'}).getText()
    except:
        title = 'NA'
    try:
        url = elem.find(attrs = {'class' : 'a-link-normal s-access-detail-page  a-text-normal'}).attrs['href']
    except:
        url = 'NA'
    try:
        price_old = re.findall(r'\d+.\d+', elem.find(attrs = {'class' : 'a-size-small a-color-secondary a-text-strike'}).getText())[0]
    except:
        price_old = 'NA'
    try:
        price_new = re.findall(r'\d+.\d+', elem.find(attrs = {'class': 'a-size-base a-color-price s-price a-text-bold'}).getText())[0]
    except:
        price_new = 'NA'
    try:
        image = elem.find(attrs = {'class' : 'a-column a-span12 a-text-center'}).find(attrs = {'class' : 's-access-image cfMarker'}).attrs['src']
    except:
        image = 'NA'
    try:
        asin = re.findall(r'dp\/(.*?)\/', url)[0]
    except:
        asin =  'NA'

    prod['product' + str(elements.index(elem))] = {'title':title, 'url':url, 'price_old':price_old, 'price_new':price_new, 'image':image,\
                                                   'asin': asin}
