#coding=utf-8
from requests.auth import HTTPBasicAuth
from time import sleep
from lxml import etree
import time
import requests
import re
import sys
import json
import datetime
import pic_rec

class Login(object):
	'''
	'''
	def __init__(self):
		print('开始登陆')
		self.headers={
		"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0"
		}
		if self.jsdh_login():
			if self.yhq_login():
				if self.im_login():
					if self.tiezi_login():
						if self.dianhua_login():
							if self.jiating_login():
								if self.yuyue_login():
									print('所有平台登陆成功!')
								else:
									sys.exit('预约挂号登陆失败')
							else:
								sys.exit('家庭医生登陆失败')
						else:
							sys.exit('电话医生登陆失败')
					else:
						sys.exit('帖子登陆失败')
				else:
					sys.exit('IM登陆失败')
			else:
				sys.exit('医患群登陆失败')			
		else:
			sys.exit('极速电话登陆失败')
		# print(self.jsdh_login())
		# print(self.yhq_login())
		# print(self.im_login())
		# print(self.tiezi_login())
		# print(self.dianhua_login())
		# print(self.jiating_login())
		# print(self.yuyue_login())

	def jsdh_login(self):
		self.jsdh_req = requests.Session()
		self.jsdh_url_login_detect = 'http://admin.jisudianhua.xywy.com/'
		self.jsdh_req.cookies['_csrf']=r'3278db58468bd5e8ce03caa6e40e98cae9859caa4ea81bec02cc79cddaa0c6e3a%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%22d5z8OLInvmtIWeUowXIVkCyZZGIRoMPd%22%3B%7D'
		self.jsdh_req.cookies['PHPSESSID']=r'pfekh1657aasnedttilt3rm931'
		self.jsdh_req.cookies['_identity']=r''
		try:
			req_login = self.jsdh_req.get(self.jsdh_url_login_detect, headers=self.headers)
			if 'Welcome!' in req_login.text:
				return True
			else:
				return False
		except Exception as e:
			print(e)
			sys.exit('请检查VPN及host是否绑定')

	def yhq_login(self):
		self.yhq_req = requests.Session()
		self.yhq_url_login = 'http://yhqadmin.xywy.com/index.php?r=login/index'
		self.yhq_url_pic = 'http://yhqadmin.xywy.com/index.php?r=login/create-verify-code'
		times = 1
		retry = 30
		while True:
			req_token = self.yhq_req.post(self.yhq_url_login, headers=self.headers)
			html = etree.HTML(req_token.text)
			token = html.xpath('//head/meta[4]/@content')[0]
			req_pic = self.yhq_req.get(self.yhq_url_pic, headers=self.headers)
			result = pic_rec.recognition(req_pic.content, 4)		
			data = {
			'_csrf':'%s'%token,
			'LoginForm[uname]':'',
			'LoginForm[password]':'',
			'LoginForm[verify]':'%s'%result,
			'login-button':''
			}
			self.yhq_req.post(self.yhq_url_login, headers=self.headers, data=data)
			login_req = self.yhq_req.get('http://yhqadmin.xywy.com/index.php?r=frame%2Findex', headers=self.headers).text
			if 'wangpan666' in login_req:
				return True
			else:
				if times > retry:
					print('请手动登陆检查账号密码是否有效')
					return False
				else:
					self.yhq_req = requests.Session()
					times = times + 1

	def im_login(self):
		self.im_url_login_detect = 'http://admin.d.xywy.com/'
		self.im_req = requests.Session()
		self.im_req.cookies['_csrf']=r'2c0c77a295c5f1b364dd97663958b91184c2b0f2bc0daa67ebc277399e073615a%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%22oE0Dq8cZ67KcnNHFAgeSz870JiknUj7Z%22%3B%7D'
		self.im_req.cookies['PHPSESSID']=r'qng6k0vipamfu5gmmlri67h300'
		self.im_req.cookies['_identity']=r''
		try:
			req_login = self.im_req.post(self.im_url_login_detect, headers=self.headers)
			if '下架问题列表' in req_login.text:
				return True
			else:
				return False
		except Exception as e:
			print(e)
			print('请检查网络是否通畅')

	def tiezi_login(self):
		self.tiezi_url_login = 'http://cadmin.xywy.com/login.php'
		self.tiezi_auth = HTTPBasicAuth('')
		self.tiezi_req = requests.Session()
		self.tiezi_req.get(self.tiezi_url_login, headers=self.headers, auth=self.tiezi_auth)
		self.tiezi_req.cookies['clubsid']=r''
		data = {
		'backurl':'',
		'username':'',
		'passwd':'',
		'submit':'登陆'.encode('gb2312')
		}
		self.tiezi_req.post(self.tiezi_url_login, headers=self.headers, data=data, auth=self.tiezi_auth)
		login_req = self.tiezi_req.get('http://cadmin.xywy.com/main.php', headers=self.headers, auth=self.tiezi_auth).content.decode('gb2312', errors='ignore')
		if '欢迎进入' in login_req:
			return True
		else:
			return False

	def dianhua_login(self):
		self.dianhua_url_login = 'http://dhys.z.xywy.com/login.php'
		self.dianhua_url_pic = 'http://dhys.z.xywy.com/captcha.php'
		self.dianhua_req = requests.Session()
		times = 1
		retry = 5
		while True:
			req_pic = self.dianhua_req.get(self.dianhua_url_pic, headers=self.headers)
			result = pic_rec.recognition(req_pic.content, 5)
			data = {
			'backurl':'',
			'username':'',
			'passwd':'',
			'img_code':'%s'%result,
			'submit':'登陆'.encode('gb2312')
			}
			self.dianhua_req.post(self.dianhua_url_login, headers=self.headers, data=data)
			login_req = self.dianhua_req.get('http://dhys.z.xywy.com/main.php', headers=self.headers).content.decode('gb2312', errors='ignore')
			if '欢迎进入' in login_req:
				return True
			else:
				if times > retry:
					print('请手动登陆检查账号密码是否有效')
					return False
				else:
					times = times + 1

	def jiating_login(self):
		self.tiezi_auth = HTTPBasicAuth()
		self.jiating_url_login = 'http://cadmin.xywy.com/login.php'
		self.jiating_req = requests.Session()
		self.jiating_req.get(self.jiating_url_login, headers=self.headers, auth=self.tiezi_auth)
		self.jiating_req.cookies['clubsid']=r''
		data = {
		'backurl':'',
		'username':'',
		'passwd':'',
		'submit':'登陆'.encode('gb2312')
		}
		self.jiating_req.post(self.jiating_url_login, headers=self.headers, data=data, auth=self.tiezi_auth)
		login_req = self.jiating_req.get('http://cadmin.xywy.com/main.php', headers=self.headers, auth=self.tiezi_auth).content.decode('gb2312', errors='ignore')
		if '欢迎进入' in login_req:
			return True
		else:
			return False

	def yuyue_login(self):
		self.yuyue_url_login = 'http://fzadmin.z.xywy.com/login.php'
		self.yuyue_url_pic = 'http://fzadmin.z.xywy.com/captcha.php'
		self.yuyue_req = requests.Session()
		times = 1
		retry = 5
		while True:
			req_pic = self.yuyue_req.get(self.yuyue_url_pic, headers=self.headers)
			result = pic_rec.recognition(req_pic.content, 5)
			data = {
			'backurl':'',
			'username':'',
			'passwd':'',
			'img_code':'%s'%result,
			'submit':'登陆'.encode('gb2312')
			}
			self.yuyue_req.post(self.yuyue_url_login, headers=self.headers, data=data)
			login_req = self.yuyue_req.get('http://fzadmin.z.xywy.com/main.php', headers=self.headers).content.decode('gb2312', errors='ignore')
			if '欢迎进入' in login_req:
				return True
			else:
				if times > retry:
					print('请手动登陆检查账号密码是否有效')
					return False
				else:
					times = times + 1


if __name__ == '__main__':
	#测试运行
	A = Login(datetime.datetime.now())
