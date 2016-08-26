import mechanize
from mechanize import Browser
from bs4 import BeautifulSoup

url = 'http://www.amazon.co.uk/dp/B00NVDNDUW'

mech = Browser()
page = mech.open(url)
html = page.read()
soup = BeautifulSoup(html)
#data = BeautifulSoup.extract(soup)

def extract(soup):
    table = soup.find("table",attrs={'id':'ctl00_TemplateBody_WebPartManager1_gwpste_container_SearchForm_ciSearchForm_RTable'})
    #print table
    data = []
    for row in table.findAll("tr"):
        s = row.getText()
        data.append(s)
    salesRankElem = data.find(attrs = {'id':'SalesRank'}).find(attrs = {'class' : 'value'}).getText()
    salesRank =  re.findall(r'\d+\sin', salesRankElem)[0].replace('in','').strip()
    return int(salesRank)

data = BeautifulSoup.extract(soup)
