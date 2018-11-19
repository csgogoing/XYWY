#coding=utf-8
from selenium import webdriver
import sys

class Page(object):
	'''
	父类，定义登陆主网址、打开方式，查找元素类等
	'''

	xywy_url = ""

	def __init__(self):
		#初始化
		retry = 1
		while retry < 4:
			try:
				self.driver = webdriver.Firefox()
				self.driver.implicitly_wait(5)
				self.driver.maximize_window()
				self.timeout = 30
			except:
				print('第%d次调起firefox浏览器失败，正在重试，共尝试3次' %retry)
				retry = retry + 1
				if retry == 4:
					print('尝试调起Chrome浏览器')
					r_retry = 1
					while r_retry < 4:
						try:
							self.driver = webdriver.Chrome(executable_path='chromedriver.exe')
							self.driver.implicitly_wait(5)
							self.driver.maximize_window()
							self.timeout = 30
						except:
							print('第%d次调起Chrome浏览器失败，正在重试，共尝试3次' %r_retry)
							r_retry = r_retry + 1
						else:
							break
					sys.exit('无法调起浏览器，请联系管理员')
			else:
				break

	def find_element(self, *loc):
		return self.driver.find_element(*loc)

	def find_elements(self, *loc):
		return self.driver.find_elements(*loc)

	def open(self, url):
		#打开网站
		self.driver.get(url)

	def on_page(self):
		#判断当前网址
		return self.driver.current_url == (self.base_url + self.url)

	def script(self, src):
		return self.driver.execute_script(src)

	def Load_button(self):
		while True:
			try:
				self.driver.find_element_by_id('loading')
			except:
				break
			else:
				pass

	def quit():
		self.driver.quit()