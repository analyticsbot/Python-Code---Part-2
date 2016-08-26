import urllib  
import urllib2  
import re  
import cookielib  
  
jar = cookielib.FileCookieJar("cookie")  
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(jar))  
  
email = 'susan@notaisltd.com'
password = '1BS1lse2s'

# url for login        
url = 'https://www.merchantwords.com/login'

user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)' 
  
data =  {  
       
         "email":email,  
        "password":password,  
}  
  
data = urllib.urlencode(data)  
login_request = urllib2.Request(url, data)  
login_reply = opener.open(login_request)  
login_reply_data = login_reply.read() 
