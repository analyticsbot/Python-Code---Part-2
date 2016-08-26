"""
This code is built in python using selenium module that parses
'https://www.atg.se/spel/2015-12-05/V75/romme/resultat
and stores the horse name, driver name, value for different races
a) in resultat table
b) (v75-1, v75-2, v75-3, v75-4, v75-5, v75-6, v75-7) tables
"""

## import necessary modules
from selenium import webdriver

## load the page in driver
driver = webdriver.Firefox()
url = 'https://www.atg.se/spel/2015-12-05/V75/romme'
driver.get(url)

resultat_dict = {}

## get the details in resultat table
## parse the elements from the resultat table
try:
    a = driver.find_element_by_xpath('//*[@id="main"]/div/div[2]/div[2]/div[2]/div[2]/div/div/div[2]/span[2]/a/span')
    a.click()
    resultat = driver.find_element_by_css_selector('.table.table--bordered.game-table').find_elements_by_tag_name('tr')
except:
    pass

resultat_dict['resultat'] = {}

try:
    for result in resultat:
        ## ignore the first row which has headers
        if resultat.index(result) == 0:
            continue
        
        elem_text = result.text
        
        elem_text_split = elem_text.split('\n')
        try:
            id_ = elem_text_split[0].strip()
            horse = elem_text_split[1].strip()
            horse_driver =  elem_text_split[2].strip()
            value = elem_text_split[3].strip()

            resultat_dict['resultat'][id_] = {'horse' : horse, 'horse_driver' :horse_driver, 'value' : value}
        except:
            pass
except:
    print 'no data'

v75_results = driver.find_elements_by_class_name('game-table-wrapper')

## parse results and store in the resultat_dict with key 'v75-1', 'v75-2', and so on till 'v75-7'
for v75_result in v75_results:
    ix = 'v75-' + str(v75_results.index(v75_result))

    resultat_dict[ix] = {}

    try:
        v75_result = v75_result.find_elements_by_tag_name('tr')
        
        for result in v75_result:

            ## ignore the first row which has headers
            if v75_result.index(result) == 0:
                continue
        
            elem_text = result.text
            
            try:
                elem_text_split = elem_text.split('\n')
                try:
                    id_ = elem_text_split[0].strip()
                    horse = elem_text_split[1].strip()
                    horse_driver =  elem_text_split[2].strip()
                    value = elem_text_split[3].strip()

                    resultat_dict[ix][id_] = {'horse' : horse, 'horse_driver' : horse_driver}
                except:
                    pass
            except:
                pass
    except:
        print 'no data'

## to get values for resultat table
##print resultat_dict['resultat']
##
#### to get values for 'v75-i' tables
##for i in range(1, 8):
##    print resultat_dict['v75-' + str(i)]
    
    
