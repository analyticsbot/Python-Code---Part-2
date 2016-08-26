from selenium.webdriver.firefox import webdriver
import pandas as pd
import datetime, re, time

driver = webdriver.WebDriver()
driver.get('https://www.hidemyass.com/proxy-list')

def getElement(element, method, indicator = None):
    if not indicator:
        if method == 'css':
            return str(driver.find_element_by_css_selector(element).text.strip())
        elif method == 'xpath':
            return str(driver.find_element_by_xpath(element).text.strip())
        elif method == 'class':
            return str(driver.find_element_by_class_name(element).text.strip())
        elif method == 'id':
            return str(driver.find_element_by_id(element).text.strip())
    else:
        elem = driver.find_element_by_xpath(element)
        return str(re.findall('width:\s(.*?);', elem.get_attribute('style'))[0])

def webElement(header, row_id, id_):
    if header:
        return '//*[@id="listable"]/thead/tr/th[' + str(id_) + ']'
    else:
        if id_ in [3, 4, 7, 8]:
            return '//*[@id="listable"]/tbody/tr[' + str(row_id) + ']/td[' + str(id_) + ']'
        elif id_ not in [5, 6]:
            return '//*[@id="listable"]/tbody/tr[' + str(row_id) + ']/td[' + str(id_) + ']/span'
        else:
            return '//*[@id="listable"]/tbody/tr[' + str(row_id) + ']/td[' + str(id_) + ']/div/div'
             

headers = [getElement(webElement(1, 0, 1), 'xpath'), getElement(webElement(1, 0, 2), 'xpath'),\
           getElement(webElement(1, 0, 3), 'xpath'), getElement(webElement(1, 0, 4), 'xpath'),\
           getElement(webElement(1, 0, 5), 'xpath'), getElement(webElement(1, 0, 6), 'xpath'),\
           getElement(webElement(1, 0, 7), 'xpath'), getElement(webElement(1, 0, 8), 'xpath'), 'proxies_scraping']

df = pd.DataFrame(columns = headers)

count = 0
j = 0

while True:
    if count == 0:
        while True:
            for i in range(1, 51):
                df.loc[j] = [getElement(webElement(0, i, 1), 'xpath'), getElement(webElement(0, i, 2), 'xpath'),\
                            getElement(webElement(0, i, 3), 'xpath'), getElement(webElement(0, i, 4), 'xpath'),\
                            getElement(webElement(0, i, 5), 'xpath', True), getElement(webElement(0, i, 6), 'xpath', True),\
                            getElement(webElement(0, i, 7), 'xpath'), getElement(webElement(0, i, 8), 'xpath') , \
                             'http://'+ str(getElement(webElement(0, i, 2), 'xpath')) + ':' + str(getElement(webElement(0, i, 3), 'xpath'))]
                j +=1
            count +=1
            

    else:
        next_page_element = driver.find_element_by_css_selector('.arrow.next').find_element_by_tag_name('a')
        next_page_element.click()
        while True:
            for i in range(1, 51):
                    df.loc[j] = [getElement(webElement(0, i, 1), 'xpath'), getElement(webElement(0, i, 2), 'xpath'),\
                                getElement(webElement(0, i, 3), 'xpath'), getElement(webElement(0, i, 4), 'xpath'),\
                                getElement(webElement(0, i, 5), 'xpath', True), getElement(webElement(0, i, 6), 'xpath', True),\
                                getElement(webElement(0, i, 7), 'xpath'), getElement(webElement(0, i, 8), 'xpath'),\
                                 'http://'+ str(getElement(webElement(0, i, 2), 'xpath')) + ':' + str(getElement(webElement(0, i, 3), 'xpath'))]
                    j +=1
            count +=1
           
df.to_csv('hide_my_ass_proxies_' + str(datetime.date.today()) + '.csv')
time.sleep(100000)
driver.close()
