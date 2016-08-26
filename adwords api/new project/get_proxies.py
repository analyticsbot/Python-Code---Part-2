import requests, re
from bs4 import BeautifulSoup

url = 'https://free-proxy-list.net/'
response = requests.get(url)
html = response.content

templs = re.findall(r'<tr><td>(.*?)</td><td>', html)
templs2 = re.findall(r'</td><td>[1-99999].*?</td><td>', html)

for i in range(len(templs)):
    print ('http://' + (templs[i] + ":" + templs2[i].replace('</td><td>', '')))
    
