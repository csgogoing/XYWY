#coding=utf-8
from auto_appnium import Test_appnium
import time
import random

class find_doctor(Test_appnium):
	def __init__(self):
		super(phone, self).__init__()

	def actions(self, choose):
		# self.swipLeft(1000)
		input_massage = "最近感冒发烧嗓子疼，怎么办啊医生，很久了"
		for i in range(3):
			try:
				self.fid('com.xywy.askxywy:id/finddoc_layout')
			except:
				self.driver.keyevent('4') 
				time.sleep(1)
				continue
			else:
				break
		if choose == 2:
			#预约挂号
			self.fid('com.xywy.askxywy:id/expert_order_orderdoctor_layout').click()
			#输入内容
			self.fid('com.xywy.askxywy:id/et_question_describe').send_keys(input_massage+"杜军医生%d" %random.randrange(1,1000,1))
			time.sleep(1)
			#下一步
			self.fid('com.xywy.askxywy:id/btn_right').click()
			for i in range(1,4):
				try:
					dujun = self.driver.find_element_by_android_uiautomator('new UiSelector().text("杜军")')
				except:
					pass
				else:
					dujun.click()
					temp = 1
					break
			if temp == 1:
				self.fid('com.xywy.askxywy:id/btn_commit').click()
				print("""创建杜军医生订单成功
					""")
			else:
				print("""没有找到杜军医生，创建订单失败
					""")

		elif choose == 3:
			#图文咨询
			self.fid('com.xywy.askxywy:id/expert_order_orderexpert_layout').click()
			#输入内容
			self.fid('com.xywy.askxywy:id/et_question_describe').send_keys(input_massage+"3元%d" %random.randrange(1,1000,1))
			time.sleep(1)
			#下一步
			self.fid('com.xywy.askxywy:id/btn_right').click()
			#选择悬赏提问
			self.fid('com.xywy.askxywy:id/reward_text').click()
			self.fid('com.xywy.askxywy:id/submitBtn').click()
			self.driver.find_element_by_android_uiautomator('new UiSelector().text("将有医生为您快速解答")').click()
			#提交问题
			self.fid('com.xywy.askxywy:id/btn_commit').click()
			print("""创建3元医生订单成功
				""")

		else:
			print("输入函数错误")

