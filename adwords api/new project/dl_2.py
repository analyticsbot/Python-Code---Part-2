import requests, shutil, time, datetime, random

f = open('keywords.csv', 'rb')
data = f.read().split('\n')[:-1]
data = [d.strip() for d in data]

# credentials
email = 'susan@notaisltd.com'
password = '1BS1lse2s'

# url for login        
url = 'https://www.merchantwords.com/login'

## add headers
headers = {'content-type': 'application/json', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

## login
s = requests.session()
auth = ('rbot', 'myname')
proxies = {'http': 'http://us-ca.proxymesh.com:31280'}
login_data = dict(email=email, password=password)
s.post(url, data=login_data,  proxies=proxies, auth=auth)
print s.cookies
pp = ['https://91.221.61.126:3128',
'https://165.138.66.32:8080',
'https://112.199.74.123:80',
'https://103.233.77.227:8080',
'https://165.138.66.247:8080',
'https://221.139.253.138:3128',
'https://46.48.145.196:3128',
'https://115.160.137.140:8088',
'https://157.7.242.125:8080',
'https://177.91.28.128:8080',
'https://89.163.131.168:3128',
'https://187.108.41.130:80',
'https://189.8.195.2:80',
'https://152.44.90.101:8080',
'https://157.7.128.215:8080',
'https://196.46.186.217:8080',
'https://51.254.103.206:3128',
'https://186.229.16.154:80',
'https://183.111.169.207:3128',
'https://157.7.131.252:8080',
'https://181.14.245.194:8000',
'https://183.111.169.203:3128',
'https://181.14.245.234:8000',
'https://138.185.149.246:80',
'https://179.185.104.114:80',
'https://103.42.56.85:3128',
'https://221.139.253.135:3128',
'https://221.139.253.133:3128',
'https://165.139.149.169:3128',
'https://212.118.22.39:8080',
'https://202.62.85.186:8080',
'https://152.44.90.102:8080',
'https://186.213.60.39:80',
'https://50.30.152.130:8086',
'https://210.140.192.11:80',
'https://201.131.47.102:8080',
'https://115.113.241.197:80',
'https://84.23.107.195:8080',
'https://31.173.74.73:8080',
'https://54.238.203.127:80'
]

a = datetime.datetime.now()

count = 0
## request file
for key in data:
    count +=1
    if count % 5==0:
        proxies = {'http': random.choice(pp)}
    
    url_key = 'https://www.merchantwords.com/search/' + '-'.join(key.split()) + '.csv'
    r = s.get(url_key, stream=True, headers = headers, proxies=proxies)
    #print r.content
    if (r.status_code == 200) and ('Hang' not in r.content):
        print 'getting data for', key
        print 'Hang' in r.content
        with open('-'.join(key.split()) + '.txt', 'wb') as f:
            f.write(r.content)
    else:
        print 'Error. Server didnt respond well'
        while True:
            time.sleep(10)
            proxies = {'http': random.choice(pp)}
            r = s.get(url_key, stream=True, headers = headers, proxies=proxies)
            if (r.status_code == 200) and ('Hang' not in r.content):
                break

b = datetime.datetime.now()
c = b - a
print c.seconds
