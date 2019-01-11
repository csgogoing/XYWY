from time import sleep
#from base import Page
from im_ask import Ask
#from im_doc_answer_browser import login_browser
from im_doc_answer import login
from result import write_result
from xlutils.copy import copy
import re
import sys
import random
import os
import xlrd

class Im_Test():
	#主类
	def __init__(self, did=117333219, times=1):
		self.did = did
		if times == 0:
			self.my_ask = Ask()
		else:
			#self.my_doctor = login_browser()
			#self.my_doctor.login_doctor(did)
			self.my_doctor = login(did)
			self.my_ask = Ask()

	def run_test(self, source=200002, q_type=2, pay_amount=300, times=20, firset_dep='内科',second_dep='呼吸内科', is_summary=0, user_id=456654, content='', doc_id='', pay_type=1):
		if source==200002:
			#百度来源提问
			result, order_id = self.my_ask.baidu_page(q_type, user_id=user_id, doctor_ids=doc_id, pay_amount=pay_amount, firset_dep=firset_dep, second_dep=second_dep, content=content)
			if result == False:
				raise Exception('提问失败')
			qid, uid = self.my_ask.get_id(order_id=order_id)
			#处理提问失败情况
			if qid == None:
				raise Exception('获取问题ID失败')
			else:
				print('本次提问的qid为%d' %qid)
			self.my_ask.persue(order_id, source, uid, 1, self.did)
			if times == 0:
				return qid
			elif 0 < times < 21:
				if q_type in (1,2):
					#查看问题库是否存在该题
					is_pool = self.my_doctor.question_pool(qid)
					if is_pool == False:
						raise Exception('此医生无法看到该问题，qid=%d'%qid)
					result = self.my_doctor.take_question(qid)
					if result == False:
						raise Exception('抢题失败，qid=%d'%qid)
				result = self.my_doctor.answer_question(qid, uid, is_summary)
				if result == False:
					raise Exception('写总结失败，qid=%d'%qid)
				for i in range(times-1):
					#根据用户输入的提问次数执行自动化
					self.my_ask.persue(order_id, source, uid, i+2, self.did)
					sleep(1)
					self.my_doctor.reply(i+2)
					sleep(1)
			else:
				raise Exception('问答轮次不得超过20')

		elif source == 'sgjk':
			#搜狗来源提问
			result, order_id = self.my_ask.sougou_page(q_type, user_id=user_id, doctor_ids=doc_id, pay_amount=pay_amount, content=content)
			if result == False:
				raise Exception('提问失败')
			qid, uid = self.my_ask.get_id(order_id=order_id)
			#处理提问失败情况
			if qid == None:
				raise Exception('获取问题ID失败')
			else:
				qid = int(qid)
				print('本次提问的qid为%d' %qid)
			self.my_ask.persue(order_id, source, uid, 1, self.did)
			if times == 0:
				return qid
			elif 0 < times < 21:
				if q_type in (1,2):
					#查看问题库是否存在该题
					is_pool = self.my_doctor.question_pool(qid)
					if is_pool == False:
						raise Exception('此医生无法看到该问题，qid=%d'%qid)
					result = self.my_doctor.take_question(qid)
					if result == False:
						raise Exception('抢题失败，qid=%d'%qid)
				result = self.my_doctor.answer_question(qid, uid, is_summary)
				if result == False:
					raise Exception('写总结失败，qid=%d'%qid)
				for i in range(times-1):
					#根据用户输入的提问次数执行自动化
					self.my_ask.persue(order_id, source, uid, i+2, self.did)
					sleep(1)
					self.my_doctor.reply(i+2)
					sleep(1)
			else:
				raise Exception('问答轮次不得超过20')

		elif source == 'ywb':
			#英威诺来源
			result, order_id = self.my_ask.other_page(resource_id=source, user_id=user_id, q_type=q_type, pay_amount=pay_amount, doctor_ids=doc_id, pay_type=1, content = content)
			if result == False:
				raise Exception('提问失败')
			sleep(1)
			#更改问题状态，根据问题是否为指定请求不同接口
			qid, uid = self.my_ask.get_id(order_id=order_id)
			#处理提问失败情况
			if qid == None:
				raise Exception('获取问题ID失败')
			else:
				qid = int(qid)
				print('本次提问的qid为%d' %qid)
			self.my_ask.persue(qid, source, uid, 1, self.did)
			if times == 0:
				return qid
			elif 0 < times < 21:
				if q_type in (1,2):
					#查看问题库是否存在该题
					is_pool = self.my_doctor.question_pool(qid)
					if is_pool == False:
						raise Exception('此医生无法看到该问题，qid=%d'%qid)
					result = self.my_doctor.take_question(qid)
					if result == False:
						raise Exception('抢题失败，qid=%d'%qid)
				result = self.my_doctor.answer_question(qid, uid, is_summary)
				if result == False:
					raise Exception('写总结失败，qid=%d'%qid)
				for i in range(times-1):
					#根据用户输入的提问次数执行自动化
					self.my_ask.persue(qid, source, uid, i+2, self.did)
					sleep(1)
					self.my_doctor.reply(i+2)
					sleep(1)
			else:
				raise Exception('问答轮次不得超过20')

		else:
			#其他来源提问
			result, order_id = self.my_ask.other_page(resource_id=source, user_id=user_id, q_type=q_type, pay_amount=pay_amount, doctor_ids=doc_id, pay_type=pay_type, content = content)
			if result == False:
				raise Exception('提问失败')
			sleep(1)
			#更改问题状态，根据问题是否为指定请求不同接口
			if q_type == 3:
				qid, uid = self.my_ask.get_id(user_id=user_id, zd=1, did=self.did)
			else:
				qid, uid = self.my_ask.get_id(user_id=user_id)
			#处理提问失败情况
			if qid == None:
				raise Exception('获取问题ID失败')
			else:
				qid = int(qid)
				print('本次提问的qid为%d' %qid)
			self.my_ask.persue(qid, source, uid, 1, self.did)
			if times == 0:
				return qid
			elif 0 < times < 21:
				if q_type in (1,2):
					#查看问题库是否存在该题
					is_pool = self.my_doctor.question_pool(qid)
					if is_pool == False:
						raise Exception('此医生无法看到该问题，qid=%d'%qid)
					result = self.my_doctor.take_question(qid)
					if result == False:
						raise Exception('抢题失败，qid=%d'%qid)
				result = self.my_doctor.answer_question(qid, uid, is_summary)
				if result == False:
					raise Exception('写总结失败，qid=%d'%qid)
				for i in range(times-1):
					#根据用户输入的提问次数执行自动化
					self.my_ask.persue(qid, source, uid, i+2, self.did)
					sleep(1)
					self.my_doctor.reply(i+2)
					sleep(1)
			else:
				raise Exception('问答轮次不得超过20')

		print("-------------------------本条用例测试通过-------------------------")
		return qid



