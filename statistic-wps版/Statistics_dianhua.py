#coding=utf-8
from login import Login
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

class Statistics_Dianhua():
	'''
	'''
	def __init__(self, wb, date_time, dianhua_req):
		# , wb, row, dianhua_req
		self.dianhua_req = dianhua_req
		self.wb = wb
		self.cur = date_time
		# self.cur = datetime.datetime.now()
		self.pass_day = self.cur.timetuple().tm_yday
		self.row = int(4+(self.cur.month+2)/3+self.cur.month+self.pass_day)
		self.headers={
		"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0"
		}


	def dianhua_get_num(self, sheet, column, params):
		while True:
			req = self.dianhua_req.get(self.dianhua_url, params=params, headers=self.headers)
			if req.status_code==200:
				break
			else:
				sleep(2)		
		req_text = req.content.decode('gb2312', errors='ignore')
		total_num = re.findall(r'总计: (.*)条', req_text)
		pay_num = re.findall(r'已付款订单量：(\d*) &nbsp', req_text)
		pay_amount = re.findall(r'已付款总金额：(\d+\.\d+)', req_text)

		# self.ws = self.wb.get_sheet(sheet)
		# if total_num==[]:
		# 	#print('空')
		# 	self.ws.write(self.row, column, 0)
		# else:
		# 	#print(total_num[0])
		# 	self.ws.write(self.row, column, total_num[0])

		# if pay_num==[]:
		# 	#print('空')
		# 	self.ws.write(self.row, column+1, 0)
		# else:
		# 	#print(total_num[0])
		# 	self.ws.write(self.row, column+1, pay_num[0])

		# if pay_amount==[]:
		# 	#print('空')
		# 	self.ws.write(self.row, column+3, 0)
		# else:
		# 	#print(pay_amount[0])
		# 	self.ws.write(self.row, column+3, pay_amount[0])

		self.wb.Worksheets[sheet].Activate()
		if total_num==[]:
			#print('空')
			self.wb.ActiveSheet.Cells(self.row, column+1).Value='0'
		else:
			#print(total_num[0])
			self.wb.ActiveSheet.Cells(self.row, column+1).Value=total_num[0]

		if pay_num==[]:
			#print('空')
			self.wb.ActiveSheet.Cells(self.row, column+2).Value='0'
		else:
			#print(total_num[0])
			self.wb.ActiveSheet.Cells(self.row, column+2).Value=pay_num[0]

		if pay_amount==[]:
			#print('空')
			self.wb.ActiveSheet.Cells(self.row, column+4).Value='0'
		else:
			#print(pay_amount[0])
			self.wb.ActiveSheet.Cells(self.row, column+4).Value=pay_amount[0]

	def dianhua_get_data(self):
		#获取数据
		# if not self.dianhua_login():
		# 	print('电话医生登陆失败')
		# 	return

		self.dianhua_url = 'http://dhys.z.xywy.com/order.php'

		dianhua_3g = {
			'type':'order_list',
			'hidden_test':'1',
			'state':'0',	
			'pay_state':'0',
			'call_start':'',
			'call_end': '',
			'expert_name':'',
			'operator_id':'0',
			'created_at_start':'%s-%s-%s'%(self.cur.year,self.cur.month,self.cur.day),
			'created_at_end':'%s-%s-%s'%(self.cur.year,self.cur.month,self.cur.day),
			'done_at_start':'',
			'done_at_end':'',
			'search': '1',
			'trade_type':'0',
			'is_balance':'0',
			'order_type': '0',
			'balance_start':'',
			'balance_end':'',
			'order_num': '',
			'is_dhysfz':'全部'.encode('gb2312'),
			'source':'3g',
			'platform_source_pay':'0',
			'hidden_test_check': 'on',	
			'search':'搜  索'.encode('gb2312')
			}

		dianhua_xywyapp = {
			'type':'order_list',
			'hidden_test':'1',
			'state':'0',	
			'pay_state':'0',
			'call_start':'',
			'call_end': '',
			'expert_name':'',
			'operator_id':'0',
			'created_at_start':'%s-%s-%s'%(self.cur.year,self.cur.month,self.cur.day),
			'created_at_end':'%s-%s-%s'%(self.cur.year,self.cur.month,self.cur.day),
			'done_at_start':'',
			'done_at_end':'',
			'search': '1',
			'trade_type':'0',
			'is_balance':'0',
			'order_type': '0',
			'balance_start':'',
			'balance_end':'',
			'order_num': '',
			'is_dhysfz':'全部'.encode('gb2312'),
			'source':'xywy_app_all',
			'platform_source_pay':'0',
			'hidden_test_check': 'on',	
			'search':'搜  索'.encode('gb2312')
			}

		dianhua_askapp = {
			'type':'order_list',
			'hidden_test':'1',
			'state':'0',	
			'pay_state':'0',
			'call_start':'',
			'call_end': '',
			'expert_name':'',
			'operator_id':'0',
			'created_at_start':'%s-%s-%s'%(self.cur.year,self.cur.month,self.cur.day),
			'created_at_end':'%s-%s-%s'%(self.cur.year,self.cur.month,self.cur.day),
			'done_at_start':'',
			'done_at_end':'',
			'search': '1',
			'trade_type':'0',
			'is_balance':'0',
			'order_type': '0',
			'balance_start':'',
			'balance_end':'',
			'order_num': '',
			'is_dhysfz':'全部'.encode('gb2312'),
			'source':'wys_app',
			'platform_source_pay':'0',
			'hidden_test_check': 'on',	
			'search':'搜  索'.encode('gb2312')
			}

		dianhua_wx = {
			'type':'order_list',
			'hidden_test':'1',
			'state':'0',	
			'pay_state':'0',
			'call_start':'',
			'call_end': '',
			'expert_name':'',
			'operator_id':'0',
			'created_at_start':'%s-%s-%s'%(self.cur.year,self.cur.month,self.cur.day),
			'created_at_end':'%s-%s-%s'%(self.cur.year,self.cur.month,self.cur.day),
			'done_at_start':'',
			'done_at_end':'',
			'search': '1',
			'trade_type':'0',
			'is_balance':'0',
			'order_type': '0',
			'balance_start':'',
			'balance_end':'',
			'order_num': '',
			'is_dhysfz':'全部'.encode('gb2312'),
			'source':'wechat',
			'platform_source_pay':'0',
			'hidden_test_check': 'on',	
			'search':'搜  索'.encode('gb2312')
			}

		dianhua_baidu_xzh = {
			'type':'order_list',
			'hidden_test':'1',
			'state':'0',	
			'pay_state':'0',
			'call_start':'',
			'call_end': '',
			'expert_name':'',
			'operator_id':'0',
			'created_at_start':'%s-%s-%s'%(self.cur.year,self.cur.month,self.cur.day),
			'created_at_end':'%s-%s-%s'%(self.cur.year,self.cur.month,self.cur.day),
			'done_at_start':'',
			'done_at_end':'',
			'search': '1',
			'trade_type':'0',
			'is_balance':'0',
			'order_type': '0',
			'balance_start':'',
			'balance_end':'',
			'order_num': '',
			'is_dhysfz':'全部'.encode('gb2312'),
			'source':'baidumip',
			'platform_source_pay':'0',
			'hidden_test_check': 'on',	
			'search':'搜  索'.encode('gb2312')
			}

		dianhua_sougou = {
			'type':'order_list',
			'hidden_test':'1',
			'state':'0',	
			'pay_state':'0',
			'call_start':'',
			'call_end': '',
			'expert_name':'',
			'operator_id':'0',
			'created_at_start':'%s-%s-%s'%(self.cur.year,self.cur.month,self.cur.day),
			'created_at_end':'%s-%s-%s'%(self.cur.year,self.cur.month,self.cur.day),
			'done_at_start':'',
			'done_at_end':'',
			'search': '1',
			'trade_type':'0',
			'is_balance':'0',
			'order_type': '0',
			'balance_start':'',
			'balance_end':'',
			'order_num': '',
			'is_dhysfz':'全部'.encode('gb2312'),
			'source':'sougou',
			'platform_source_pay':'0',
			'hidden_test_check': 'on',	
			'search':'搜  索'.encode('gb2312')
			}

		dianhua_pc = {
			'type':'order_list',
			'hidden_test':'1',
			'state':'0',	
			'pay_state':'0',
			'call_start':'',
			'call_end': '',
			'expert_name':'',
			'operator_id':'0',
			'created_at_start':'%s-%s-%s'%(self.cur.year,self.cur.month,self.cur.day),
			'created_at_end':'%s-%s-%s'%(self.cur.year,self.cur.month,self.cur.day),
			'done_at_start':'',
			'done_at_end':'',
			'search': '1',
			'trade_type':'0',
			'is_balance':'0',
			'order_type': '0',
			'balance_start':'',
			'balance_end':'',
			'order_num': '',
			'is_dhysfz':'全部'.encode('gb2312'),
			'source':'pc',
			'platform_source_pay':'0',
			'hidden_test_check': 'on',	
			'search':'搜  索'.encode('gb2312')
			}

		dianhua_jrtt = {
			'type':'order_list',
			'hidden_test':'1',
			'state':'0',	
			'pay_state':'0',
			'call_start':'',
			'call_end': '',
			'expert_name':'',
			'operator_id':'0',
			'created_at_start':'%s-%s-%s'%(self.cur.year,self.cur.month,self.cur.day),
			'created_at_end':'%s-%s-%s'%(self.cur.year,self.cur.month,self.cur.day),
			'done_at_start':'',
			'done_at_end':'',
			'search': '1',
			'trade_type':'0',
			'is_balance':'0',
			'order_type': '0',
			'balance_start':'',
			'balance_end':'',
			'order_num': '',
			'is_dhysfz':'全部'.encode('gb2312'),
			'source':'jinritoutiao',
			'platform_source_pay':'0',
			'hidden_test_check': 'on',	
			'search':'搜  索'.encode('gb2312')
			}

		self.dianhua_get_num(6, 17, params=dianhua_3g)
		self.dianhua_get_num(6, 25, params=dianhua_xywyapp)
		self.dianhua_get_num(6, 33, params=dianhua_askapp)
		self.dianhua_get_num(6, 41, params=dianhua_wx)
		self.dianhua_get_num(6, 49, params=dianhua_baidu_xzh)
		self.dianhua_get_num(6, 57, params=dianhua_sougou)
		self.dianhua_get_num(6, 65, params=dianhua_pc)
		self.dianhua_get_num(6, 73, params=dianhua_jrtt)
		print('电话医生统计完成')


if __name__ == '__main__':
	#测试运行
	A = Statistics_Dianhua()
	A.dianhua_login()
	#A.test()
	#A.get_data()
