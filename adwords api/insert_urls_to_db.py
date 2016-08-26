import sqlite3, hashlib

## open connection to sqlite3 db
conn = sqlite3.connect('urls')
print "Opened database connection successfully!!"
c = conn.cursor()

## read the file contents
f = open('TestRun.csv', 'rb')
data = f.read().split('\n')[:-1]

## iterate through file and insert to db
for url in data:
    url = url.strip().replace(',', '')
    url_hash = hashlib.md5(url).hexdigest()

    c.execute("INSERT INTO all_urls (url, url_hash) values(?, ?)", (url, url_hash),)
    conn.commit()

## close connection
conn.close()