if __name__ == '__main__':
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
		1：快速创建问题
		2：问答自定义(请编辑data.xls文件，并关闭测试医生IM窗口)
		3: 继续追问已有问题
		4：更改问题状态为已支付
		其他：退出
请选择：'''))
		except:
			print('感谢使用')
			sleep(1)
			sys.exit()
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
				其他：返回主菜单
请选择：'''))
						if m_source not in range(1,8):
							print('问题类型错误，返回主菜单')
							break
					except:
						print('返回主菜单')
						break
					else:
						try:
							m_q_type = int(input('''
			提问类型：
				1：免费
				2：悬赏
				3：指定(医生ID：117333219)
				其他：返回主菜单
请选择：'''))				
							if m_q_type not in (1,2,3):
								print('提问类型错误，返回主菜单')
								break
							if m_q_type == 3:
								doctor_id=117333219
							else:
								doctor_id=''
						except:
							print('返回主菜单')
							break
						else:
							user_random = random.randint(9999,999999)
							if m_source == 1:
								source = 200002
								result,order_id = my_ask.baidu_page(m_q_type, user_id=user_random, doctor_ids=doctor_id, pay_amount=300, firset_dep='内科', second_dep='呼吸内科')
								qid,uid = my_ask.get_id(order_id=order_id)
								if qid == None:
									pass
								else:
									print('本次提问的qid为%d'%qid)

							elif m_source == 7:
								source = 'sgjk'
								result,order_id = my_ask.sougou_page(m_q_type, user_id=user_random, doctor_ids=doctor_id, pay_amount=300)
								qid,uid = my_ask.get_id(order_id=order_id)
								if qid == None:
									pass
								else:
									print('本次提问的qid为%d'%qid)

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
								if m_q_type == 3:
									qid,uid = my_ask.get_id(user_id=user_random,zd=1,did=doctor_id)
								else:
									qid,uid = my_ask.get_id(user_id=user_random)
								if qid == None:
									pass
								else:
									print('本次提问的qid为%d'%qid)
							else:
								print('返回主菜单')
								break

				elif choose == 3:
					try:
						m_source = input('''
		请以‘英文逗号’分隔，以下所有内容必填，需按顺序输入
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
请输入：''')
						pat = re.split(r'[,]',m_source)
						if len(pat) != 3:
							print('输入错误，返回主菜单')
							break
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
						print('返回主菜单')
						break
					else:
						result = my_ask.persue(qid, resource_id, user_id, 0)
						if result == True:
							print('%s来源追问成功'%resource_id)
						else:
							print('追问失败')

				elif choose == 4:
					try:
						m_qid = int(input('''
请输入qid：'''))
					except:
						print('qid输入错误，返回主菜单')
						break
					else:
						result = my_ask.pay_question(qid)
						if result == True:
							print('qid:%d支付成功'%m_qid)
						else:
							print('qid:%d支付失败'%m_qid)

				elif choose == 2:
					try:
						excel_path=os.getcwd()+r'/data.xls'
						book=xlrd.open_workbook(excel_path)
						sheet=book.sheet_by_index(0)
						nrows=sheet.nrows
						wrt = write_result(excel_path)
						for row in range(1,nrows):
						#循环执行excel
							try:
								pat=sheet.row_values(row)
								#初始化赋值
								t_pay_amount = 300
								t_pay_type = 1
								t_times = 20
								t_firset_dep = '内科'
								t_second_dep = '呼吸内科'
								t_is_summary = 0
								t_did = 117333219
								t_user_id = random.randint(9999,999999)
								t_content = ''
								if pat[0] == '':
									print('请向excel中输入数据')
									break
								#按顺序循环赋值自定义项
								for i in range(len(pat)):
									if i == 0:
										if pat[i] == '':
											raise Exception('请输入问题来源')
										elif type(pat[i]) != float:
											t_source = pat[i]
											name_source = t_source
										elif int(pat[i]) == 1:
											t_source = 200002
											name_source = '百度'
										elif int(pat[i]) == 2:
											t_source = "xywyapp"
											name_source = '寻医问药APP'
										elif int(pat[i]) == 3:
											t_source = "pc"
											name_source = 'PC'
										elif int(pat[i]) == 4:
											t_source = "xiaomi"
											name_source = '快应用'
										elif int(pat[i]) == 5:
											t_source = "hlwyy"
											name_source = '互联网医院'
										elif int(pat[i]) == 6:
											t_source = "ywb"
											name_source = '英威诺'
										elif int(pat[i]) == 7:
											t_source = "sgjk"
											name_source = '搜狗'
										else:
											t_source = int(pat[i])
											name_source = t_source

									elif i == 1:
										if pat[i] == '':
											raise Exception('请输入提问类型')
										else:
											t_q_type = int(pat[i])
											if t_q_type == 1:
												name_type = '免费'
											elif t_q_type == 2:
												name_type = '悬赏'
											elif t_q_type == 3:
												name_type = '指定'
											else:
												raise Exception('提问类型错误')
									elif i == 2:
										if pat[i] == '':
											pass
										else:
											t_pay_amount = int(pat[i])
									elif i == 3:
										if pat[i] == '':
											pass
										else:
											t_pay_type = int(pat[i])	
									elif i == 4:
										if pat[i] == '':
											pass
										else:
											t_times = int(pat[i])
									elif i == 5:
										if pat[i] == '':
											pass
										else:
											t_firset_dep = pat[i]
									elif i == 6:
										if pat[i] == '':
											pass
										else:
											t_second_dep = pat[i]
									elif i == 7:
										if pat[i] == '':
											pass
										else:
											t_is_summary = int(pat[i])
									elif i == 8:
										if pat[i] == '':
											pass
										else:
											t_did = int(pat[i])
									elif i == 9:
										t_content = pat[i]
									else:
										break
								test_auto = Im_Test(did=t_did, times=t_times)
								if t_q_type == 2:
									t_did = ''
								#兼容其它来源提问，需根据提问方式修改did是否为空
								qid = test_auto.run_test(source=t_source,q_type=t_q_type,pay_amount=t_pay_amount,pay_type=t_pay_type,times=t_times,firset_dep=t_firset_dep,second_dep=t_second_dep,is_summary=t_is_summary,user_id=t_user_id,content=t_content, doc_id=t_did)
							except Exception as e:
								print(e)
								print("-------------------------本条用例未通过-------------------------")
								wrt.conclude(row,name_source,name_type,0,result=e)
							else:
								wrt.conclude(row,name_source,name_type,qid)
					except Exception as e:
						print('请检查当前目录下存在data.xls文件，并关闭data.xls')
						sleep(2)
						sys.exit()
					else:
						break

				else:
					print('感谢使用')
					sleep(1)
					sys.exit()