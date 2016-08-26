import requests, re
from bs4 import BeautifulSoup

asin = 'B00NVDNDUW'

url = 'http://www.amazon.co.uk/dp/' + asin
response = requests.get(url, headers={'User-agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36'})
soup = BeautifulSoup(response.content)
##tags = {}
##for li in soup.select('table#productDetailsTable div.content ul li'):
##    try:
##        title = li.b
##        key = title.text.strip().rstrip(':')
##        value = title.next_sibling.strip()
##
##        tags[key] = value
##    except AttributeError:
##        break


from bs4 import BeautifulSoup
import requests

url = 'http://www.amazon.com/dp/0439136369'
response = requests.get(url, headers={'User-agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36'})

soup = BeautifulSoup(response.content)
x = soup.find(attrs = {'class':'average_customer_reviews'})
    
def get_proxies(self):
    # called in init to set self.proxies
    proxies = []
    with open('proxies.txt', 'r') as f:
        # strip \n from proxies
        proxies = [proxy.strip() for proxy in f]
    return proxies


def get_post(self, url, timeout=15):
    # return html of url using a random proxy from the list
    proxy = random.choice(self.proxies)
    html = requests.get(url, headers=self.headers, 
               proxies={'http': 'http://' + proxy, 
               'https': 'http://' + proxy},   
               timeout=timeout
                )
    return html
