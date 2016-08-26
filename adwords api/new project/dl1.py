import requests, shutil

auth = requests.auth.HTTPProxyAuth('RBOT', 'myname')
proxies = {'http': 'http://us-ca.proxymesh.com:31280'}
##response = requests.get('http://analyticsbot.ml', proxies=proxies, auth=auth)

f = open('keywords.csv', 'rb')
data = f.read().split('\n')[:-1]
data = [d.strip() for d in data][:1]

# credentials
email = 'susan@notaisltd.com'
password = '1BS1lse2s'

# url for login        
url = 'https://www.merchantwords.com/login'
auth = ('rbot', 'myname')
proxies = {'http': 'http://us-ca.proxymesh.com:31280'}
login_data = dict(email=email, password=password)

## add headers
headers = {'content-type': 'application/json', \
           'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',\
           'referer':'https://www.merchantwords.com/'}

response = requests.post(url, data=login_data, headers = headers, proxies=proxies, auth=auth)

cookie = response.cookies.get_dict()
print cookie

#### request file
for key in data:
    print 'getting data for', key
    url_key = 'https://www.merchantwords.com/search/' + '-'.join(key.split()) + '.csv'
    r = requests.get(url_key, cookies = cookie, stream=True, headers = headers, proxies=proxies, auth=auth)
    if r.status_code == 200:
        with open('-'.join(key.split()) + '.csv', 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)
    else:
        print 'Error. Server didnt respond well'
