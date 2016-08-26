## import required modules
from googleads import adwords
import pandas as pd
from unidecode import unidecode
import time, sqlite3,threading
from threading import Thread

## declare static variables
PAGE_SIZE = 20 # number of keywords to extract per url
cols_data = ['URL', 'Keyword', 'Avg. Monthly Searches']  # headers to extract from the response
ROWS = 60000 # while exporting to excel, each thread download at max these many number of rows.
             # low value for rows will have higher number of threads in action. High value will have lower
             # number of threads. Ideally, there should be around 10-12 threads max.
debug = False # print status
path_yaml = 'path to yaml file'
input_file = 'path to input csv file. only contains urls. No headers'

def main(client, url, df, i, writer, PAGE_SIZE, cols_data, ROWS, main_df, debug):
    """
    Function that will extract the keyword ideas from Google Adwords API
    client -- google adwords client
    url -- url for which data is to be extracted
    df -- pandas dataframe for each thread to store data
    i -- thread indicator
    writer -- excel writer object
    PAGE_SIZE -- number of keywords to extract per url
    cols_data -- columns to be extracted from the response
    ROWS -- number of rows per excel sheet at max
    main_df -- global list to store the pandas dataframe
"""
    if debug: print "[+] Getting data from thread :: ", i
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
                if debug: print "Writing to the file!"
                df.to_excel(writer,'Sheet1', index = False, header=cols_data)
                writer.save()
                
              if (nrows %1000) == 0:
                ## writing the output to text file incase of any error happens, all data is not lost
                ## at at every 1000 rows, write to textfile
                if debug: print nrows, ' downloaded for thread ::', i
                try:
                    l=unidecode(df.to_string())
                    kk= open('keywords_Ideas_'+str(i)+'.txt','wb')
                    kk.write(l)
                    kk.close()
                except Exception,e:
                    if debug: print str(e)
                    pass
                  
          else:
            print url, 'No related keywords were found'
            

          offset += PAGE_SIZE
          selector['paging']['startIndex'] = str(offset)
          more_pages = offset < int(page['totalNumEntries'])
          more_pages = False
    except Exception,e:
        if debug: print url, str(e)
        time.sleep(2)


def runningThreads(url_subset, i, writer, df, adwords_client, PAGE_SIZE, cols_data, ROWS, main_df):
    """
    Function to start the threads
    adwords_client - adwords client
    url_subset -- url subset for each thread for which data is to be extracted
    df -- pandas dataframe for each thread to store data
    i -- thread indicator
    writer -- excel writer object
    PAGE_SIZE -- number of keywords to extract per url
    cols_data -- columns to be extracted from the response
    ROWS -- number of rows per excel sheet at max
    main_df -- global list to store the pandas dataframe    
    """

    ## store the downloaded urls in a sqlite db so as if the code is started again
    ## these urls are not downloaded. 
    sqlite3.threadsafety = 0    
    conn = sqlite3.connect('downloaded_urls_' + str(i) + '.db', check_same_thread = False)
    if debug: print "[+] Opened database connection successfully"
    c = conn.cursor()

    ## tryto create the table if it does not exists
    try:
        c.execute("create table d_urls(url TEXT);")
        conn.commit()
    except:
        pass

    ## for every 100 urls downloaded, print on screen
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
          if debug: print '[+] Data for url :: ', url, ' already downloaded. Working for threads :: ', i
    conn.close() ## close the connection for a particular thread

def runThreads(urls, numThreads, adwords_client, PAGE_SIZE, cols_data, ROWS, main_df, debug):
    """
    Function to run threads
    adwords_client - adwords client
    urls -- urls for which data is to be extracted
    writer -- excel writer object
    PAGE_SIZE -- number of keywords to extract per url
    cols_data -- columns to be extracted from the response
    ROWS -- number of rows per excel sheet at max
    main_df -- global list to store the pandas dataframe
    debug -- print output on screen
    """

    ## initialize a list and writers for each thread
    dataframes = []
    writers = []

    ## start threads
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
                                    dataframes[i-1],adwords_client, PAGE_SIZE, cols_data, ROWS, main_df, debug)))
    ## start the threads
    for t in threads:
        t.start()

    ## wait for all the threads to complete
    for t in threads:
        t.join()
        dataframes[threads.index(t)].to_excel(writers[threads.index(t)],'Sheet1', index = False, header=cols_data)
        writers[threads.index(t)].save()
           
# Initialize client object.
if debug: print 'Starting....'
adwords_client = adwords.AdWordsClient.LoadFromStorage(path_yaml)
if debug: print 'Read configuration from the yaml file'
f = open(input_file, 'rb')
urls = f.read().split('\n')[:-1]
if debug: print 'Read data from input file'
numThreads = int(len(urls)*PAGE_SIZE/ROWS)+1
main_df = ['']*(numThreads+1)
if debug: print 'Starting the threads'
runThreads(urls, numThreads, adwords_client, PAGE_SIZE, cols_data, ROWS, main_df, debug)

for i in range(1, numThreads+1): 
    writer = pd.ExcelWriter('keywords_Ideas_'+str(i)+'.xlsx')
    main_df[i].to_excel(writer,'Sheet1', index = False, header=cols_data)
    writer.save()

if debug: print 'All excel files written'
