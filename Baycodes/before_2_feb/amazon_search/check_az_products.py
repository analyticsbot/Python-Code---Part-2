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

def getAmazonProducts(product, pg_max):
    url = 'http://www.amazon.co.uk/s/ref=nb_sb_noss?url=search-alias%3Daps&field-keywords=' +  '+'.join(product.split())
    pg_num = 1
    #pg_max = 1

    while True:
        if pg_num == 5:
            url = url
            pg_num += 1
        else:
            if pg_num == (pg_max + 1):
                print pg_num, (pg_max + 1), pg_max
                break
            url = 'http://www.amazon.co.uk/s/ref=sr_pg_' + str(pg_num) + '?rh=i%3Aaps%2Ck%3A' + '+'.join(product.split()) + '&page=' + str(pg_num) + '&keywords'+  '+'.join(product.split())
            pg_num += 1
        print url    
        response = requests.get(url, headers={'User-agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36'})
        soup = BeautifulSoup(response.content, "lxml")

        elements = soup.findAll(attrs = {'class': 's-result-item celwidget'})
        #print elements
        prod = {'numProducts' : len(elements)}

        for elem in elements:
            try:
                title = elem.find(attrs = {'class' : 'a-size-medium a-color-null s-inline s-access-title a-text-normal'}).getText()
            except Exception,e:
                print str(e)
                title = 'NA'
            try:
                url = elem.find(attrs = {'class' : 'a-link-normal s-access-detail-page  a-text-normal'}).attrs['href']
            except Exception,e:
                print str(e)
                url = 'NA'
            try:
                price_old = re.findall(r'\d+.\d+', elem.find(attrs = {'class' : 'a-size-small a-color-secondary a-text-strike'}).getText())[0]
            except Exception,e:
                print str(e)
                price_old = 'NA'
            try:
                price_new = re.findall(r'\d+.\d+', elem.find(attrs = {'class': 'a-size-base a-color-price s-price a-text-bold'}).getText())[0]
            except Exception,e:
                print str(e)
                price_new = 'NA'
            try:
                image = elem.find(attrs = {'class' : 'a-column a-span12 a-text-center'}).find(attrs = {'class' : 's-access-image cfMarker'}).attrs['src']
            except Exception,e:
                print str(e)
                image = 'NA'
            try:
                asin = re.findall(r'dp\/(.*?)\/', url)[0]
            except Exception,e:
                print str(e)
                asin =  'NA'

            prod['product' + str(elements.index(elem))] = {'title':title, 'url':url, 'price_old':price_old, 'price_new':price_new, 'image':image,\
                                                       'asin': asin}
    return prod

hh = getAmazonProducts('lego', 2)
