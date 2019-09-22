#coding=utf-8

from time import sleep
from base import Init_open


class Im_doctor(Init_open):
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

	def Actions(self, mtype):
		#登陆
		if mtype == 1:
			id = 117333237
		else:
			id = 117333219
		self.driver.find_element_by_name('userlogin').send_keys('admin')
		self.driver.find_element_by_name('password').send_keys('123456')
		self.driver.find_element_by_xpath('//*[@id="loginForm"]/div[4]/button').click()
		sleep(2)
		#进入IM问答页
		js1 = 'window.open("http://test.dr.xywy.com/account/pc-login?id=436558&user_id=%d");' %id
		self.driver.execute_script(js1)
		sleep(1)
		js2 = 'window.open("http://test.d.xywy.com/doctor-client/im");'
		self.driver.execute_script(js2)
		handles = self.driver.window_handles
		self.driver.switch_to_window(handles[1])
		#问题库抢题
		self.Load_button()
		#点击第1个问题
		#self.driver.find_element_by_xpath('//*[@id="mCSB_2_container"]').click()
		while True:
			self.driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div[1]/div[1]/div[2]/span[1]').click()
			sleep(1)
			My_questions = self.driver.find_elements_by_class_name('message-user-item')
			try:
			 	My_questions[0].click()
			except:
			 	pass
			else:
				My_questions[0].click()
				break
		self.Load_button()
		self.driver.find_element_by_link_text('抢题').click()
		#点击处理中标签
		self.Load_button()
		self.driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div[1]/div[1]/div[1]/span[1]').click()
		self.Load_button()
		self.driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div[2]/div[1]/div[6]/div[1]/ul/li[1]').click()
		sleep(1)
		self.driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div[2]/div[1]/div[6]/div[1]/ul/li[1]').click()
if __name__ == '__main__':
	doctor = Im_doctor('http://test.dr.xywy.com/site/login')
	doctor.Actions(1)

