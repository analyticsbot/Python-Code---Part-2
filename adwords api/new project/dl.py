import requests, shutil

f = open('keywords.csv', 'rb')
data = f.read().split('\n')[:-1]
data = [d.strip() for d in data][4:10]

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

## request file
for key in data:
    print 'getting data for', key
    url_key = 'https://www.merchantwords.com/search/' + '-'.join(key.split()) + '.csv'
    r = s.get(url_key, stream=True, headers = headers, proxies=proxies, auth=auth)
    if r.status_code == 200:
        with open('-'.join(key.split()) + '.csv', 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)
    else:
        print 'Error. Server didnt respond well'

