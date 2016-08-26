import os
import pandas as pd

row_in_each_csv = 971175 ## number of rows in each csv
debug =  False # make it False on big Files

df = pd.DataFrame(columns = ['phrase','volume'])

directory = 'C:\\Users\\Ravi Shankar\\Documents\\Upwork\\adwords api\\new project\\join\\Files\\Files\\'

for file in os.listdir(directory):
    if file.endswith(".csv"):
        f = open(file, 'rb')
        data = f.read()
        if 'doctype' in data.lower():
            continue
        temp = pd.read_csv(directory + '/' + file, sep = ",")
        if debug: print 'Reading file ::', file
        df = pd.concat([df, temp], axis = 0)

print 'total rows in all the file is  :: ', df.shape
print 'Writing to output csv'

count = 0
while True:
    from_ = row_in_each_csv*count
    to_ = row_in_each_csv*(count+1)
    
    if df[from_:to_].shape[0] != 0:
        df[from_:to_].to_csv('dataset_' + str(count+1)+'.csv', index = False)
        if debug: print 'dataset_' + str(count+1)+'.csv' + ' written with ' +df[from_:to_].shape[0] + ' rows.  Check'
        count +=1
    else:
        break
    
    
