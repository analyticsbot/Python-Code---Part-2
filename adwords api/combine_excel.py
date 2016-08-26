#import modules
import os
import pandas as pd
import csv

### This script merges all the excel data into one csv ###
### This script also writes the downloaded urls and the left urls ###

df = pd.DataFrame(columns = ['URL', 'Keyword', 'Avg. Monthly Searches'])
directory = 'path to directory that contains the excel files'
input_file = 'file which has the list of urls to be downloaded'

# iterate through all the files. if an excel file, read and append to the dataframe
for file in os.listdir(directory):
    if file.endswith(".xlsx"):
        temp = pd.read_excel(directory + '/' + file)
        df = pd.concat([df, temp], axis = 0)
    
print 'total number of rows ::', df.shape
print 'total urls downloaded ::',len(df['URL'].unique())

df.to_csv('dataset.csv', sep=',', encoding='utf-8', index = False)

unique_urls = df['URL'].unique()

## to write all downloaded urls
f = open('downloaded_urls.csv', 'wb')
writer = csv.writer(f)
for url in unique_urls:
    writer.writerow([url])

## file name from which data was written
o = open(input_file, 'rb')
data = o.read().split('\n')[:-1]
data = [line.strip() for line in data]

## left urlsss
count = 0
s = open('left_urls.csv', 'wb')
writer1 = csv.writer(s)
for url in unique_urls:
    if url not in data:
        count +=1
        writer.writerow([url])

print 'left urls::', count

f.close()
o.close()
s.close()


    
