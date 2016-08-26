import os
import pandas as pd

df = pd.DataFrame(columns = ['URL', 'Keyword', 'Avg. Monthly Searches'])

directory = 'C:\\Users\\Ravi Shankar\\Documents\\Upwork\\adwords api\\100k url 1st LOT\\'

subdirectory = [x[0] for x in os.walk(directory)]

for dir_ in subdirectory:
    for file in os.listdir(dir_):
        if file.endswith(".xlsx"):
            temp = pd.read_excel(dir_ + '/' + file)
            df = pd.concat([df, temp], axis = 0)
    if dir_ == 'url_set_3':
        for file in os.listdir(dir_):
            if file.endswith(".txt"):
                temp = pd.read_csv(dir_ + '/' + file, sep = " ", header = None)
                temp.columns = ['url', 'keyword', 'searches']
                df = pd.concat([df, temp], axis = 0)

print df.shape
print len(df['URL'].unique())

>>> df.to_csv('dataset.txt', sep='\t', encoding='utf-8')
>>> df.iloc[:971175].to_csv('dataset.csv', sep=',', encoding='utf-8')
>>> df.iloc[971175:].to_csv('dataset1.csv', sep=',', encoding='utf-8')
>>> df['URL'].to_csv('urls_downloaded.csv', sep=',', encoding='utf-8')
>>> df['URL'].unique().to_csv('unique_urls_downloaded.csv', sep=',', encoding='utf-8')
