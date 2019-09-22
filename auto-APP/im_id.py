#coding=utf-8

from time import sleep
from base import Init_open
import urllib


class Im_id(Init_open):
	def __int__(self):
		pass

	def Load_button(self):
		while True:
			try:
				self.driver.find_element_by_id('loading')
			except:
				break
			else:
				pass

	def Actions(self):
		#登陆
		self.driver.find_element_by_name('Login[username]').send_keys('admin')
		self.driver.find_element_by_name('Login[password]').send_keys('123456')
		self.driver.find_element_by_name('Login[verifyCode]').send_keys('testme')
		self.driver.find_element_by_xpath('/html/body/div/div[2]/form/div[4]/div[2]/button').click()
		sleep(2)
		#进入我的账号问题列表页
		js1 = 'window.open("http://test.admin.d.xywy.com/question/default/index?QuestionBaseSearch[keyword_type]=patient_phone&QuestionBaseSearch[keyword]=17810354797");'
		self.driver.execute_script(js1)
		handles = self.driver.window_handles
		self.driver.switch_to_window(handles[1])
		#获取问题ID
		id = self.driver.find_element_by_xpath('/html/body/div[1]/div[1]/section[2]/div/div/div[1]/div[2]/table/tbody/tr[1]/td[1]').text
		urllib.request.urlopen('http://test.admin.d.xywy.com/site/question-order-pay-status?qid=%s' %id)
		self.quit()


if __name__ == '__main__':
	doctor = Im_id('http://test.admin.d.xywy.com/question/default/index')

