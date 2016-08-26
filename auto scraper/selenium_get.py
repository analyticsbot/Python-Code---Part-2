from selenium  import webdriver

driver = webdriver.Firefox()
url = 'http://www.autogarage.nl/auto/'
driver.get(url)

click_e = driver.find_element_by_id('pagercounter')
click_e.click()
