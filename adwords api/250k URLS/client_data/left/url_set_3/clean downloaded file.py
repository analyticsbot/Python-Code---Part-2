import os
import pandas as pd
import csv

df = pd.read_csv('dataset.csv')

print df.shape
print df.columns

def f(x):    
   return x['URL'].split()[-1]
   
df['URL_NEW'] = df.apply(f, axis=1)
df['URL'] = df['URL_NEW']
df.pop('URL_NEW')
df.to_csv('dataset_cleaned.csv', sep=',', encoding='utf-8', index =False)

unique_urls = df['URL'].unique()

f = open('downloaded_urls.csv', 'wb')
writer = csv.writer(f)
for url in unique_urls:
    writer.writerow([url])
f.close()


    
