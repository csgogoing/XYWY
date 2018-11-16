#coding=utf-8
import os
import re
import time
from appium import webdriver
global driver
import os
import sys


class Test_appnium:
	def __init__(self):
		# 读取设备 id
		# readDeviceId = list(os.popen('adb devices').readlines())
		# # 正则表达式匹配出 id 信息
		# deviceId = re.findall(r'^\w*\b', readDeviceId[1])[0]
		#设备信息
		desired_caps={
		'newCommandTimeout':600,
		'device':'android',
		'platformName':'Android',
		'browserName':'',
		'version':'',
		'deviceName':'',
		'appPackage':'com.xywy.askxywy',
		'appActivity':'.domain.welcome.activity.WelcomeActivity',
		'unicodeKeyboard':True,
		'resetKeyboard':True
		}
		#打开webdriver，重试3次
		maxTryNum=3
		for tries in range(maxTryNum):
			try:	
				self.driver = webdriver.Remote('http://localhost:4723/wd/hub',desired_caps)
			except:
				if tries < (maxTryNum-1):
					print("连接失败，正在重试")
					continue
				else:
					print('连接手机失败，请尝试重新启动appium客户端')
					sys.exit()
			else:
				time.sleep(5)
				self.driver.implicitly_wait(2)
				print("连接成功")
				# 登陆
				account = '17810354797'
				passwd = 'test123'
				self.fid('com.xywy.askxywy:id/tabMine').click()
				# 判断登陆
				try:
					logined = self.fid('com.xywy.askxywy:id/mine_phone')
				except:
					# 未登陆，登陆
					account_pwd = self.fids('com.xywy.askxywy:id/input_edit_text')
					account_pwd[0].send_keys(account)
					account_pwd[1].send_keys(passwd)
					self.fid('com.xywy.askxywy:id/login_btn_tv').click()
				else:
					# 已登陆，跳过
					self.fid('com.xywy.askxywy:id/ivTabIconLogo').click()
				print("登陆完毕")
				break

	#获得机器屏幕大小x,y
	def getSize(self):
		x = self.driver.get_window_size()['width']
		y = self.driver.get_window_size()['height']
		return (x, y)

	#屏幕向上滑动
	def swipeUp(self, t):
		l = self.getSize()
		x1 = int(l[0] * 0.5)  #x坐标
		y1 = int(l[1] * 0.75)   #起始y坐标
		y2 = int(l[1] * 0.25)   #终点y坐标
		self.driver.swipe(x1, y1, x1, y2,t)
	#屏幕向下滑动
	def swipeDown(self, t):
		l = self.getSize()
		x1 = int(l[0] * 0.5)  #x坐标
		y1 = int(l[1] * 0.25)   #起始y坐标
		y2 = int(l[1] * 0.75)   #终点y坐标
		self.driver.swipe(x1, y1, x1, y2,t)
	#屏幕向左滑动
	def swipLeft(self, t):
		l= self.getSize()
		x1=int(l[0]*0.75)
		y1=int(l[1]*0.5)
		x2=int(l[0]*0.05)
		self.driver.swipe(x1,y1,x2,y1,t)
	#屏幕向右滑动
	def swipRight(self, t):
		l= self.getSize()
		x1=int(l[0]*0.05)
		y1=int(l[1]*0.5)
		x2=int(l[0]*0.75)
		self.driver.swipe(x1,y1,x2,y1,t)

	def fids(self, id):
		#ID查找元素方法
		return self.driver.find_elements_by_id(id)

	def fid(self, id):
		#ID查找元素方法
		return self.driver.find_element_by_id(id)

	def mquit(self):
		#退出driver
		self.driver.quit()
		os.system('adb shell am force-stop com.xywy.askxywy')
		print('程序已退出')

	def is_success(self):
		#点击创建订单存在失败情况，需要重试逻辑及返回成功与失败
		try:
			pass
		except Exception as e:
			raise
		else:
			pass
		finally:
			pass
