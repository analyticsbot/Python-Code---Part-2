import requests, shutil, time, datetime, random, sqlite3
from threading import Thread
import requests, re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

INPUT_FILE = 'keywords.csv'
# credentials
email ='susan@notaisltd.com'
password ='1BS1lse2s'

# url for login        
url = 'https://www.merchantwords.com/login'
## add headers
headers = {'content-type': 'application/json', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


f = open(INPUT_FILE, 'rb')
data = f.read().split('\n')[:-1]
data = [d.strip() for d in data][:1]


s = requests.session()
auth = ('rbot', 'myname')
proxies = {'http': 'http://us-ca.proxymesh.com:31280'}
login_data = dict(email=email, password=password)
s.post(url, data=login_data,  proxies=proxies, auth=auth)
debug = True
if debug: print 'Logged in for thread', '\n'

a = datetime.datetime.now()

count = 0
## request file
for key in data:
    count = 0
    continue_ = True
    while continue_:
        count += 1
        url_key = 'https://www.merchantwords.com/search/' + '-'.join(key.split())+'/page-' + str(count)
        print url_key
        r = s.get(url_key, stream=True, headers = headers, proxies=proxies)
        
        if (r.status_code == 200) and ('Hang' not in r.content):
            if debug: print 'getting data for', key, ' for thread', '\n'
            
            soup = BeautifulSoup(r.content, "html")
            #print soup.find_all('tr')
            f = open('dk\\' + '-'.join(key.split()) + '.txt', 'wb')
            for tr in soup.find(attrs = {'class':'span8 offset2'}).find_all('tr'):
                tds = tr.find_all('td')
                try:
                    if tds[1].text !='':
                        print tds[0].text + ',' + tds[1].text+',' + tds[2].text
                        f.write(tds[0].text + ',' + tds[1].text+',' + tds[2].text + '\n')
                    else:
                        print tds[0].text + ',' + '<100'+',' + tds[2].text
                        f.write(tds[0].text + ',' + '<100'+',' + tds[2].text + '\n')
                except Exception,e:
                    #print str(e)
                    pass
            if len(soup.find(attrs = {'class':'span8 offset2'}).find_all('tr'))==0:
                continue_ = False
        else:
            if debug: print 'Error. Server didnt respond well', '\n'
            while True:
                time.sleep(2)
                proxies = {'http': random.choice(dd['pp'])}
                r = s.get(url_key, stream=True, headers = headers, proxies=proxies)
                if (r.status_code == 200) and ('Hang' not in r.content):
                    break

