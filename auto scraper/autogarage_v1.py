import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

cols = ['email', 'mobile', 'address', 'website', 'rating', 'company_name']
df = pd.DataFrame(columns = cols)

url = 'http://www.autogarage.nl/auto/'
response = requests.get(url)
soup = bs(response.text)

segments = soup.findAll(attrs = {'class' : 'section'})

for seg in segments:
    pg_href = seg.find_all('a', href=True)
    if len(pg_href)>0:
        pg_link = 'http://www.autogarage.nl' + pg_href[0]['href']
        company_name, mobile, address, website, email, phone = getItem(pg_link)
        nrow = df.shape[0]
        df.loc[nrow+1] = [company_name, mobile, address, website, email, phone]


def getItem(pg_url):
    resp_pg = requests.get(pg_url)
    soup_pg = bs(resp_pg.text)
    try:
        company_name = soup_pg.find(attrs = {'class' : 'heading'}).getText().replace('\n','')
    except:
        company_name = 'NA'
    try:
        mobile = soup_pg.findAll(attrs = {'class' : 'tel'})[0].getText().replace('\n','')
    except:
        mobile = 'NA'
    try:
        address = soup_pg.find(attrs = {'class' : 'street-address'}).getText().replace('\n','') +\
              ' ' + soup_pg.find(attrs = {'class' : 'postal-code'}).getText().replace('\n','') +\
              ' ' + soup_pg.find(attrs = {'class' : 'locality'}).getText().replace('\n','')
    except:
        address = 'NA'
    try:
        website = soup_pg.find(attrs = {'class' : 'url'}).getText().replace('\n','')
    except:
        website = 'NA'
    try:
        email = soup_pg.find(attrs = {'class' : 'email'}).getText().replace('\n','').\
            replace('E-mail algemeen:','')
    except:
        email = 'NA'
    try:
        phone = soup_pg.findAll(attrs = {'class' : 'tel'})[1].getText().replace('\n','')
    except:
        try:
            phone = soup_pg.findAll(attrs = {'class' : 'tel'})[0].getText().replace('\n','')
        except:
            pass
    return company_name, mobile, address, website, email, phone
    
while True:
    n = 1
    try:
        n +=1
        url_nx = 'http://www.autogarage.nl/pager/'
        headers = {'User-Agent': 'Mozilla/5.0'}
        payload = {'query':'','city':'', 'page':n,'origin':'wizard','part1':'',\
                   'part2':''}
        session = requests.Session()
        resp = session.get(url_nx,headers=headers)

        # did this for first to get the cookies from the page, stored them with next line:
        cookies = requests.utils.cookiejar_from_dict(requests.utils.dict_from_cookiejar(session.cookies))
        resp = session.post(url_nx,headers=headers,data=payload,cookies =cookies)
        soup = bs(resp.text)

        segments = soup.findAll(attrs = {'class' : 'section'})

        for seg in segments:
            pg_href = seg.find_all('a', href=True)
            if len(pg_href)>0:
                pg_link = 'http://www.autogarage.nl' + pg_href[0]['href']
                company_name, mobile, address, website, email, phone = getItem(pg_link)
                #print company_name, mobile, address, website, email, phone
                nrow = df.shape[0]
                df.loc[nrow+1] = [company_name, mobile, address, website, email, phone]
        
    except Exception,e:
        print str(e)
        break

df.to_csv('autogarage.csv')
