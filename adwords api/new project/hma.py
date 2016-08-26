from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

import unittest


driver = webdriver.Firefox()
driver.get("http://proxylist.hidemyass.com/")
proxys = driver.find_elements_by_xpath('/html/body/section/section[4]/section[1]/div/table/tbody/tr/td[2]')
ports = driver.find_elements_by_xpath('/html/body/section/section[4]/section[1]/div/table/tbody/tr/td[3]')
for ip in proxys:
    print(ip.text+ ':'+ ports[proxys.index(ip)].text)
