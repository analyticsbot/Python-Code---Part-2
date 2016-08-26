#!/usr/bin/python

from googleads import adwords
import pandas as pd
from unidecode import unidecode

PAGE_SIZE = 50
df = pd.DataFrame(columns = ['URL', 'Keyword', 'Avg. Monthly Searches'])
counter = 6

def main(client, url, df, counter):
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

    # Display results.
    if 'entries' in page:
      for result in page['entries']:
        attributes = {}
        for attribute in result['data']:
          attributes[attribute['key']] = getattr(attribute['value'], 'value',
                                                 '0')
        nrows = df.shape[0]+1
        df.loc[nrows] = [url, attributes['KEYWORD_TEXT'],attributes['SEARCH_VOLUME']]
        nrows +=1

        if (nrows %100) ==0:
          print nrows
          
        if (nrows %1000) ==0:
          print nrows, ' downloaded'
          print url
          #df.to_csv('api_keywords_' + str(counter) + '.csv')
          ss = df.to_string()
          f =open('api_keywords_' + str(counter) + '.txt', 'wb')
          f.write(unidecode(ss))
          f.close()
          df = pd.DataFrame(columns = ['URL', 'Keyword', 'Avg. Monthly Searches'])
          counter +=1
                  
      print
    else:
      print 'No related keywords were found.'
    offset += PAGE_SIZE
    selector['paging']['startIndex'] = str(offset)
    more_pages = offset < int(page['totalNumEntries'])
    more_pages = False


if __name__ == '__main__':
  # Initialize client object.
  adwords_client = adwords.AdWordsClient.LoadFromStorage()
  f = open('google_api.csv', 'rb')
  urls = f.read().split('\n')[2:-1]
  #urls = ['http://www.amazon.com/dp/B00N2BW2PK', 'http://www.amazon.com/dp/B005AXNHD4/']
  for url in urls:
    url = url.strip().replace(',','')
    main(adwords_client, url, df, counter)
