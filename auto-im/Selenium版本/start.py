from time import sleep
from base import Page
from im_ask import Ask
from im_doc_answer import login
import re
import sys
import random

class Im_Test():
	def __init__(self, did=117333219):
		self.my_doctor = login()
		self.my_doctor.login_doctor(did)
		self.my_ask = Ask()

	def run_test(self, source=200002, q_type=2, pay_amount=300, times=20, firset_dep='内科',second_dep='呼吸内科', is_summary=0, did=117333219, user_id=456654, content=''):
		if source==200002:
			result, order_id = self.my_ask.baidu_page(q_type, user_id=user_id, doctor_ids=did, pay_amount=pay_amount, firset_dep=firset_dep, second_dep=second_dep, content=content)
			if result == False:
				return
			qid = int(self.my_ask.get_id(user_id))
			print('本次提问的qid为%d' %qid)
			if q_type in (1,2):
				self.my_doctor.take_question(qid)
			if times <= 1:
				self.my_doctor.answer_question(qid, is_summary)
			elif 1 < times < 21:
				self.my_doctor.answer_question(qid, is_summary)
				for i in range(times-1):
					self.my_ask.persue(order_id, source, user_id)
					sleep(1)
					self.my_doctor.answer_ques_20(i+2)
					sleep(1)
			else:
				print('times输入错误')
		elif source == 'sgjk':
			result, order_id = self.my_ask.sougou_page(q_type, user_id=user_id, doctor_ids=did, pay_amount=pay_amount, content=content)
			if result == False:
				return
			qid = int(self.my_ask.get_id(user_id))
			print('本次提问的qid为%d' %qid)
			if q_type in (1,2):
				self.my_doctor.take_question(qid)
			if times <= 1:
				self.my_doctor.answer_question(qid, is_summary)
			elif 1 < times < 21:
				self.my_doctor.answer_question(qid, is_summary)
				for i in range(times-1):
					self.my_ask.persue(order_id, source, user_id)
					sleep(1)
					self.my_doctor.answer_ques_20(i+2)
					sleep(1)
			else:
				print('times输入错误')
		else:
			result, order_id = self.my_ask.other_page(resource_id=source, user_id=user_id, q_type=q_type, pay_amount=pay_amount, doctor_ids=did, pay_type=1, content = content)
			if result == False:
				return
			sleep(1)
			#更改问题状态，根据问题是否为指定请求不同接口
			if q_type == 3:
				qid = int(self.my_ask.get_id(user_id, zd=1, did=did))
			else:
				qid = int(self.my_ask.get_id(user_id))
				self.my_doctor.take_question(qid)
			#处理提问失败情况
			if type(qid) != int:
				return
			#根据用户输入的提问次数执行自动化
			if times <= 1:
				self.my_doctor.answer_question(qid, is_summary)
			elif 1 < times < 21:
				self.my_doctor.answer_question(qid, is_summary)
				for i in range(times-1):
					self.my_ask.persue(qid, source, user_id)
					sleep(1)
					self.my_doctor.answer_ques_20(i+2)
					sleep(1)
			else:
				print('times输入错误')

	def quit():
		self.driver.quit()



