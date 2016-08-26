import requests
from bs4 import BeautifulSoup
from apscheduler.schedulers.blocking import BlockingScheduler
import logging
import MySQLdb

# Open database connection
db = MySQLdb.connect("localhost","user","pass123","amazon")

# prepare a cursor object using cursor() method
cursor = db.cursor()

# initialize the scheduler
sched = BlockingScheduler(misfire_grace_time = 100)

primary_url = "http://www.samair.ru/proxy/proxy-00.htm"
urls = []
n_proxies = 0
n_working_proxies = 0
PROXY_MAX_TRY = 10

def check_proxy(session, proxy):
    """ method to return a working proxy else return NA. No proxy will be used then.
    Code looks at the current ip at http://canihazip.com/s and compares with the random ip picked.
    if both match, proxy is returned, else retry is done until PROXY_MAX_TRY times
    session : request module's session
    """
    count = 0
    while True:
        count +=1
        response = session.get('https://api.ipify.org')
        returned_ip = response.text
        if returned_ip == proxy:
            return proxy, True
            break
        elif count == PROXY_MAX_TRY:
            return False
            break

for i in range(1, 31):
    if i < 10:
            urls.append(primary_url.replace("00", "0" + str(i)))
    else:
            urls.append(primary_url.replace("00", str(i)))

def getProxies(n_proxies, n_working_proxies):
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
            soup = BeautifulSoup(response.content, "html.parser")
            link = 'http://www.samair.ru' + soup.find(attrs = {'id':'ipportonly'}).find('a')['href']
            print link
            response = session.get(link, headers = headers)
            soup = BeautifulSoup(response.content, "html.parser")
            ips = soup.find(attrs = {'id':'content'}).getText().split('\n')
            n_proxies += len(ips)
            working_ips = []
            for ip in ips:                
                print 'http://' + ip
                # Prepare SQL query to INSERT a record into the database.
                sql = "INSERT INTO proxies(proxy) \
                       VALUES ('%s')" % \
                       ('http://' + ip)
                try:
                   # Execute the SQL command
                   cursor.execute(sql)
                   # Commit your changes in the database
                   db.commit()
                except Exception,e:
                   # Rollback in case there is any error
                   db.rollback()
   
            n_working_proxies += len(working_ips)
            # write to csv or put in a db here #
            
        except Exception, e:        
            print str(e)

if __name__ == '__main__':
    
    @sched.scheduled_job('interval', minutes=30)
    
    def timed_job():
        logging.basicConfig()
        print('Getting proxies!!')           
        getProxies(n_proxies, n_working_proxies)
        # disconnect from server
        db.close()
        
    sched.start()

print 'total proxies grabbed from samair ::' , n_proxies
print 'total working proxies grabbed from samair ::' , n_working_proxies
