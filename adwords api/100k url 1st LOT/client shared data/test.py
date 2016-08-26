import pandas as pd

df = pd.read_csv('all_downloaded.csv')
df1 = pd.read_csv('dataset.csv')
df2 = pd.read_csv('dataset1.csv')

print 'df -- ', df.shape
print 'df1 -- ', df1.shape
print 'df2 -- ', df2.shape

df = df.drop_duplicates()
df1 = df1.drop_duplicates()
df2 = df2.drop_duplicates()

df.to_csv('dataset2_deduped.csv')
df1.to_csv('dataset_deduped.csv')
df2.to_csv('dataset1_deduped.csv')

print '\n'
print 'df -- ', df.shape
print 'df1 -- ', df1.shape
print 'df2 -- ', df2.shape

print 'df url-- ', len(df['URL'].unique())
print 'df1 url-- ', len(df1['URL'].unique())
print 'df2 url -- ', len(df2['URL'].unique())

print len(df['URL'].unique()) + len(df1['URL'].unique()) + len(df2['URL'].unique())

