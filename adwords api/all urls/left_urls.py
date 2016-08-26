import pandas as pd

df1 = pd.read_csv('ASIN_BBS_list_1.csv')
df2 = pd.read_csv('ASIN_BBS_list_2.csv')
df3 = pd.read_csv('ASIN_master.csv')

df4 = pd.DataFrame(columns = ['url'])

count = 0
for i, row in df3.iterrows():
    url = row[0]
    #print url
    if (df1.query('url == "' + url + '"').shape[0]==0) and\
       (df2.query('url == "' + url + '"').shape[0]==0):
        df4.loc[count] = url
        count +=1
    
    #break
    
