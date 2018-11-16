#coding=utf-8
from auto_appnium import Test_appnium
import time
import random

class quick_ask(Test_appnium):
	def __init__(self):
		super(quick_ask, self).__init__()

	def Auto_pay(self, id):
		pass

	def actions(self, choose):
		# self.swipLeft(1000)
		input_massage = "怀孕了怎么办，怀孕了应该怎么办，妇产科问题"
		#寻找快速问诊按钮
		for i in range(4):
			try:
				self.fid('com.xywy.askxywy:id/quick_ask_layout')
			except:
				if i < 4:
					self.driver.keyevent('4')
					time.sleep(1)
					continue
				else:
					print('找不到快速问诊按钮')
					self.driver.quit()
			else:
				break
		#根据类型完成测试
		if choose == 1:
			#快速问诊
			self.fid('com.xywy.askxywy:id/quick_ask_layout').click()
			#输入内容
			self.fid('com.xywy.askxywy:id/et_question_describe').send_keys(input_massage+"三湘四水医生%d" %random.randrange(1,1000,1))
			time.sleep(1)
			#下一步
			self.fid('com.xywy.askxywy:id/next_txt').click()
			for i in range(1,4):
				try:
					dujun = self.driver.find_element_by_android_uiautomator('new UiSelector().text("三湘四水")')
				except:
					pass
				else:
					dujun.click()
					temp = 1
					break
			if temp == 1:
				self.fid('com.xywy.askxywy:id/btn_commit').click()
				if self.is_success():
					pass
				else:
					print("""创建订单失败，请检查网络环境
					""")
			else:
				print("""没有找到三湘四水医生，创建订单失败
					""")

		elif choose == 2:
			#快速问诊
			self.fid('com.xywy.askxywy:id/quick_ask_layout').click()
			#输入内容
			self.fid('com.xywy.askxywy:id/et_question_describe').send_keys(input_massage+"3元%d" %random.randrange(1,1000,1))
			time.sleep(1)
			#下一步
			self.fid('com.xywy.askxywy:id/next_txt').click()
			#选择悬赏提问
			self.fid('com.xywy.askxywy:id/reward_text').click()
			self.fid('com.xywy.askxywy:id/submitBtn').click()
			self.driver.find_element_by_android_uiautomator('new UiSelector().text("将有医生为您快速解答")').click()
			#提交问题
			self.fid('com.xywy.askxywy:id/btn_commit').click()
			
			print("""创建3元医生订单成功
				""")

		elif choose == 3:
			#快速问诊
			self.fid('com.xywy.askxywy:id/quick_ask_layout').click()
			#输入内容
			self.fid('com.xywy.askxywy:id/et_question_describe').send_keys(input_massage+"5元%d" %random.randrange(1,1000,1))
			time.sleep(1)
			#下一步
			self.fid('com.xywy.askxywy:id/next_txt').click()
			#选择悬赏提问
			self.fid('com.xywy.askxywy:id/reward_text').click()
			self.fid('com.xywy.askxywy:id/submitBtn').click()
			self.driver.find_element_by_android_uiautomator('new UiSelector().text("二甲及以上级别医生为您服务")').click()
			#提交问题
			self.fid('com.xywy.askxywy:id/btn_commit').click()
			print("""创建5元医生订单成功
				""")

		elif choose == 4:
			#快速问诊
			self.fid('com.xywy.askxywy:id/quick_ask_layout').click()
			#输入内容
			self.fid('com.xywy.askxywy:id/et_question_describe').send_keys(input_massage+"10元%d" %random.randrange(1,1000,1))
			time.sleep(1)
			#下一步
			self.fid('com.xywy.askxywy:id/next_txt').click()
			#选择悬赏提问
			self.fid('com.xywy.askxywy:id/reward_text').click()
			self.fid('com.xywy.askxywy:id/submitBtn').click()
			self.driver.find_element_by_android_uiautomator('new UiSelector().text("二甲医院以上级别医生为您解答")').click()
			#提交问题
			self.fid('com.xywy.askxywy:id/btn_commit').click()
			print("""创建10元医生订单成功
				""")

		elif choose == 5:
			#快速问诊
			self.fid('com.xywy.askxywy:id/quick_ask_layout').click()
			#输入内容
			self.fid('com.xywy.askxywy:id/et_question_describe').send_keys(input_massage+"免费%d" %random.randrange(1,1000,1))
			time.sleep(1)
			#下一步
			self.fid('com.xywy.askxywy:id/next_txt').click()
			#选择悬赏提问
			self.fid('com.xywy.askxywy:id/reward_text').click()
			self.fid('com.xywy.askxywy:id/submitBtn').click()
			#点击免费提问
			self.fid('com.xywy.askxywy:id/reward_skip_to_ask').click()
			print("""创建免费订单成功
				""")

		else:
			print("输入函数错误，创建订单失败")

