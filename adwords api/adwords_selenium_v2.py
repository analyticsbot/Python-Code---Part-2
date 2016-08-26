from selenium import webdriver
from selenium.common.exceptions import TimeoutException
import selenium.webdriver.support.wait
import re, random, time, os
from os import listdir
import pandas as pd
import sqlite3, hashlib

## declare static variables
EMAIL = "ivar.dodo123@gmail.com"
PASSWORD ="ravihari!12"
INITIAL_DEST_FOLDER = 'C:\\Users\\Ravi Shankar\\Documents\\Upwork\\adwords api\\initial_dest\\'
FINAL_DEST_FOLDER = 'C:\\Users\\Ravi Shankar\\Documents\\Upwork\\adwords api\\final\\s'
CLICK_DELAY_LOGIN = 10
DELAY_URL2 = 15
OUTPUT_FILE_MAX_ROWS = 10000
OUTPUT_FILENAME = 'KEYWORD_IDEAS'
OUTPUT_FILENAME_COUNTER = 0

## final dataframe
df = pd.DataFrame(columns = ['URL', 'Keyword', 'Avg. Monthly Searches'])

## profile of firefox
profile = webdriver.FirefoxProfile()
profile.set_preference("browser.download.folderList", 2)
profile.set_preference("browser.download.manager.showWhenStarting", False)
profile.set_preference("browser.download.dir", INITIAL_DEST_FOLDER)
profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/csv")

## declare an instance of firefox driver
driver = webdriver.Firefox(firefox_profile=profile)

## open the webpage
print '[+] Opening adwords.google.com'
driver.get('https://adwords.google.com')

## login to the adwords portal
driver.implicitly_wait(CLICK_DELAY_LOGIN) # seconds
driver.find_element_by_class_name('ignore-channel').click()
driver.find_element_by_id("Email").send_keys(EMAIL)
driver.find_element_by_id('next').click()
driver.find_element_by_id("Passwd").send_keys(PASSWORD)
signin = driver.find_element_by_id('signIn')
signin.submit()

print '[+] Logged into adwords.google.com'
search = re.compile(r'(\?[^#]*)#').search(driver.current_url).group(1)
kwurl = 'https://adwords.google.com/o/Targeting/Explorer'+search+'&__o=cues&ideaRequestType=KEYWORD_IDEAS'

print '[+] Visiting keyword tools'
driver.implicitly_wait(DELAY_URL2) # seconds
driver.get(kwurl)

## click on the resume session link
driver.find_element_by_id('gwt-debug-splash-panel-resume-anchor').click()
time.sleep(random.randint(15, 20))

def getKeywordIdeas(url, c, conn):
    try:
        print '[+] Getting keyword ideas'
        driver.find_element_by_id('gwt-debug-url-suggest-box').clear()
        time.sleep(random.randint(1, 2))
        driver.find_element_by_id('gwt-debug-url-suggest-box').send_keys(url)
        driver.find_element_by_id('gwt-debug-search-button-content').click()
        time.sleep(random.randint(1, 15))
        
        ## click on the keyword ideas tab
        g = driver.find_element_by_xpath('//*[@id="gwt-debug-grouping-toggle-KEYWORD_IDEAS"]/div')
        g.click()
        time.sleep(random.randint(10, 15))

        print '[+] Downloading keyword ideas'
        ## download file
        driver.find_element_by_xpath('//*[@id="gwt-debug-search-download-button"]/div[2]/div[1]/div/div/div/div[2]').click()
        time.sleep(random.randint(15, 20))
        driver.find_element_by_xpath('//*[@id="gwt-debug-download-button-content"]').click()
        time.sleep(random.randint(15, 20))
        driver.find_element_by_xpath('//*[@id="gwt-debug-retrieve-download-content"]').click()
        time.sleep(random.randint(15, 20))

        ## get file in the initial download folder
        filename = listdir(INITIAL_DEST_FOLDER)[0]

        sku = url.split('/')[-1] + '.csv'

        print '[+] Renaming file from Google Adwords to sku name'
        ## rename the file to SKU name
        os.rename(filename, sku)

        print '[+] Adding keyword ideas to main dataframe'
        ## read the contents of this file and add to the main file

        temp = pd.read_csv(sku)
        temp = temp[["Keyword", "Avg. Monthly Searches (exact match only)"]].iloc[:20]
        temp['url'] = pd.Series(url, index=temp.index)
        df  = pd.concat([df, temp], axis=0)
            
        
        ## move this file to the final folder destination
        print '[+] Moving file to the final directory'
        shutil.move(INITIAL_DEST_FOLDER + '/' + sku, FINAL_DEST_FOLDER + '/')

        ## insert finished urls into the db in the completed table
        print '[+] Inserting url entry as downloaded in the db'
        url = url.strip().replace(',', '')
        c.execute("INSERT INTO completed_urls (url, ) values(?)", (url, ),)
        conn.commit()

        ## output to csv if the num rows limit reaches csv
        if nrows > OUTPUT_FILE_MAX_ROWS:
            print '[+] Max row limit reached. Outputting to csv and opening new file'
            df.to_csv(FINAL_DEST_FOLDER + '/' + OUTPUT_FILENAME + '_' + OUTPUT_FILENAME_COUNTER + '.csv')
            OUTPUT_FILENAME_COUNTER +=1
            df = pd.DataFrame(columns = ['URL', 'Keyword', 'Avg. Monthly Searches'])

    except Exception,e:
        print 'Error - ', str(e), ' during url :: ', url
        driver.refresh()
        time.sleep(random.randint(5, 10))
        print '[+] Inserting url entry as failed in the db'
        url = url.strip().replace(',', '')
        c.execute("INSERT INTO failed_urls (url, ) values(?)", (url, ),)
        conn.commit()

        ## click on the resume session link
        driver.find_element_by_id('gwt-debug-splash-panel-resume-anchor').click()
        time.sleep(random.randint(15, 20))

if __name__== "__main__":
    conn = sqlite3.connect('urls')
    print "[+] Opened database connection successfully!!"
    c = conn.cursor()

    print '[+] Read urls from database'
    f = open('aa.csv', 'rb')
    data = f.read().split('\n')[:-1]
    for url in data:
        url = row.strip()
        x = c.execute("SELECT * FROM completed_urls WHERE url = '%s'" % url)
        rows = x.fetchone()
        if (data.index(url)+1) % 100 ==0:
            print 'Downloaded data for ', (data.index(url)+1), ' urls'
        if rows == None:
            print '[+] Getting data for :: ', url
            getKeywordIdeas(url, c, conn)
        else:
            print '[+] Data for url :: ', url, ' already downloaded'

    conn.close()
                  


    
