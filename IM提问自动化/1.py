from bs4 import BeautifulSoup
import requests
import re

url_login='http://test.admin.d.xywy.com/admin/user/login'
url="http://test.admin.d.xywy.com/question/default/index"
headers={
"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
}


req=requests.get(url_login)
m_value = re.findall(r'f" value="(.*)">', req.text)
print(m_value)
cookies=req.cookies.get_dict()
data={
'_csrf':m_value,
'Login[username]':'admin',
'Login[password]':'123456',
'Login[verifyCode]':'testme'
}
req_login=requests.post(url_login,data=data,cookies=cookies)
a_cookies=req_login.cookies.get_dict()



request_qid=req_login.get(url,cookies=a_cookies)
k = request_ele.text
table_forms=re.findall(r'<td>(\d{5})</td>', k)
print(table_forms)