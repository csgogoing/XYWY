#coding=utf-8
from login import Login
import time
import requests
import re
import sys
import json
import datetime
from time import sleep
from urllib import request,parse
from lxml import etree

class Statistics_Jsdh():
	'''
	jsdh统计类
	'''
	def __init__(self, wb, date_time, jsdh_req):
		# , wb, row, jsdh_req
		self.jsdh_req = jsdh_req
		self.wb = wb
		self.cur = date_time
		#self.cur = datetime.datetime.now()
		self.pass_day = self.cur.timetuple().tm_yday
		#由于医患群excel页面结构，需要行数-1
		self.row = int(4+(self.cur.month+2)/3+self.cur.month+self.pass_day-1)
		print(self.row)
		self.headers={
		"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
		}


	def jsdh_get_num(self, sheet, column, params):
		while True:
			req = self.jsdh_req.get(self.jsdh_url, params=params, headers=self.headers)
			if req.status_code==200:
				break
			else:
				sleep(2)
		# self.ws = self.wb.get_sheet(sheet)
		# q_num = re.findall(r'共<b>(.*)</b>条数据.</div>', req.text)
		# if q_num==[]:
		# 	self.ws.write(self.row, column, 0)
		# else:
		# 	self.ws.write(self.row, column, q_num[0])

		self.wb.Worksheets[sheet].Activate()
		q_num = re.findall(r'共<b>(.*)</b>条数据.</div>', req.text)
		if q_num==[]:
			#print(00)
			self.wb.ActiveSheet.Cells(self.row, column+1).Value='0'
		else:
			#print(q_num[0])
			self.wb.ActiveSheet.Cells(self.row, column+1).Value=q_num[0]

	def jsdh_get_num_pay(self, sheet, column, params):
		while True:
			req = self.jsdh_req.get(self.jsdh_url, params=params, headers=self.headers)
			if req.status_code==200:
				break
			else:
				sleep(2)
		# self.ws = self.wb.get_sheet(sheet)
		# q_num = re.findall(r'共<b>(.*)</b>条数据.</div>', req.text)
		# if q_num==[]:
		# 	self.ws.write(self.row, column, 0)
		# else:
		# 	self.ws.write(self.row, column, q_num[0])

		self.wb.Worksheets[sheet].Activate()
		q_num = re.findall(r'共<b>(.*)</b>条数据.</div>', req.text)
		if q_num==[]:
			#print(00)
			self.wb.ActiveSheet.Cells(self.row, column+1).Value='0'
			self.wb.ActiveSheet.Cells(self.row, column+4).Value='0'
		else:
			#print(q_num[0])
			self.wb.ActiveSheet.Cells(self.row, column+1).Value=q_num[0]
			self.wb.ActiveSheet.Cells(self.row, column+4).Value=int(q_num[0])*29

	def jsdh_get_data(self):
		# if not self.jsdh_login():
		# 	print('极速电话登陆失败')
		# 	return
		self.jsdh_url = "http://admin.jisudianhua.xywy.com/question/default/index"

		#送心意
		jsdh_all = {
			'QuestionOrderSearch[bdate]':'%s-%s-%s'%(self.cur.year,self.cur.month,self.cur.day),
			'QuestionOrderSearch[edate]':'%s-%s-%s'%(self.cur.year,self.cur.month,self.cur.day)
			}
		jsdh_paid = {
			'QuestionOrderSearch[bdate]':'%s-%s-%s'%(self.cur.year,self.cur.month,self.cur.day),
			'QuestionOrderSearch[edate]':'%s-%s-%s'%(self.cur.year,self.cur.month,self.cur.day),
			'QuestionOrderSearch[status]':'10'
			}
		jsdh_unpaid = {
			'QuestionOrderSearch[id]':'',
			'QuestionOrderSearch[order_id]':'',
			'QuestionOrderSearch[status]':'2',
			'QuestionOrderSearch[patient_phone]':'',
			'QuestionOrderSearch[depa_pid]':'',
			'QuestionOrderSearch[did]':'',
			'QuestionOrderSearch[doctor_phone]':'',
			'QuestionOrderSearch[source]':'',
			'QuestionOrderSearch[bdate]':'%s-%s-%s'%(self.cur.year,self.cur.month,self.cur.day),
			'QuestionOrderSearch[edate]':'%s-%s-%s'%(self.cur.year,self.cur.month,self.cur.day)
			}
		# try:
		# 	self.jsdh_get_num(0, 64, jsdh_all)
		# 	self.jsdh_get_num(0, 66, jsdh_unpaid)
		# 	#pay需要顺便计算总金额
		# 	self.jsdh_get_num_pay(0, 65, jsdh_paid)

		# except Exception as e:
		# 	print(e)
		# 	print('极速电话统计失败')
		# else:
		# 	print('极速电话统计完成')
		
		self.jsdh_get_num(0, 64, jsdh_all)
		self.jsdh_get_num(0, 66, jsdh_unpaid)
		#pay需要顺便计算总金额
		self.jsdh_get_num_pay(0, 65, jsdh_paid)
		print('极速电话统计完成')


if __name__ == '__main__':
	#测试运行
	A = Statistics_Jsdh()
	A.jsdh_get_data()
