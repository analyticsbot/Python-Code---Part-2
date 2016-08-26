import os
import pandas as pd
import csv

urls = []

directory = 'C:\\Users\\Ravi Shankar\\Documents\\Upwork\\adwords api\\250k URLS\\'

subdirectory = [x[0] for x in os.walk(directory)]

for dir_ in subdirectory:
    if dir_.startswith('left_'):
        print dir_
        for file in os.listdir(dir_):
            if file == 'left_urls.csv':
                print dir_+ '\\' + file
                f = open(dir_+ '\\' + file, 'rb')
                data = f.read().split('\n')[:-1]
                data = [line.strip() for line in data]
                urls.extend(data)
                f.close()

print len(urls)


o = open('left_left_urls.csv', 'wb')
writer = csv.writer(o)

for line in urls:
    line = line.strip()
    writer.writerow([line])
o.close()
    