if __name__ == '__main__':
	#百度悬赏
	#A.run_test(source=200002, q_type=2, times=20, is_summary=1)
	#百度指定
	#A.run_test(source=200002, q_type=3, times=20, is_summary=1)
	#其他悬赏
	#A.run_test(source='xywyapp', q_type=2, times=20, is_summary=1)
	#A.quit()

	#下一步，区分来源，获取用户输入
	# "xywyapp"寻医问药APP
	# "pc"PC
	# "200002"百度
	# "xiaomi"小米
	# "hlwyy"互联网医院
	# "ywb"英威诺
	# "sgjk"搜狗健康

	while True:
		try:
			choose = int(input('''
		1：仅创建问题
		2：创建问题+回答
		3：创建问题+问答20轮次
		4：创建问题+问答自定义
		5: 继续追问已有问题
		其他：退出
请选择：'''))
		except:
			sys.exit('感谢使用')
		else:
			my_ask = Ask()
			while True:
				#选择为1
				if choose == 1:
					try:
						m_source = int(input('''
			问题类型：
				1：百度
				2：寻医问药APP
				3：PC
				4：小米
				5：互联网医院
				6：英威诺
				7：搜狗健康
				其他数字：返回
				空格：退出
请选择：'''))
						if m_source not in range(1,8):
							print('返回上一级菜单')
							break
					except:
						sys.exit('感谢使用')
					else:
						try:
							m_q_type = int(input('''
			提问类型：
				1：免费
				2：悬赏
				3：指定(医生ID：117333219)
				其他数字：返回
				空格：退出
请选择：'''))				
							if m_q_type not in (1,2,3):
								print('返回上一级菜单')
								break
							if m_q_type == 3:
								doctor_id=117333219
							else:
								doctor_id=''
						except:
							sys.exit('感谢使用')
						else:
							user_random = random.randint(9999,999999)
							print('本次提问的userid为%d'%user_random)
							if m_source == 1:
								source = 200002
								result,order_id = my_ask.baidu_page(m_q_type, user_id=user_random, doctor_ids=doctor_id, pay_amount=300, firset_dep='内科', second_dep='呼吸内科')
								if result == True:
									qid = my_ask.get_id(user_random)
									print('本次提问的qid为%d'%qid)
								else:
									print('提问失败')

							elif m_source == 7:
								source = 'sgjk'
								result,order_id = my_ask.sougou_page(m_q_type, user_id=user_random, doctor_ids=doctor_id, pay_amount=300)
								if result == True:
									qid = my_ask.get_id(user_random)
									print('本次提问的qid为%d'%qid)
								else:
									print('提问失败')

							elif m_source in (2,3,4,5,6):
								if m_source == 2:
									source = "xywyapp"
								elif m_source == 3:
									source = "pc"
								elif m_source == 4:
									source = "xiaomi"
								elif m_source == 5:
									source = "hlwyy"
								elif m_source == 6:
									source = "ywb"
								result,order_id = my_ask.other_page(source, user_id=user_random, q_type=m_q_type, doctor_ids=doctor_id, pay_type=1)
								if result == True:
									sleep(1)
									if m_q_type == 3:
										qid = my_ask.get_id(user_random,zd=1,did=doctor_id)
									else:
										qid = my_ask.get_id(user_random)
									print('本次提问的qid为%d'%qid)
								else:
									print('提问失败')
							else:
								print('返回上一级菜单')
								break


				#选择为2
				elif choose ==2:
					try:
						m_source = int(input('''
			问题类型：
				1：百度
				2：寻医问药APP
				3：PC
				4：小米
				5：互联网医院
				6：英威诺
				7：搜狗健康
				其他数字：返回
				空格：退出
请选择：'''))		
						if m_source not in range(1,8):
							print('返回上一级菜单')
							break
					except:
						sys.exit('感谢使用')
					else:
						try:
							m_q_type = int(input('''
			提问类型：
				1：免费
				2：悬赏
				3：指定(医生ID：117333219)
				其他数字：返回
				空格：退出
请选择：'''))				
							if m_q_type not in (1,2,3):
								print('返回上一级菜单')
								break
							if m_q_type == 3:
								doctor_id=117333219
							else:
								doctor_id=''
						except:
							sys.exit('感谢使用')
						else:
							user_random = random.randint(9999,999999)
							print('本次提问的userid为%d'%user_random)
							test_2 =  Im_Test()
							if m_source == 1:
								source = 200002
							elif m_source == 2:
								source = "xywyapp"
							elif m_source == 3:
								source = "pc"
							elif m_source == 4:
								source = "xiaomi"
							elif m_source == 5:
								source = "hlwyy"
							elif m_source == 6:
								source = "ywb"
							elif m_source == 7:
								source = "sgjk"
							else:
								break
							test_2.run_test(source=source, user_id=user_random, q_type=m_q_type, pay_amount=300, times=1, is_summary=0, did=doctor_id)

				elif choose == 3:
					try:
						m_source = int(input('''
			问题类型：
				1：百度
				2：寻医问药APP
				3：PC
				4：小米
				5：互联网医院
				6：英威诺
				7：搜狗健康
				其他数字：返回
				空格：退出
请选择：'''))		
						if m_source not in range(1,8):
							print('返回上一级菜单')
							break
					except:
						sys.exit('感谢使用')
					else:
						try:
							m_q_type = int(input('''
			提问类型：
				1：免费
				2：悬赏
				3：指定(医生ID：117333219)
				其他数字：返回
				空格：退出
请选择：'''))				
							if m_q_type not in (1,2,3):
								print('返回上一级菜单')
								break
							if m_q_type == 3:
								doctor_id=117333219
							else:
								doctor_id=''
						except:
							sys.exit('感谢使用')
						else:
							try:
								is_summary = int(input('''
			是否写总结：
				0：不写总结
				1：写总结
				非数字：退出
请选择：'''))			
							except:
								sys.exit('感谢使用')
							else:
								user_random = random.randint(9999,999999)
								print('本次提问的userid为%d'%user_random)
								test_3 =  Im_Test()
								if m_source == 1:
									source = 200002
								elif m_source == 2:
									source = "xywyapp"
								elif m_source == 3:
									source = "pc"
								elif m_source == 4:
									source = "xiaomi"
								elif m_source == 5:
									source = "hlwyy"
								elif m_source == 6:
									source = "ywb"
								elif m_source == 7:
									source = "sgjk"
								else:
									break
								test_3.run_test(source=source, user_id=user_random, q_type=m_q_type, pay_amount=300, times=20, is_summary=is_summary, did=doctor_id)
								
				elif choose == 4:
					try:
						m_source = input('''
			一.问题类型：
				1：百度
				2：寻医问药APP
				3：PC
				4：小米
				5：互联网医院
				6：英威诺
				7：搜狗健康
				其他：输入类型源码(如xywy)
			二.提问类型：
				1：免费
				2：悬赏
				3：指定
			三.金额(数字，单位分，默认300)
			四.问答轮次(数字，默认1)
			五.一级科室(默认内科)
			六.二级科室(默认呼吸内科)
			六.是否写总结(默认不写总结)
				0：不写总结
				1：写总结
			五.医生ID(数字，默认117333219)
			七.患者ID(数字，默认456654)
			八.问题内容(不可出现英文逗号)

		请以‘英文逗号’分隔，输入所有内容，需按顺序输入，可以为空
		如(1,2,,15)表示百度-悬赏-问答15轮次
请输入：''')
						pat = re.split(r'[,]',m_source)
						#初始化赋值
						t_source = 200002
						t_q_type = 2
						t_pay_amount = 300
						t_times = 20
						t_firset_dep = '内科'
						t_second_dep = '呼吸内科'
						t_is_summary = 0
						t_did = 117333219
						t_user_id = random.randint(9999,999999)
						t_content = ''
						#按顺序循环赋值自定义项
						for i in range(len(pat)):
							if i == 0:
								if pat[i] == '':
									pass
								if pat[i] == '1':
									t_source = 200002
								elif pat[i] == '2':
									t_source = "xywyapp"
								elif pat[i] == '3':
									t_source = "pc"
								elif pat[i] == '4':
									t_source = "xiaomi"
								elif pat[i] == '5':
									t_source = "hlwyy"
								elif pat[i] == '6':
									t_source = "ywb"
								elif pat[i] == '7':
									t_source = "sgjk"
								else:
									t_source = pat[i]

							elif i == 1:
								if pat[i] == '':
									pass
								else:
									t_q_type = int(pat[i])
							elif i == 2:
								if pat[i] == '':
									pass
								else:
									t_pay_amount = int(pat[i])
							elif i == 3:
								if pat[i] == '':
									pass
								else:
									t_times = int(pat[i])
							elif i == 4:
								if pat[i] == '':
									pass
								else:
									t_firset_dep = pat[i]
							elif i == 5:
								if pat[i] == '':
									pass
								else:
									t_second_dep = pat[i]
							elif i == 6:
								if pat[i] == '':
									pass
								else:
									t_is_summary = int(pat[i])
							elif i == 7:
								if pat[i] == '':
									pass
								else:
									t_did = int(pat[i])
							elif i == 8:
								if pat[i] == '':
									pass
								else:
									t_user_id = int(pat[i])
							elif i == 9:
								t_content = pat[i]
							else:
								break
					except:
						sys.exit('感谢使用')
					else:
						test_4 = Im_Test(did=t_did)
						if t_source!=200002 & t_q_type==2:
							t_did = ''
						#兼容其它来源提问，需根据提问方式修改did是否为空
						test_4.run_test(source=t_source,q_type=t_q_type,pay_amount=t_pay_amount,times=t_times,firset_dep=t_firset_dep,second_dep=t_second_dep,is_summary=t_is_summary,did=t_did,user_id=t_user_id,content=t_content)

				elif choose == 5:
					try:
						m_source = input('''
			一.问题id(数字)
				-百度和搜狗来源写入合作问题id，其他来源写入qid
			二.问题来源
				1：百度
				2：寻医问药APP
				3：PC
				4：小米
				5：互联网医院
				6：英威诺
				7：搜狗健康
				其他：输入类型源码(如xywy)
			三.用户id(数字)
		请以‘英文逗号’分隔，输入所有内容，需按顺序输入
请输入：''')
						pat = re.split(r'[,]',m_source)
						#按顺序循环赋值自定义项
						for i in range(len(pat)):
							if i == 0:
								qid = int(pat[i])
							elif i == 1:
								source = int(pat[i])
								if source == 1:
									resource_id = 200002
								elif source == 2:
									resource_id = "xywyapp"
								elif source == 3:
									resource_id = "pc"
								elif source == 4:
									resource_id = "xiaomi"
								elif source == 5:
									resource_id = "hlwyy"
								elif source == 6:
									resource_id = "ywb"
								elif source == 7:
									resource_id = "sgjk"
								else:
									resource_id = source
							elif i == 2:
								user_id = int(pat[i])
							else:
								pass
					except:
						sys.exit('感谢使用')
					else:
						result = my_ask.persue(qid, resource_id, user_id)
						if result == True:
							print('%s来源追问成功'%resource_id)
						else:
							print('追问失败')
				else:
					sys.exit('感谢使用')