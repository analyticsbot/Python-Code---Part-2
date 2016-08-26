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


def getPriceAmazon(url, queue):
    response = requests.get(url, headers={'User-agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36'})
    soup = BeautifulSoup(response.content, "lxml")
    price =  soup.find(attrs = {'class': 'a-row a-spacing-mini olpOffer'}).\
            find(attrs = {'class' : 'a-size-large a-color-price olpOfferPrice a-text-bold'}).getText().strip()[1:].replace('UR', '')
    
    result = float(price.replace(',','.'))
    queue.put(result)

def combine(asin):
    q1 = Queue.Queue()
    q2 = Queue.Queue()
    q3 = Queue.Queue()
    q4 = Queue.Queue()

    url1 = 'http://www.amazon.co.uk/gp/offer-listing/{ASIN}/ref=dp_olp_new?ie=UTF8&condition=new'.replace('{ASIN}', asin)
    url2 = 'http://www.amazon.fr/gp/offer-listing/{ASIN}/ref=dp_olp_new?ie=UTF8&condition=new'.replace('{ASIN}', asin)
    url3 = 'http://www.amazon.it/gp/offer-listing/{ASIN}/ref=dp_olp_new?ie=UTF8&condition=new'.replace('{ASIN}', asin)
    url4 = 'http://www.amazon.es/gp/offer-listing/{ASIN}/ref=dp_olp_new?ie=UTF8&condition=new'.replace('{ASIN}', asin)

    t1 = Thread(target = getPriceAmazon, args=(url1, q1))
    t2 = Thread(target = getPriceAmazon, args=(url2, q2))
    t3 = Thread(target = getPriceAmazon, args=(url3, q3))
    t4 = Thread(target = getPriceAmazon, args=(url4, q4))
    
    t1.start()
    t2.start()
    t3.start()
    t4.start()

    t1.join()
    t2.join()
    t3.join()
    t4.join()

    return [q1.get(),q2.get(),q3.get(),q4.get()]

print combine('B00NVDNDUW')
