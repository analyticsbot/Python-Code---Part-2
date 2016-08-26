import requests, shutil, time, datetime, random, sqlite3
from threading import Thread
import requests, re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

INPUT_FILE = 'keywords.csv'
# credentials
email = 'susan@notaisltd.com'
password = '1BS1lse2s'
# url for login        
url = 'https://www.merchantwords.com/login'
## add headers
headers = {'content-type': 'application/json', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
debug = True # print status
numThreads = 5
CHANGE_PROXY_EVERY_N_REQUESTS = 5
dd = {}
PROXY_RENEW_INTERVAL = 1800 #seconds

f = open(INPUT_FILE, 'rb')
data = f.read().split('\n')[:-1]
data = [d.strip() for d in data]
if debug: print 'Keyword data read form the csv file. Total keywords :: ', len(data)

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

    ## add proxies from samair
    primary_url = "http://www.samair.ru/proxy/proxy-00.htm"
    urls = []

    for i in range(1, 31):
        if i < 10:
                urls.append(primary_url.replace("00", "0" + str(i)))
        else:
                urls.append(primary_url.replace("00", str(i)))

    for url in urls:
        try:
            session = requests.session()
            headers = {'Host': 'www.proxylisty.com',
                     'Connection': 'keep-alive',
                     'Cache-Control': 'max-age=0',
                     'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                     'Upgrade-Insecure-Requests': '1',
                     'User-agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
                     'Referer': 'https://www.google.co.in/',
                     'Accept-Encoding':'gzip, deflate, sdch',
                     'Accept-Language':'en-US,en;q=0.8'}

            response = session.get(url, headers = headers)
            soup = BeautifulSoup(response.content, "lxml")
            link = 'http://www.samair.ru' + soup.find(attrs = {'id':'ipportonly'}).find('a')['href']
            response = session.get(link, headers = headers)
            soup = BeautifulSoup(response.content, "lxml")
            ips = soup.find(attrs = {'id':'content'}).getText().split('\n')
            for ip in ips:
                proxy.append('http://' + ip)
        except:
            pass

    ## get proxies from hidemyass
    driver = webdriver.Firefox()
    driver.get("http://proxylist.hidemyass.com/")
    proxys = driver.find_elements_by_xpath('/html/body/section/section[4]/section[1]/div/table/tbody/tr/td[2]')
    ports = driver.find_elements_by_xpath('/html/body/section/section[4]/section[1]/div/table/tbody/tr/td[3]')
    for ip in proxys:
        try:
            proxy.append('http://' + ip.text+ ':'+ ports[proxys.index(ip)].text)
        except:
            pass
    driver.close()
    dd['stop'] = False
    if debug: print('Total proxies downloaded', len(proxy))
    return proxy
    
dd['pp'] = getProxies()

proxy_start = datetime.datetime.now()

def renewProxies(debug, PROXY_RENEW_INTERVAL):
    while True:
        proxy_now = datetime.datetime.now()
        if int((proxy_now-proxy_start).seconds)%PROXY_RENEW_INTERVAL==0:
            if debug: print 'Renewing Proxies...', '\n'
            dd['pp'] = getProxies()
    
def getKeywords(thread_data, thread, dd, debug, email, password, CHANGE_PROXY_EVERY_N_REQUESTS):
    conn = sqlite3.connect('downloaded_keywords_' + str(thread) + '.db', check_same_thread = False)
    if debug: print "[+] Opened database connection successfully for thread :: ", thread, '\n'
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

    if debug: print 'Logged in for thread', thread, '\n'

    a = datetime.datetime.now()
    
    count = 0
    ## request file
    for key in thread_data:
        try:            
            while True:
                if dd['stop']:
                    pass
                elif not dd['stop']:
                    break

            c.execute("SELECT * FROM d_keywords WHERE keyword = '%s'" % key)
            rows = c.fetchone()

            if rows == None:
                if debug: print 'Working on thread', thread, '\n'
                count +=1
                if count % CHANGE_PROXY_EVERY_N_REQUESTS==0:
                    proxies = {'http': random.choice(dd['pp'])}

                if count % 100:
                    print 'Downloaded ', count, ' keywords for thread', thread, '\n'
                
                url_key = 'https://www.merchantwords.com/search/' + '-'.join(key.split()) + '.csv'
                r = s.get(url_key, stream=True, headers = headers, proxies=proxies)
                
                if (r.status_code == 200) and ('Hang' not in r.content):
                    if debug: print 'getting data for', key, ' for thread', thread, '\n'
                    c.execute("INSERT INTO d_keywords (keyword) values(?)", (key, ))
                    conn.commit()
                    with open('dd\\' + '-'.join(key.split()) + '.txt', 'wb') as f:
                        f.write(r.content)
                else:
                    if debug: print 'Error. Server didnt respond well', '\n'
                    while True:
                        time.sleep(2)
                        proxies = {'http': random.choice(dd['pp'])}
                        r = s.get(url_key, stream=True, headers = headers, proxies=proxies)
                        if (r.status_code == 200) and ('Hang' not in r.content):
                            break
        except Exception,e:
            if debug: print 'Error', str(e)

    b = datetime.datetime.now()
    c = b - a
    if debug: print 'Took', (c.seconds/60), ' minutes for thread', thread, ' to download', len(thread_data), ' keywords'

threads = []

for i in range(1, numThreads+1):
    keywords_each_thread = len(data)/(numThreads+1)
    thread_data = data[keywords_each_thread*(i-1):keywords_each_thread*i]
    threads.append(Thread(target = getKeywords, args=(thread_data, i, dd, debug, \
                                                      email, password, CHANGE_PROXY_EVERY_N_REQUESTS)))
    threads.append(Thread(target = renewProxies, args=(debug, PROXY_RENEW_INTERVAL)))

## start the threads
for t in threads:
    t.start()
if debug: print 'All threads started'
## wait for threads to stop
for t in threads[:-1]:
    t.join()

