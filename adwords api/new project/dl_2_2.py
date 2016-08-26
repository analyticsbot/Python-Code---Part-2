import requests, shutil, time, datetime, random, sqlite3
from threading import Thread
import requests, re
from bs4 import BeautifulSoup

INPUT_FILE = 'keywords.csv'
# credentials
email = 'susan@notaisltd.com'
password = '1BS1lse2s'
# url for login        
url = 'https://www.merchantwords.com/login'
## add headers
headers = {'content-type': 'application/json', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
debug = False # print status
numThreads = 5
CHANGE_PROXY_EVERY_N_REQUESTS = 5
dd = {}
PROXY_RENEW_INTERVAL = 1800 #seconds

f = open(INPUT_FILE, 'rb')
data = f.read().split('\n')[:-1]
data = [d.strip() for d in data]

## function to get the list of proxies
def getProxies():
    dd['stop'] = True
    proxy = []
    url = 'https://free-proxy-list.net/'
    response = requests.get(url)
    html = response.content

    templs = re.findall(r'<tr><td>(.*?)</td><td>', html)
    templs2 = re.findall(r'</td><td>[1-99999].*?</td><td>', html)

    for i in range(len(templs)):
        proxy.append('http://' + (templs[i] + ":" + templs2[i].replace('</td><td>', '')))
    
    return proxy
    dd['stop'] = False
    
dd['pp'] = getProxies()
proxy_start = datetime.datetime.now()

def renewProxies(debug, PROXY_RENEW_INTERVAL):
    proxy_now = datetime.datetime.now()
    if (proxy_now-proxy_start)%PROXY_RENEW_INTERVAL:
        if debug: print 'Renewing Proxies'
        dd['pp'] = getProxies()
    
def getKeywords(thread_data, thread, dd, debug, email, password, CHANGE_PROXY_EVERY_N_REQUESTS):
    conn = sqlite3.connect('downloaded_keywords_' + str(thread) + '.db', check_same_thread = False)
    if debug: print "[+] Opened database connection successfully for thread :: ", thread
    c = conn.cursor()

    ## try to create the table if it does not exists
    try:
        c.execute("create table d_keywords(keyword TEXT);")
        conn.commit()
    except:
        pass
    
    ## login to merchant site
    s = requests.session()
    auth = ('rbot', 'myname')
    proxies = {'http': 'http://us-ca.proxymesh.com:31280'}
    login_data = dict(email=email, password=password)
    s.post(url, data=login_data,  proxies=proxies, auth=auth)

    if debug: print 'Logged in for thread', thread

    a = datetime.datetime.now()
    
    count = 0
    ## request file
    for key in thread_data:
        while True:
            if dd['stop']:
                pass
            elif not dd['stop']:
                break
        count +=1
        if count % CHANGE_PROXY_EVERY_N_REQUESTS==0:
            proxies = {'http': random.choice(dd['pp'])}
        
        url_key = 'https://www.merchantwords.com/search/' + '-'.join(key.split()) + '.csv'
        r = s.get(url_key, stream=True, headers = headers, proxies=proxies)
        
        if (r.status_code == 200) and ('Hang' not in r.content):
            if debug: print 'getting data for', key, ' for thread', thread
            with open('-'.join(key.split()) + '.txt', 'wb') as f:
                f.write(r.content)
        else:
            if debug: print 'Error. Server didnt respond well'
            while True:
                time.sleep(10)
                proxies = {'http': random.choice(dd['pp'])}
                r = s.get(url_key, stream=True, headers = headers, proxies=proxies)
                if (r.status_code == 200) and ('Hang' not in r.content):
                    break

    b = datetime.datetime.now()
    c = b - a
    if debug: print 'Took', (c.seconds/60), ' minutes for thread', thread, ' to download', len(thread_data), ' keywords'

for i in range(1, numThreads+1):
    keywords_each_thread = len(data)/(numThreads+1)
    thread_data = data[keywords_each_thread*(i-1):keywords_each_thread*i]
    threads.append(Thread(target = getKeywords, args=(thread_data, i, dd, debug, \
                                                      email, password, CHANGE_PROXY_EVERY_N_REQUESTS)))
    threads.append(Thread(target = renewProxies, args=(debug, PROXY_RENEW_INTERVAL)))
    ## start the threads
    for t in threads:
        t.start()

    ## wait for threads to stop
    for t in threads[:-1]:
        t.join()

