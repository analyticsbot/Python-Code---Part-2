from selenium import webdriver

profile = webdriver.FirefoxProfile()
profile.set_preference("browser.download.folderList", 2)
profile.set_preference("browser.download.manager.showWhenStarting", False)
profile.set_preference("browser.download.dir", 'C:\\Users\\Ravi Shankar\\Documents\\Upwork\\adwords api\\initial_dest\\')
profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/csv")

driver = webdriver.Firefox(firefox_profile=profile)

# url for login        
url = 'https://www.merchantwords.com/login'

driver.get(url)
f = open('keywords.csv', 'rb')
data = f.read().split('\n')[:-1]
data = [d.strip() for d in data][1:]

# credentials
email = 'susan@notaisltd.com'
password = '1BS1lse2s'

email_elem = driver.find_element_by_name('email')
email_elem.send_keys(email)
pwd_elem = driver.find_element_by_name('password')
pwd_elem.send_keys(password)

btn = driver.find_element_by_css_selector('.btn.btn-primary')
btn.click()

## request file
for key in data:
    print 'getting data for', key
    search = driver.find_element_by_id('usersearchbox')
    search.clear()
    search.send_keys(key)
    driver.find_element_by_class_name('btn').click()
    driver.find_element_by_class_name('span2').find_element_by_class_name('btn').click()
    
    
    

