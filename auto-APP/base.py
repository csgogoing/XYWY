#coding=utf-8
from selenium import webdriver

class Init_open(object):
	def __init__(self):
		self.driver = webdriver.Firefox()
		self.driver.get(url)
		self.driver.implicitly_wait(5)
		self.driver.maximize_window()
		self.driver = selenium_driver
		self.base_url = base_url
		self.timeout = 30
		self.parent = parent

	def find_element(self, *loc):
		return self.driver.find_element(*loc)

	def find_elements(self, *loc):
		return self.driver.find_elements(*loc)

	def Load_button(self):
		while True:
			try:
				self.driver.find_element_by_id('loading')
			except:
				break
			else:
				pass

	def close(self):
		self.driver.close()

	def quit(self):
		self.driver.quit()