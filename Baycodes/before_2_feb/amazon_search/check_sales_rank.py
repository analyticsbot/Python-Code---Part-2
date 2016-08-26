from flask import Flask, render_template, request
from bs4 import BeautifulSoup
import requests, random
from amazon.api import AmazonAPI
from flask_table import Table, Col
import threading, re
from selenium import webdriver
from threading import Thread
import Queue
import mechanize
from mechanize import Browser
from random import choice

salesRankFrom = 100
asin = 'B00NVDNDUW'
asin = 'B00NVDMREA'
salesRankTo = 200
url = 'http://www.amazon.co.uk/dp/' + asin
print url
mech = Browser()
#proxy = random_proxy()  # will be proxies.random_proxy()
session = requests.Session()

mech.set_proxies({'http': 'http://202.50.176.212:8080'})
page = mech.open(url)
html = page.read()
soup = BeautifulSoup(str(html))
data = BeautifulSoup.extract((soup))
#print str(data)[1:100]
salesRankElem = data.find(attrs = {'id':'SalesRank'}).find(attrs = {'class' : 'value'}).getText()
salesRank =  re.findall(r'\n(.*?)\sin', salesRankElem)[0].replace('in','').replace(',','').strip()
print salesRank
print salesRankFrom <= int(salesRank) <= salesRankTo
