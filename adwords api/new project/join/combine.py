import os
import pandas as pd

row_in_each_csv = 971175 ## number of rows in each csv

df = pd.DataFrame(columns = ['phrase','volume'])

directory = 'patht to folder'

for file in os.listdir(directory):
    if file.endswith(".csv"):
        temp = pd.read_csv(directory + '/' + file, sep = ",")
        df = pd.concat([df, temp], axis = 0)

print 'total rows', df.shape

count = 0
while True:
    from_ = row_in_each_csv*count
    to_ = row_in_each_csv*(count+1)
    print from_, to_
    if df[from_:to_].shape[0] != 0:
        df[971175*count:971175*(count+1)].to_csv('dataset_' + str(count+1)+'.csv')
        count +=1
    else:
        break
    
    
