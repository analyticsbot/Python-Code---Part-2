import csv

o = open('all_left_urls.csv')
data = o.read().split('\n')[:-1]
data = [l.strip() for l in data]

x = len(data)/3
c = 0

for i in range(3):
    f = open('all_left_urls' + str(i) + '.csv', 'wb')
    temp = data[i*x:(i+1)*x]
    c += len(temp) 
    writer = csv.writer(f)
    for line in temp:
        line = line.strip()
        writer.writerow([line])
    f.close()

print c
o.close()
        
        
