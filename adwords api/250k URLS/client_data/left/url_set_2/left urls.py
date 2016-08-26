import os
import pandas as pd
import csv

file_name = 'url_set_2.csv'

f = open('downloaded_urls.csv', 'rb')
data1 = f.read().split('\n')[:-1]
data1 = [line.strip() for line in data1]

o = open(file_name, 'rb')
data = o.read().split('\n')[:-1]
data = [line.strip() for line in data]

count = 0
s = open('left_urls.csv', 'wb')
writer1 = csv.writer(s)
for url in data:
    if url not in data1:
        #print url
        count +=1
        writer1.writerow([url])

print 'left urls::', count

f.close()
o.close()
s.close()


    
