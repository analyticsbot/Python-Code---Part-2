# import modules
from googleads import adwords
import pandas as pd
from unidecode import unidecode
import time, sqlite3,threading
from threading import Thread

# static variables
PAGE_SIZE = 20
cols_data = ['URL', 'Keyword', 'Avg. Monthly Searches']
ROWS = 60000
main_df = ['']*100
      
def main(client, url, df, i, writer, PAGE_SIZE, cols_data, ROWS, main_df):
    #print "[+] Getting data from thread :: ", i
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
              main_df[i] = df
              nrows +=1

              if (nrows %ROWS) ==0:
                print("Writing to the file!")
                df.to_excel(writer,'Sheet1', index = False, header=cols_data)
                writer.save()
                
              if (nrows %1000) == 0:
                print nrows, ' downloaded'
                try:
                    l=unidecode(df.to_string())
                    kk= open('keywords_Ideas_'+str(i)+'.txt','wb')
                    kk.write(l)
                    kk.close()
                except Exception,e:
                    print str(e)
                    pass
                  
          else:
            print url, 'No related keywords were found.'
            time.sleep(3)

          offset += PAGE_SIZE
          selector['paging']['startIndex'] = str(offset)
          more_pages = offset < int(page['totalNumEntries'])
          more_pages = False
    except Exception,e:
        print url, str(e)
        time.sleep(2)


def runningThreads(url_subset, i, writer, df, adwords_client, PAGE_SIZE, cols_data, ROWS, main_df):

    sqlite3.threadsafety = 0
    
    conn = sqlite3.connect('downloaded_urls_' + str(i) + '.db', check_same_thread = False)
    print "[+] Opened database connection successfully"
    c = conn.cursor()
    try:
        c.execute("create table d_urls(url TEXT);")
        conn.commit()
    except:
        pass
    
    count = 0
    for url in url_subset:
      count +=1
      url = url.strip().replace(',','')
      c.execute("SELECT * FROM d_urls WHERE url = '%s'" % url)
      rows = c.fetchone()
      lock = threading.Lock()
      if rows == None:
          if (count % 100) == 0:
            print '[+] Downloaded data for ', (count), ' urls for thread :: ', i
          main(adwords_client, url, df, i, writer, PAGE_SIZE, cols_data, ROWS, main_df)
          lock.acquire(True)
          c.execute("INSERT INTO d_urls (url ) values(?)", (url, ))
          conn.commit()
          lock.release()
          
      else:
          pass
          #print '[+] Data for url :: ', url, ' already downloaded. Working for threads :: ', i
    conn.close()

def runThreads(urls, numThreads, adwords_client, PAGE_SIZE, cols_data, ROWS, main_df):
    dataframes = []
    writers = []

    for i in range(1, numThreads+1):
        try:
            writer = pd.ExcelWriter('keywords_Ideas_'+str(i)+'.xlsx')
            writers.append(writer)
            df = pd.read_excel('keywords_Ideas_'+str(i)+'.xlsx','Sheet1')
            dataframes.append(df)
        except:
            writer = pd.ExcelWriter('keywords_Ideas_'+str(i)+'.xlsx', engine='xlsxwriter')
            writers.append(writer)
            df = pd.DataFrame(columns=cols_data)
            dataframes.append(df)

    threads= []
    for i in range(1, numThreads+1):
        if i!=numThreads+1:
            url_subset = urls[len(urls)/numThreads*(i-1):len(urls)/numThreads*i]
            print i, len(url_subset)
        else:
            url_subset = urls[len(urls)/numThreads*(i):]
            print i, len(url_subset)

        threads.append(Thread(target = runningThreads, \
                              args=(url_subset, i, writers[i-1], \
                                    dataframes[i-1],adwords_client, PAGE_SIZE, cols_data, ROWS, main_df)))
    for t in threads:
        t.start()

    for t in threads:
        t.join()
        dataframes[threads.index(t)].to_excel(writers[threads.index(t)],'Sheet1', index = False, header=cols_data)
        writers[threads.index(t)].save()
           
# Initialize client object.
print 'sleeping.....'
#time.sleep(15600)
print 'awoken....'
adwords_client = adwords.AdWordsClient.LoadFromStorage('/home/ubuntu/Desktop/rr/url_set_3/googleads.yaml')
f = open('url_set_3.csv', 'rb')
urls = f.read().split('\n')[:-1]
numThreads = int(len(urls)*PAGE_SIZE/ROWS)+1
runThreads(urls, numThreads, adwords_client, PAGE_SIZE, cols_data, ROWS, main_df)

for i in range(1, numThreads+1):
    print main_df[i].shape
    writer = pd.ExcelWriter('keywords_Ideas_'+str(i)+'.xlsx')
    main_df[i].to_excel(writer,'Sheet1', index = False, header=cols_data)
    writer.save()
