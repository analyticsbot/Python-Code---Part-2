import os
import pandas as pd

df = pd.DataFrame(columns = ['URL', 'Keyword', 'Avg. Monthly Searches'])

directory = 'C:\\Users\\Ravi Shankar\\Documents\\Upwork\\adwords api\\250k URLS\\client_data\\left\\url_set_3\\'

for file in os.listdir(directory):
    if file.endswith(".xlsx"):
        temp = pd.read_excel(directory + '/' + file)
        df = pd.concat([df, temp], axis = 0)
    
print df.shape
print len(df['URL'].unique())

df.to_csv('dataset.csv', sep=',', encoding='utf-8', index = False)

unique_urls = df['URL'].unique()

import csv
f = open('downloaded_urls.csv', 'wb')
writer = csv.writer(f)
for url in unique_urls:
    writer.writerow([url])

o = open('url_set_3.csv', 'rb')
data = o.read().split('\n')[:-1]
data = [line.strip() for line in data]

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


    
