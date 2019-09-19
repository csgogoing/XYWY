import requests


#下面是一些测试代码。  
if __name__ == "__main__":  
	url = 'http://admin.d.xywy.com/admin/user/captcha?v=5c91fdf5527cc'
	headers={
		"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0"
	}
	for i in range(2):
		req = requests.get(url, headers=self.headers)
		f = open('%d.jpg'%i, 'w') # 若是'wb'就表示写二进制文件
		f.write(req.content)
		f.close()