import os
import pandas as pd

df = pd.DataFrame(columns = ['URL', 'Keyword', 'Avg. Monthly Searches'])

directory = 'C:\\Users\\Ravi Shankar\\Documents\\Upwork\\adwords api\\250k URLS\\client_data\\'

for file in os.listdir(directory):
    if file.endswith(".csv"):
        #print file
        temp = pd.read_csv(file, sep = ",", header = None)
        #print temp.shape
        temp.columns = ['URL', 'Keyword', 'Avg. Monthly Searches']
        
        df = pd.concat([df, temp], axis = 0)
        #print df.shape

print df.shape
print len(df['URL'].unique())

df = df.drop_duplicates()
print df.shape

for i in range(9):
    df.iloc[971175*i:971175*(i+1)].to_csv('dataset_final_' +str(i) +'.csv', sep=',', index = False)

master = 'C:\\Users\\Ravi Shankar\\Documents\\Upwork\\adwords api\\all urls\\ASIN_master.csv'
df4 = pd.DataFrame(columns = ['url'])
df3 = pd.read_csv(master)

count = 0
for i, row in df3.iterrows():
    url = row[0]
    #print url
    if (df.query('URL == "' + url + '"').shape[0]==0):
        df4.loc[count] = url
        count +=1
    if count %10000==0:
        print count

print 'urls left :: ', count
