from selenium import webdriver
import time

driver  = webdriver.Firefox()

def getElement(element, method):
    try:
        if method == 'class':
            return driver.find_element_by_class_name(element)
        elif method == 'css':
            return driver.find_element_by_css_selector(element)
        elif method == 'xpath':
            return driver.find_element_by_xpath(element)
        elif method == 'id':
            return driver.find_element_by_id(element)
    except:
        return None

def returnText(elem):    
    try:
        if str(makeGood((elem.text)).strip().replace(')','').replace('(','')):
            return str(makeGood((elem.text)).strip().replace(')','').replace('(',''))
        else:
            return None
    except:
        return None
    
url = 'http://www.amazon.com/gp/product/B015MI3H0E'

driver.get(url)

try:
    getElement('redir-opt-out-label', 'id').click()
    getElement('redir-a-button-sec-center', 'class').click()
except:
    pass
time.sleep(2)
getElement('add-to-cart-button', 'id').click()
time.sleep(2)
getElement('hlb-ptc-btn-native', 'id').click()
time.sleep(2)

email = ## add your own email
pwd = ## add ur own password
promo = 'QNQF-UD625M-DMHRQV'

getElement('ap_email', 'id').send_keys(email)
time.sleep(2)
getElement('ap_password', 'id').send_keys(pwd)
time.sleep(2)
getElement('signInSubmit', 'id').click()
time.sleep(2)

getElement('address-book-entry-2', 'id').find_element_by_class_name('a-button-inner').click()
time.sleep(2)
getElement('a-button-inner', 'class').click()
time.sleep(2)
getElement('gc-link-expander', 'id').click()
time.sleep(2)
getElement('gcpromoinput', 'id').send_keys(promo)
time.sleep(2)
getElement('button-add-gcpromo', 'id').click()
time.sleep(2)

elem = getElement('gcpromoerrorblock', 'id')
time.sleep(2)

error = returnText(elem)

print error





