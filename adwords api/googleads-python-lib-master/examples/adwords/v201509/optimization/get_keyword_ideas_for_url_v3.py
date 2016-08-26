# import modules
from googleads import adwords
import pandas as pd
from unidecode import unidecode
import time, sqlite3

# static variables
PAGE_SIZE = 20
cols_data = ['URL', 'Keyword', 'Avg. Monthly Searches']
ROWS = 50000

try:
    writer = pd.ExcelWriter('keywords_Ideas.xlsx')
    df = pd.read_excel('keywords_Ideas.xlsx','Sheet1')
except:
    writer = pd.ExcelWriter('keywords_Ideas.xlsx', engine='xlsxwriter')
    df = pd.DataFrame(columns=cols_data)
        
def main(client, url, df):
  try:    
    # Initialize appropriate service.
    targeting_idea_service = client.GetService(
        'TargetingIdeaService', version='v201509')

    # Construct selector object and retrieve related keywords.
    offset = 0
    selector = {
        'searchParameters': [
            {
                'xsi_type': 'RelatedToUrlSearchParameter',
                'urls': [url]
            },
            {
                # Language setting (optional).
                # The ID can be found in the documentation:
                #  https://developers.google.com/adwords/api/docs/appendix/languagecodes
                'xsi_type': 'LanguageSearchParameter',
                'languages': [{'id': '1000'}]
            }
        ],
        'ideaType': 'KEYWORD',
        'requestType': 'IDEAS',
        'requestedAttributeTypes': ['KEYWORD_TEXT', 'SEARCH_VOLUME',
                                    'CATEGORY_PRODUCTS_AND_SERVICES'],
        'paging': {
            'startIndex': str(offset),
            'numberResults': str(PAGE_SIZE)
        }
    }
    more_pages = True
    while more_pages:
      page = targeting_idea_service.get(selector)

      # store results in the df
      if 'entries' in page:
        for result in page['entries']:
          attributes = {}
          for attribute in result['data']:
            attributes[attribute['key']] = getattr(attribute['value'], 'value',
                                                   '0')
          nrows = df.shape[0]+1
          df.loc[nrows] = [url, attributes['KEYWORD_TEXT'],attributes['SEARCH_VOLUME']]
          nrows +=1

          if (nrows %ROWS) ==0:
            print("Writing to the file!")
            df.to_excel(writer,'Sheet1', index = False, header=cols_data)
            writer.save()

            time.sleep(1)

            writer = pd.ExcelWriter('keywords_Ideas.xlsx')
            df = pd.read_excel('keywords_Ideas.xlsx','Sheet1')
            
          if (nrows %1000) == 0:
            print nrows, ' downloaded'         
              
      else:
        print 'No related keywords were found.'
        time.sleep(3)

      offset += PAGE_SIZE
      selector['paging']['startIndex'] = str(offset)
      more_pages = offset < int(page['totalNumEntries'])
      more_pages = False
  except Exception,e:
    print str(e)
    time.sleep(2)

conn = sqlite3.connect('downloaded_urls.db')
print "[+] Opened database connection successfully!!"
c = conn.cursor()
    
# Initialize client object.
adwords_client = adwords.AdWordsClient.LoadFromStorage()
f = open('google_api.csv', 'rb')
urls = f.read().split('\n')[:-1]

count = 0
for url in urls:
  count +=1
  url = url.strip().replace(',','')
  c.execute("SELECT * FROM d_urls WHERE url = '%s'" % url)
  rows = c.fetchone()
  
  if rows == None:
      if (count % 100) == 0:
        print '[+] Downloaded data for ', (count), ' urls'
      main(adwords_client, url, df)
      c.execute("INSERT INTO d_urls (url ) values(?)", (url, ))
      conn.commit()
  else:
      print '[+] Data for url :: ', url, ' already downloaded'
  
print("Writing to the file!")
df.to_excel(writer,'Sheet1', index = False, header=cols_data)
writer.save()
