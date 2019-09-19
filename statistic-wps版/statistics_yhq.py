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

class Statistics_Yhq():
	'''
	'''
	def __init__(self, wb, date_time, yhq_req):
		# , wb, row, yhq_req
		self.yhq_req = yhq_req
		self.wb = wb
		self.cur = date_time
		#self.cur = datetime.datetime.now()
		self.pass_day = self.cur.timetuple().tm_yday
		#由于医患群excel页面结构，需要行数-1
		self.row = int(4+(self.cur.month+2)/3+self.cur.month+self.pass_day-1)
		self.headers={
		"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0"
		}



	def yhq_get_num(self, sheet, column, params):
		while True:
			req = self.yhq_req.get(self.yhq_url, params=params, headers=self.headers)
			if req.status_code==200:
				break
			else:
				sleep(2)
		self.wb.Worksheets[sheet].Activate()

		q_num = re.findall(r'总订单：(.*)笔', req.text)[0]
		q_amount = re.findall(r'总金额：(.*)元', req.text)[0]
		self.wb.ActiveSheet.Cells(self.row, column+1).Value=q_num
		self.wb.ActiveSheet.Cells(self.row, column+2).Value=q_amount



	def yhq_get_data(self):
		# if not self.yhq_login():
		# 	print('有问必答登陆失败')
		# 	return
		self.yhq_url = 'http://yhqadmin.xywy.com/index.php'

		yhq_param = {
			'r':'order/index',
			'Order[doctor_id]':'',
			'Order[doctor_name]':'',
			'Order[user_id]':'',
			'Order[nickname]':'',
			'Order[order_num]':'',
			'Order[pay_num]':'',
			'Order[state]':'1',
			'Order[order_type]':'',
			'Order[is_zhzhen]':'',
			'Order[list]':'1',
			'Order[start]':'{}-{:0=2}-{:0=2}'.format(self.cur.year,self.cur.month,self.cur.day),
			'Order[end]':'{}-{:0=2}-{:0=2}'.format(self.cur.year,self.cur.month,self.cur.day),
			'Order[tag]':''
			}
		# try:
		# 	self.yhq_get_num(0, 61, params=yhq_param)
		# except Exception as e:
		# 	print(e)
		# 	print('医患群统计失败')
		# else:
		# 	print('医患群统计完成')
		self.yhq_get_num(0, 61, params=yhq_param)
		print('医患群统计完成')


if __name__ == '__main__':
	#测试运行
	A = Statistics_Yhq()
	A.yhq_get_data()
	#A.yhq_get_data()
