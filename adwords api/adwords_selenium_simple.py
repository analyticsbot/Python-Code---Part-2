from selenium import webdriver
from selenium.common.exceptions import TimeoutException
import selenium.webdriver.support.wait
selenium.webdriver.support.wait.POLL_FREQUENCY = 0.05

import re
import random
import collections

email="ivar.dodo123@gmail.com"
passwd="ravihari!12"
keywords = ["ipad","cars","a0012k2k2","kindle","mac","beats","travel"]

profile = webdriver.FirefoxProfile()
profile.set_preference("browser.download.folderList", 2)
profile.set_preference("browser.download.manager.showWhenStarting", False)
profile.set_preference("browser.download.dir", 'C:\\Users\\Ravi Shankar\\Documents\\Upwork\\adwords api\\initial_dest\\')
profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/csv")

ff = webdriver.Firefox(firefox_profile=profile)
ff.set_page_load_timeout(30)
ff.implicitly_wait(40)
busy = False
is_login = False
on_keyword_page = False
kwurl = ''

print 'getting adwords.google.com'
ff.get('https://adwords.google.com')
ff.find_element_by_class_name('ignore-channel').click()
ff.find_element_by_id("Email").send_keys(email)
ff.find_element_by_id('next').click()
ff.find_element_by_id("Passwd").send_keys(passwd)
signin = ff.find_element_by_id('signIn')

signin.submit()

is_login = True
search = re.compile(r'(\?[^#]*)#').search(ff.current_url).group(1)
kwurl = 'https://adwords.google.com/o/Targeting/Explorer'+search+'&__o=cues&ideaRequestType=KEYWORD_IDEAS'

print email, 'querying', keywords
busy = True
ret = {}

print 'visiting keyword tools'
ff.get(kwurl)

kwinput = ff.find_element_by_class_name('spgc-g')
kwinput.click()

##kwinput = ff.find_element_by_css_selector(".spC-a.spob-c")
##kwinput.send_keys('http://www.amazon.com/dp/B00N2BW2PK')
#ff.execute_script("document.getElementById('gwt-debug-url-suggest-box').value = 'http://www.google.com';")
ff.execute_script('document.getElementsByClassName("spob-b spA-b")[1].innerHTML = "";')
ff.execute_script('document.getElementsByClassName("spC-a spob-c")[1].value = " http://www.google.com ";')
##document.getElementsByClassName("spC-a spob-c")[1].focus();
##
##document.getElementsByClassName("spC-a spob-c")[1].select();
##document.getElementsByClassName("spob-b spA-b")[1].innerHTML = "";
#ff.find_element_by_css_selector("button.gwt-Button").click()
#document.getElementsByClassName("spC-a spob-c")[1].value = "https://www.google.com";
ff.execute_script("document.getElementById('gwt-debug-search-button-content').click();")
ff.execute_script("document.getElementsByClassName('goog-button-base-content')[1].click();")

ff.find_element_by_id('gwt-debug-splash-panel-resume-anchor').click()


ff.find_element_by_xpath('//*[@id="gwt-debug-search-download-button"]/div[2]/div[1]/div/div/div/div[2]').click()
ff.find_element_by_xpath('//*[@id="gwt-debug-download-button-content"]').click()
ff.find_element_by_xpath('//*[@id="gwt-debug-retrieve-download-content"]').click()
from os import listdir

os.rename(filename, filename[7:])
listdir('C:\\Users\\Ravi Shankar\\Documents\\Upwork\\adwords api\\initial_dest\\')

shutil.move(src_file, dst_dir)

ff.find_element_by_id('gwt-debug-url-suggest-box').clear()
ff.find_element_by_id('gwt-debug-url-suggest-box').send_keys('http://www.amazon.com/dp/B00N2BW2PK')
ff.find_element_by_id('gwt-debug-search-button-content').click()

