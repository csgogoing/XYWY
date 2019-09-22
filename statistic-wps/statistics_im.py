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

class Statistics_Im():
	'''
	IM统计类
	'''
	def __init__(self, wb, date_time, im_req):
		# , wb, row, im_req
		self.im_req = im_req
		self.wb = wb
		self.cur = date_time
		#self.cur = datetime.datetime.now()
		self.pass_day = self.cur.timetuple().tm_yday
		self.row = int(4+(self.cur.month+2)/3+self.cur.month+self.pass_day)
		self.headers={
		"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
		}



	def im_get_num_unpaid(self, sheet, column, params):
		while True:
			req = self.im_req.get(self.im_url, params=params, headers=self.headers)
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
			self.wb.ActiveSheet.Cells(self.row, column+1).Value='0'
		else:
			self.wb.ActiveSheet.Cells(self.row, column+1).Value=q_num[0]

	def im_get_num_paid(self, sheet, column, params):
		while True:
			req = self.im_req.get(self.im_url, params=params, headers=self.headers)
			if req.status_code==200:
				break
			else:
				sleep(2)
		shifu = re.findall(r'实付金额：(.*)元</span>', req.text)[0]
		q_num = re.findall(r'共<b>(.*)</b>条数据.</div>', req.text)

		# self.ws = self.wb.get_sheet(sheet)
		# self.ws.write(self.row, column+3, shifu)
		# if q_num==[]:
		# 	self.ws.write(self.row, column+1, 0)
		# else:
		# 	self.ws.write(self.row, column+1, q_num[0])

		self.wb.Worksheets[sheet].Activate()
		self.wb.ActiveSheet.Cells(self.row, column+4).Value=shifu
		if q_num==[]:
			self.wb.ActiveSheet.Cells(self.row, column+2).Value='0'
		else:
			self.wb.ActiveSheet.Cells(self.row, column+2).Value=q_num[0]

	def im_get_num_paid_l(self, sheet, column, params):
		while True:
			req = self.im_req.get(self.im_url, params=params, headers=self.headers)
			if req.status_code==200:
				break
			else:
				sleep(2)
		shifu = re.findall(r'实付金额：(.*)元</span>', req.text)[0]
		q_num = re.findall(r'共<b>(.*)</b>条数据.</div>', req.text)

		# self.ws = self.wb.get_sheet(sheet)
		# self.ws.write(self.row, column+2, shifu)
		# if q_num==[]:
		# 	self.ws.write(self.row, column+1, 0)
		# else:
		# 	self.ws.write(self.row, column+1, q_num[0])

		self.wb.Worksheets[sheet].Activate()
		self.wb.ActiveSheet.Cells(self.row, column+3).Value=shifu
		if q_num==[]:
			self.wb.ActiveSheet.Cells(self.row, column+2).Value='0'
		else:
			self.wb.ActiveSheet.Cells(self.row, column+2).Value=q_num[0]

	def im_get_num_tip(self, sheet, column, params):
		#送心意写入行由于业务流水页面不同，需要-1
		while True:
			req = self.im_req.get(self.tip_url, params=params, headers=self.headers)
			if req.status_code==200:
				break
			else:
				sleep(2)
		shifu = re.findall(r'送心意金额：(.*)元', req.text)[0]
		q_num = re.findall(r'共<b>(.*)</b>条数据.</div>', req.text)

		# self.ws = self.wb.get_sheet(sheet)
		# self.ws.write(self.row, column+2, shifu)
		# if q_num==[]:
		# 	self.ws.write(self.row, column+1, 0)
		# else:
		# 	self.ws.write(self.row, column+1, q_num[0])

		self.wb.Worksheets[sheet].Activate()
		self.wb.ActiveSheet.Cells(self.row-1, column+2).Value=shifu
		if q_num==[]:
			self.wb.ActiveSheet.Cells(self.row-1, column+1).Value='0'
		else:
			self.wb.ActiveSheet.Cells(self.row-1, column+1).Value=q_num[0]

	def im_get_data(self):
		# if not self.im_login():
		# 	print('IM登陆失败')
		# 	return

		self.im_url = "http://admin.d.xywy.com/order/question/index"
		self.tip_url = 'http://admin.d.xywy.com/order/reward/index'
		#免费
		#百度
		reward_baidu_unpaid = {
			'QuestionOrderSearch[order_type]':'1',
			'QuestionOrderSearch[pay_source]':'1',
			'QuestionOrderSearch[pay_status]':'',
			'QuestionOrderSearch[pay_type]':'',
			'QuestionOrderSearch[keyword_type]':'',
			'QuestionOrderSearch[keyword]':'',
			'QuestionOrderSearch[bgDate]':'%s-%s-%s'%(self.cur.year,self.cur.month,self.cur.day),
			'QuestionOrderSearch[edDate]':'%s-%s-%s'%(self.cur.year,self.cur.month,self.cur.day)
			}
		#寻医问药
		reward_xywyapp_unpaid = {
			'QuestionOrderSearch[order_type]':'1',
			'QuestionOrderSearch[pay_source]':'2',
			'QuestionOrderSearch[pay_status]':'',
			'QuestionOrderSearch[pay_type]':'',
			'QuestionOrderSearch[keyword_type]':'',
			'QuestionOrderSearch[keyword]':'',
			'QuestionOrderSearch[bgDate]':'%s-%s-%s'%(self.cur.year,self.cur.month,self.cur.day),
			'QuestionOrderSearch[edDate]':'%s-%s-%s'%(self.cur.year,self.cur.month,self.cur.day)
			}

		self.im_get_num_unpaid(1, 10, reward_baidu_unpaid)
		self.im_get_num_unpaid(1, 16, reward_xywyapp_unpaid)
		print('IM免费统计完成')

		#悬赏
		#寻医问药app
		reward_xywyapp_unpaid = {
			'QuestionOrderSearch[order_type]':'2',
			'QuestionOrderSearch[pay_source]':'2',
			'QuestionOrderSearch[pay_status]':'3',
			'QuestionOrderSearch[pay_type]':'',
			'QuestionOrderSearch[keyword_type]':'',
			'QuestionOrderSearch[keyword]':'',
			'QuestionOrderSearch[bgDate]':'%s-%s-%s'%(self.cur.year,self.cur.month,self.cur.day),
			'QuestionOrderSearch[edDate]':'%s-%s-%s'%(self.cur.year,self.cur.month,self.cur.day)
			}
		reward_xywyapp_paid = {
			'QuestionOrderSearch[order_type]':'2',
			'QuestionOrderSearch[pay_source]':'2',
			'QuestionOrderSearch[pay_status]':'2',
			'QuestionOrderSearch[pay_type]':'',
			'QuestionOrderSearch[keyword_type]':'',
			'QuestionOrderSearch[keyword]':'',
			'QuestionOrderSearch[bgDate]':'%s-%s-%s'%(self.cur.year,self.cur.month,self.cur.day),
			'QuestionOrderSearch[edDate]':'%s-%s-%s'%(self.cur.year,self.cur.month,self.cur.day)
			}
		#问医生app
		reward_askapp_unpaid = {
			'QuestionOrderSearch[order_type]':'2',
			'QuestionOrderSearch[pay_source]':'11',
			'QuestionOrderSearch[pay_status]':'3',
			'QuestionOrderSearch[pay_type]':'',
			'QuestionOrderSearch[keyword_type]':'',
			'QuestionOrderSearch[keyword]':'',
			'QuestionOrderSearch[bgDate]':'%s-%s-%s'%(self.cur.year,self.cur.month,self.cur.day),
			'QuestionOrderSearch[edDate]':'%s-%s-%s'%(self.cur.year,self.cur.month,self.cur.day)
			}
		reward_askapp_paid = {
			'QuestionOrderSearch[order_type]':'2',
			'QuestionOrderSearch[pay_source]':'11',
			'QuestionOrderSearch[pay_status]':'2',
			'QuestionOrderSearch[pay_type]':'',
			'QuestionOrderSearch[keyword_type]':'',
			'QuestionOrderSearch[keyword]':'',
			'QuestionOrderSearch[bgDate]':'%s-%s-%s'%(self.cur.year,self.cur.month,self.cur.day),
			'QuestionOrderSearch[edDate]':'%s-%s-%s'%(self.cur.year,self.cur.month,self.cur.day)
			}
		#百度熊掌号
		reward_baidu_xzh_unpaid = {
			'QuestionOrderSearch[order_type]':'2',
			'QuestionOrderSearch[pay_source]':'16',
			'QuestionOrderSearch[pay_status]':'3',
			'QuestionOrderSearch[pay_type]':'',
			'QuestionOrderSearch[keyword_type]':'',
			'QuestionOrderSearch[keyword]':'',
			'QuestionOrderSearch[bgDate]':'%s-%s-%s'%(self.cur.year,self.cur.month,self.cur.day),
			'QuestionOrderSearch[edDate]':'%s-%s-%s'%(self.cur.year,self.cur.month,self.cur.day)
			}
		reward_baidu_xzh_paid = {
			'QuestionOrderSearch[order_type]':'2',
			'QuestionOrderSearch[pay_source]':'16',
			'QuestionOrderSearch[pay_status]':'2',
			'QuestionOrderSearch[pay_type]':'',
			'QuestionOrderSearch[keyword_type]':'',
			'QuestionOrderSearch[keyword]':'',
			'QuestionOrderSearch[bgDate]':'%s-%s-%s'%(self.cur.year,self.cur.month,self.cur.day),
			'QuestionOrderSearch[edDate]':'%s-%s-%s'%(self.cur.year,self.cur.month,self.cur.day)
			}
		#百度小程序
		reward_bd_xcx_unpaid = {
			'QuestionOrderSearch[order_type]':'2',
			'QuestionOrderSearch[pay_source]':'31',
			'QuestionOrderSearch[pay_status]':'3',
			'QuestionOrderSearch[pay_type]':'',
			'QuestionOrderSearch[keyword_type]':'',
			'QuestionOrderSearch[keyword]':'',
			'QuestionOrderSearch[bgDate]':'%s-%s-%s'%(self.cur.year,self.cur.month,self.cur.day),
			'QuestionOrderSearch[edDate]':'%s-%s-%s'%(self.cur.year,self.cur.month,self.cur.day)
			}
		reward_bd_xcx_paid = {
			'QuestionOrderSearch[order_type]':'2',
			'QuestionOrderSearch[pay_source]':'31',
			'QuestionOrderSearch[pay_status]':'2',
			'QuestionOrderSearch[pay_type]':'',
			'QuestionOrderSearch[keyword_type]':'',
			'QuestionOrderSearch[keyword]':'',
			'QuestionOrderSearch[bgDate]':'%s-%s-%s'%(self.cur.year,self.cur.month,self.cur.day),
			'QuestionOrderSearch[edDate]':'%s-%s-%s'%(self.cur.year,self.cur.month,self.cur.day)
			}
		#头条小程序
		reward_toutiao_xcx_unpaid = {
			'QuestionOrderSearch[order_type]':'2',
			'QuestionOrderSearch[pay_source]':'29',
			'QuestionOrderSearch[pay_status]':'3',
			'QuestionOrderSearch[pay_type]':'',
			'QuestionOrderSearch[keyword_type]':'',
			'QuestionOrderSearch[keyword]':'',
			'QuestionOrderSearch[bgDate]':'%s-%s-%s'%(self.cur.year,self.cur.month,self.cur.day),
			'QuestionOrderSearch[edDate]':'%s-%s-%s'%(self.cur.year,self.cur.month,self.cur.day)
			}
		reward_toutiao_xcx_paid = {
			'QuestionOrderSearch[order_type]':'2',
			'QuestionOrderSearch[pay_source]':'29',
			'QuestionOrderSearch[pay_status]':'2',
			'QuestionOrderSearch[pay_type]':'',
			'QuestionOrderSearch[keyword_type]':'',
			'QuestionOrderSearch[keyword]':'',
			'QuestionOrderSearch[bgDate]':'%s-%s-%s'%(self.cur.year,self.cur.month,self.cur.day),
			'QuestionOrderSearch[edDate]':'%s-%s-%s'%(self.cur.year,self.cur.month,self.cur.day)
			}
		#wap
		reward_3g_unpaid = {
			'QuestionOrderSearch[order_type]':'2',
			'QuestionOrderSearch[pay_source]':'4',
			'QuestionOrderSearch[pay_status]':'3',
			'QuestionOrderSearch[pay_type]':'',
			'QuestionOrderSearch[keyword_type]':'',
			'QuestionOrderSearch[keyword]':'',
			'QuestionOrderSearch[bgDate]':'%s-%s-%s'%(self.cur.year,self.cur.month,self.cur.day),
			'QuestionOrderSearch[edDate]':'%s-%s-%s'%(self.cur.year,self.cur.month,self.cur.day)
			}
		reward_3g_paid = {
			'QuestionOrderSearch[order_type]':'2',
			'QuestionOrderSearch[pay_source]':'4',
			'QuestionOrderSearch[pay_status]':'2',
			'QuestionOrderSearch[pay_type]':'',
			'QuestionOrderSearch[keyword_type]':'',
			'QuestionOrderSearch[keyword]':'',
			'QuestionOrderSearch[bgDate]':'%s-%s-%s'%(self.cur.year,self.cur.month,self.cur.day),
			'QuestionOrderSearch[edDate]':'%s-%s-%s'%(self.cur.year,self.cur.month,self.cur.day)
			}
		#微信小程序
		reward_weixin_xcx_unpaid = {
			'QuestionOrderSearch[order_type]':'2',
			'QuestionOrderSearch[pay_source]':'25',
			'QuestionOrderSearch[pay_status]':'3',
			'QuestionOrderSearch[pay_type]':'',
			'QuestionOrderSearch[keyword_type]':'',
			'QuestionOrderSearch[keyword]':'',
			'QuestionOrderSearch[bgDate]':'%s-%s-%s'%(self.cur.year,self.cur.month,self.cur.day),
			'QuestionOrderSearch[edDate]':'%s-%s-%s'%(self.cur.year,self.cur.month,self.cur.day)
			}
		reward_weixin_xcx_paid = {
			'QuestionOrderSearch[order_type]':'2',
			'QuestionOrderSearch[pay_source]':'25',
			'QuestionOrderSearch[pay_status]':'2',
			'QuestionOrderSearch[pay_type]':'',
			'QuestionOrderSearch[keyword_type]':'',
			'QuestionOrderSearch[keyword]':'',
			'QuestionOrderSearch[bgDate]':'%s-%s-%s'%(self.cur.year,self.cur.month,self.cur.day),
			'QuestionOrderSearch[edDate]':'%s-%s-%s'%(self.cur.year,self.cur.month,self.cur.day)
			}
		#百度
		reward_baidu_unpaid = {
			'QuestionOrderSearch[order_type]':'2',
			'QuestionOrderSearch[pay_source]':'1',
			'QuestionOrderSearch[pay_status]':'3',
			'QuestionOrderSearch[pay_type]':'',
			'QuestionOrderSearch[keyword_type]':'',
			'QuestionOrderSearch[keyword]':'',
			'QuestionOrderSearch[bgDate]':'%s-%s-%s'%(self.cur.year,self.cur.month,self.cur.day),
			'QuestionOrderSearch[edDate]':'%s-%s-%s'%(self.cur.year,self.cur.month,self.cur.day)
			}
		reward_baidu_paid = {
			'QuestionOrderSearch[order_type]':'2',
			'QuestionOrderSearch[pay_source]':'1',
			'QuestionOrderSearch[pay_status]':'2',
			'QuestionOrderSearch[pay_type]':'',
			'QuestionOrderSearch[keyword_type]':'',
			'QuestionOrderSearch[keyword]':'',
			'QuestionOrderSearch[bgDate]':'%s-%s-%s'%(self.cur.year,self.cur.month,self.cur.day),
			'QuestionOrderSearch[edDate]':'%s-%s-%s'%(self.cur.year,self.cur.month,self.cur.day)
			}
		#华夏保险
		reward_hxbx_unpaid = {
			'QuestionOrderSearch[order_type]':'2',
			'QuestionOrderSearch[pay_source]':'19',
			'QuestionOrderSearch[pay_status]':'3',
			'QuestionOrderSearch[pay_type]':'',
			'QuestionOrderSearch[keyword_type]':'',
			'QuestionOrderSearch[keyword]':'',
			'QuestionOrderSearch[bgDate]':'%s-%s-%s'%(self.cur.year,self.cur.month,self.cur.day),
			'QuestionOrderSearch[edDate]':'%s-%s-%s'%(self.cur.year,self.cur.month,self.cur.day)
			}
		reward_hxbx_paid = {
			'QuestionOrderSearch[order_type]':'2',
			'QuestionOrderSearch[pay_source]':'19',
			'QuestionOrderSearch[pay_status]':'2',
			'QuestionOrderSearch[pay_type]':'',
			'QuestionOrderSearch[keyword_type]':'',
			'QuestionOrderSearch[keyword]':'',
			'QuestionOrderSearch[bgDate]':'%s-%s-%s'%(self.cur.year,self.cur.month,self.cur.day),
			'QuestionOrderSearch[edDate]':'%s-%s-%s'%(self.cur.year,self.cur.month,self.cur.day)
			}
		#搜狗
		reward_sougou_unpaid = {
			'QuestionOrderSearch[order_type]':'2',
			'QuestionOrderSearch[pay_source]':'26',
			'QuestionOrderSearch[pay_status]':'3',
			'QuestionOrderSearch[pay_type]':'',
			'QuestionOrderSearch[keyword_type]':'',
			'QuestionOrderSearch[keyword]':'',
			'QuestionOrderSearch[bgDate]':'%s-%s-%s'%(self.cur.year,self.cur.month,self.cur.day),
			'QuestionOrderSearch[edDate]':'%s-%s-%s'%(self.cur.year,self.cur.month,self.cur.day)
			}
		reward_sougou_paid = {
			'QuestionOrderSearch[order_type]':'2',
			'QuestionOrderSearch[pay_source]':'26',
			'QuestionOrderSearch[pay_status]':'2',
			'QuestionOrderSearch[pay_type]':'',
			'QuestionOrderSearch[keyword_type]':'',
			'QuestionOrderSearch[keyword]':'',
			'QuestionOrderSearch[bgDate]':'%s-%s-%s'%(self.cur.year,self.cur.month,self.cur.day),
			'QuestionOrderSearch[edDate]':'%s-%s-%s'%(self.cur.year,self.cur.month,self.cur.day)
			}
		#快应用
		reward_kuaiyingyong_unpaid = {
			'QuestionOrderSearch[order_type]':'2',
			'QuestionOrderSearch[pay_source]':'14',
			'QuestionOrderSearch[pay_status]':'3',
			'QuestionOrderSearch[pay_type]':'',
			'QuestionOrderSearch[keyword_type]':'',
			'QuestionOrderSearch[keyword]':'',
			'QuestionOrderSearch[bgDate]':'%s-%s-%s'%(self.cur.year,self.cur.month,self.cur.day),
			'QuestionOrderSearch[edDate]':'%s-%s-%s'%(self.cur.year,self.cur.month,self.cur.day)
			}
		reward_kuaiyingyong_paid = {
			'QuestionOrderSearch[order_type]':'2',
			'QuestionOrderSearch[pay_source]':'14',
			'QuestionOrderSearch[pay_status]':'2',
			'QuestionOrderSearch[pay_type]':'',
			'QuestionOrderSearch[keyword_type]':'',
			'QuestionOrderSearch[keyword]':'',
			'QuestionOrderSearch[bgDate]':'%s-%s-%s'%(self.cur.year,self.cur.month,self.cur.day),
			'QuestionOrderSearch[edDate]':'%s-%s-%s'%(self.cur.year,self.cur.month,self.cur.day)
			}
		
		self.im_get_num_unpaid(3, 13, reward_xywyapp_unpaid)
		self.im_get_num_paid(3, 13, reward_xywyapp_paid)

		self.im_get_num_unpaid(3, 19, reward_askapp_unpaid)
		self.im_get_num_paid(3, 19, reward_askapp_paid)

		self.im_get_num_unpaid(3, 25, reward_baidu_xzh_unpaid)
		self.im_get_num_paid(3, 25, reward_baidu_xzh_paid)

		self.im_get_num_unpaid(3, 31, reward_bd_xcx_unpaid)
		self.im_get_num_paid(3, 31, reward_bd_xcx_paid)

		self.im_get_num_unpaid(3, 37, reward_toutiao_xcx_unpaid)
		self.im_get_num_paid(3, 37, reward_toutiao_xcx_paid)

		self.im_get_num_unpaid(3, 43, reward_3g_unpaid)
		self.im_get_num_paid(3, 43, reward_3g_paid)

		self.im_get_num_unpaid(3, 49, reward_weixin_xcx_unpaid)
		self.im_get_num_paid(3, 49, reward_weixin_xcx_paid)

		self.im_get_num_unpaid(3, 55, reward_baidu_unpaid)
		self.im_get_num_paid_l(3, 55, reward_baidu_paid)

		self.im_get_num_unpaid(3, 60, reward_hxbx_unpaid)
		self.im_get_num_paid_l(3, 60, reward_hxbx_paid)

		self.im_get_num_unpaid(3, 65, reward_sougou_unpaid)
		self.im_get_num_paid_l(3, 65, reward_sougou_paid)

		self.im_get_num_unpaid(3, 70, reward_kuaiyingyong_unpaid)
		self.im_get_num_paid_l(3, 70, reward_kuaiyingyong_paid)

		print('IM悬赏统计完成')

		#指定
		#寻医问药app
		assign_xywyapp_unpaid = {
			'QuestionOrderSearch[order_type]':'3',
			'QuestionOrderSearch[pay_source]':'2',
			'QuestionOrderSearch[pay_status]':'3',
			'QuestionOrderSearch[pay_type]':'',
			'QuestionOrderSearch[keyword_type]':'',
			'QuestionOrderSearch[keyword]':'',
			'QuestionOrderSearch[bgDate]':'%s-%s-%s'%(self.cur.year,self.cur.month,self.cur.day),
			'QuestionOrderSearch[edDate]':'%s-%s-%s'%(self.cur.year,self.cur.month,self.cur.day)
			}
		assign_xywyapp_paid = {
			'QuestionOrderSearch[order_type]':'3',
			'QuestionOrderSearch[pay_source]':'2',
			'QuestionOrderSearch[pay_status]':'2',
			'QuestionOrderSearch[pay_type]':'',
			'QuestionOrderSearch[keyword_type]':'',
			'QuestionOrderSearch[keyword]':'',
			'QuestionOrderSearch[bgDate]':'%s-%s-%s'%(self.cur.year,self.cur.month,self.cur.day),
			'QuestionOrderSearch[edDate]':'%s-%s-%s'%(self.cur.year,self.cur.month,self.cur.day)
			}
		#问医生app
		assign_askapp_unpaid = {
			'QuestionOrderSearch[order_type]':'3',
			'QuestionOrderSearch[pay_source]':'11',
			'QuestionOrderSearch[pay_status]':'3',
			'QuestionOrderSearch[pay_type]':'',
			'QuestionOrderSearch[keyword_type]':'',
			'QuestionOrderSearch[keyword]':'',
			'QuestionOrderSearch[bgDate]':'%s-%s-%s'%(self.cur.year,self.cur.month,self.cur.day),
			'QuestionOrderSearch[edDate]':'%s-%s-%s'%(self.cur.year,self.cur.month,self.cur.day)
			}
		assign_askapp_paid = {
			'QuestionOrderSearch[order_type]':'3',
			'QuestionOrderSearch[pay_source]':'11',
			'QuestionOrderSearch[pay_status]':'2',
			'QuestionOrderSearch[pay_type]':'',
			'QuestionOrderSearch[keyword_type]':'',
			'QuestionOrderSearch[keyword]':'',
			'QuestionOrderSearch[bgDate]':'%s-%s-%s'%(self.cur.year,self.cur.month,self.cur.day),
			'QuestionOrderSearch[edDate]':'%s-%s-%s'%(self.cur.year,self.cur.month,self.cur.day)
			}
		#百度熊掌号
		assign_baidu_xzh_unpaid = {
			'QuestionOrderSearch[order_type]':'3',
			'QuestionOrderSearch[pay_source]':'16',
			'QuestionOrderSearch[pay_status]':'3',
			'QuestionOrderSearch[pay_type]':'',
			'QuestionOrderSearch[keyword_type]':'',
			'QuestionOrderSearch[keyword]':'',
			'QuestionOrderSearch[bgDate]':'%s-%s-%s'%(self.cur.year,self.cur.month,self.cur.day),
			'QuestionOrderSearch[edDate]':'%s-%s-%s'%(self.cur.year,self.cur.month,self.cur.day)
			}
		assign_baidu_xzh_paid = {
			'QuestionOrderSearch[order_type]':'3',
			'QuestionOrderSearch[pay_source]':'16',
			'QuestionOrderSearch[pay_status]':'2',
			'QuestionOrderSearch[pay_type]':'',
			'QuestionOrderSearch[keyword_type]':'',
			'QuestionOrderSearch[keyword]':'',
			'QuestionOrderSearch[bgDate]':'%s-%s-%s'%(self.cur.year,self.cur.month,self.cur.day),
			'QuestionOrderSearch[edDate]':'%s-%s-%s'%(self.cur.year,self.cur.month,self.cur.day)
			}
		#百度小程序
		assign_bd_xcx_unpaid = {
			'QuestionOrderSearch[order_type]':'3',
			'QuestionOrderSearch[pay_source]':'31',
			'QuestionOrderSearch[pay_status]':'3',
			'QuestionOrderSearch[pay_type]':'',
			'QuestionOrderSearch[keyword_type]':'',
			'QuestionOrderSearch[keyword]':'',
			'QuestionOrderSearch[bgDate]':'%s-%s-%s'%(self.cur.year,self.cur.month,self.cur.day),
			'QuestionOrderSearch[edDate]':'%s-%s-%s'%(self.cur.year,self.cur.month,self.cur.day)
			}
		assign_bd_xcx_paid = {	
			'QuestionOrderSearch[order_type]':'3',
			'QuestionOrderSearch[pay_source]':'31',
			'QuestionOrderSearch[pay_status]':'2',
			'QuestionOrderSearch[pay_type]':'',
			'QuestionOrderSearch[keyword_type]':'',
			'QuestionOrderSearch[keyword]':'',
			'QuestionOrderSearch[bgDate]':'%s-%s-%s'%(self.cur.year,self.cur.month,self.cur.day),
			'QuestionOrderSearch[edDate]':'%s-%s-%s'%(self.cur.year,self.cur.month,self.cur.day)
			}
		#微信小程序
		assign_weixin_xcx_unpaid = {
			'QuestionOrderSearch[order_type]':'3',
			'QuestionOrderSearch[pay_source]':'25',
			'QuestionOrderSearch[pay_status]':'3',
			'QuestionOrderSearch[pay_type]':'',
			'QuestionOrderSearch[keyword_type]':'',
			'QuestionOrderSearch[keyword]':'',
			'QuestionOrderSearch[bgDate]':'%s-%s-%s'%(self.cur.year,self.cur.month,self.cur.day),
			'QuestionOrderSearch[edDate]':'%s-%s-%s'%(self.cur.year,self.cur.month,self.cur.day)
			}
		assign_weixin_xcx_paid = {
			'QuestionOrderSearch[order_type]':'3',
			'QuestionOrderSearch[pay_source]':'25',
			'QuestionOrderSearch[pay_status]':'2',
			'QuestionOrderSearch[pay_type]':'',
			'QuestionOrderSearch[keyword_type]':'',
			'QuestionOrderSearch[keyword]':'',
			'QuestionOrderSearch[bgDate]':'%s-%s-%s'%(self.cur.year,self.cur.month,self.cur.day),
			'QuestionOrderSearch[edDate]':'%s-%s-%s'%(self.cur.year,self.cur.month,self.cur.day)
			}
		#头条小程序
		assign_toutiao_xcx_unpaid = {
			'QuestionOrderSearch[order_type]':'3',
			'QuestionOrderSearch[pay_source]':'29',
			'QuestionOrderSearch[pay_status]':'3',
			'QuestionOrderSearch[pay_type]':'',
			'QuestionOrderSearch[keyword_type]':'',
			'QuestionOrderSearch[keyword]':'',
			'QuestionOrderSearch[bgDate]':'%s-%s-%s'%(self.cur.year,self.cur.month,self.cur.day),
			'QuestionOrderSearch[edDate]':'%s-%s-%s'%(self.cur.year,self.cur.month,self.cur.day)
			}
		assign_toutiao_xcx_paid = {
			'QuestionOrderSearch[order_type]':'3',
			'QuestionOrderSearch[pay_source]':'29',
			'QuestionOrderSearch[pay_status]':'2',
			'QuestionOrderSearch[pay_type]':'',
			'QuestionOrderSearch[keyword_type]':'',
			'QuestionOrderSearch[keyword]':'',
			'QuestionOrderSearch[bgDate]':'%s-%s-%s'%(self.cur.year,self.cur.month,self.cur.day),
			'QuestionOrderSearch[edDate]':'%s-%s-%s'%(self.cur.year,self.cur.month,self.cur.day)
			}
		#熊掌号mip
		assign_baidu_mip_unpaid = {
			'QuestionOrderSearch[order_type]':'3',
			'QuestionOrderSearch[pay_source]':'23',
			'QuestionOrderSearch[pay_status]':'3',
			'QuestionOrderSearch[pay_type]':'',
			'QuestionOrderSearch[keyword_type]':'',
			'QuestionOrderSearch[keyword]':'',
			'QuestionOrderSearch[bgDate]':'%s-%s-%s'%(self.cur.year,self.cur.month,self.cur.day),
			'QuestionOrderSearch[edDate]':'%s-%s-%s'%(self.cur.year,self.cur.month,self.cur.day)
			}
		assign_baidu_mip_paid = {
			'QuestionOrderSearch[order_type]':'3',
			'QuestionOrderSearch[pay_source]':'23',
			'QuestionOrderSearch[pay_status]':'2',
			'QuestionOrderSearch[pay_type]':'',
			'QuestionOrderSearch[keyword_type]':'',
			'QuestionOrderSearch[keyword]':'',
			'QuestionOrderSearch[bgDate]':'%s-%s-%s'%(self.cur.year,self.cur.month,self.cur.day),
			'QuestionOrderSearch[edDate]':'%s-%s-%s'%(self.cur.year,self.cur.month,self.cur.day)
			}
		#3g
		assign_3g_unpaid = {
			'QuestionOrderSearch[order_type]':'3',
			'QuestionOrderSearch[pay_source]':'4',
			'QuestionOrderSearch[pay_status]':'3',
			'QuestionOrderSearch[pay_type]':'',
			'QuestionOrderSearch[keyword_type]':'',
			'QuestionOrderSearch[keyword]':'',
			'QuestionOrderSearch[bgDate]':'%s-%s-%s'%(self.cur.year,self.cur.month,self.cur.day),
			'QuestionOrderSearch[edDate]':'%s-%s-%s'%(self.cur.year,self.cur.month,self.cur.day)
			}
		assign_3g_paid = {
			'QuestionOrderSearch[order_type]':'3',
			'QuestionOrderSearch[pay_source]':'4',
			'QuestionOrderSearch[pay_status]':'2',
			'QuestionOrderSearch[pay_type]':'',
			'QuestionOrderSearch[keyword_type]':'',
			'QuestionOrderSearch[keyword]':'',
			'QuestionOrderSearch[bgDate]':'%s-%s-%s'%(self.cur.year,self.cur.month,self.cur.day),
			'QuestionOrderSearch[edDate]':'%s-%s-%s'%(self.cur.year,self.cur.month,self.cur.day)
			}
		#快应用
		assign_kuaiyingyong_unpaid = {
			'QuestionOrderSearch[order_type]':'3',
			'QuestionOrderSearch[pay_source]':'14',
			'QuestionOrderSearch[pay_status]':'3',
			'QuestionOrderSearch[pay_type]':'',
			'QuestionOrderSearch[keyword_type]':'',
			'QuestionOrderSearch[keyword]':'',
			'QuestionOrderSearch[bgDate]':'%s-%s-%s'%(self.cur.year,self.cur.month,self.cur.day),
			'QuestionOrderSearch[edDate]':'%s-%s-%s'%(self.cur.year,self.cur.month,self.cur.day)
			}
		assign_kuaiyingyong_paid = {
			'QuestionOrderSearch[order_type]':'3',
			'QuestionOrderSearch[pay_source]':'14',
			'QuestionOrderSearch[pay_status]':'2',
			'QuestionOrderSearch[pay_type]':'',
			'QuestionOrderSearch[keyword_type]':'',
			'QuestionOrderSearch[keyword]':'',
			'QuestionOrderSearch[bgDate]':'%s-%s-%s'%(self.cur.year,self.cur.month,self.cur.day),
			'QuestionOrderSearch[edDate]':'%s-%s-%s'%(self.cur.year,self.cur.month,self.cur.day)
			}
		#百度
		assign_baidu_unpaid = {
			'QuestionOrderSearch[order_type]':'3',
			'QuestionOrderSearch[pay_source]':'1',
			'QuestionOrderSearch[pay_status]':'3',
			'QuestionOrderSearch[pay_type]':'',
			'QuestionOrderSearch[keyword_type]':'',
			'QuestionOrderSearch[keyword]':'',
			'QuestionOrderSearch[bgDate]':'%s-%s-%s'%(self.cur.year,self.cur.month,self.cur.day),
			'QuestionOrderSearch[edDate]':'%s-%s-%s'%(self.cur.year,self.cur.month,self.cur.day)
			}
		assign_baidu_paid = {
			'QuestionOrderSearch[order_type]':'3',
			'QuestionOrderSearch[pay_source]':'1',
			'QuestionOrderSearch[pay_status]':'2',
			'QuestionOrderSearch[pay_type]':'',
			'QuestionOrderSearch[keyword_type]':'',
			'QuestionOrderSearch[keyword]':'',
			'QuestionOrderSearch[bgDate]':'%s-%s-%s'%(self.cur.year,self.cur.month,self.cur.day),
			'QuestionOrderSearch[edDate]':'%s-%s-%s'%(self.cur.year,self.cur.month,self.cur.day)
			}
		#搜狗
		assign_sougou_unpaid = {
			'QuestionOrderSearch[order_type]':'3',
			'QuestionOrderSearch[pay_source]':'26',
			'QuestionOrderSearch[pay_status]':'3',
			'QuestionOrderSearch[pay_type]':'',
			'QuestionOrderSearch[keyword_type]':'',
			'QuestionOrderSearch[keyword]':'',
			'QuestionOrderSearch[bgDate]':'%s-%s-%s'%(self.cur.year,self.cur.month,self.cur.day),
			'QuestionOrderSearch[edDate]':'%s-%s-%s'%(self.cur.year,self.cur.month,self.cur.day)
			}
		assign_sougou_paid = {
			'QuestionOrderSearch[order_type]':'3',
			'QuestionOrderSearch[pay_source]':'26',
			'QuestionOrderSearch[pay_status]':'2',
			'QuestionOrderSearch[pay_type]':'',
			'QuestionOrderSearch[keyword_type]':'',
			'QuestionOrderSearch[keyword]':'',
			'QuestionOrderSearch[bgDate]':'%s-%s-%s'%(self.cur.year,self.cur.month,self.cur.day),
			'QuestionOrderSearch[edDate]':'%s-%s-%s'%(self.cur.year,self.cur.month,self.cur.day)
			}

		self.im_get_num_unpaid(5, 13, assign_xywyapp_unpaid)
		self.im_get_num_paid(5, 13, assign_xywyapp_paid)

		self.im_get_num_unpaid(5, 19, assign_askapp_unpaid)
		self.im_get_num_paid(5, 19, assign_askapp_paid)

		self.im_get_num_unpaid(5, 25, assign_baidu_xzh_unpaid)
		self.im_get_num_paid(5, 25, assign_baidu_xzh_paid)

		self.im_get_num_unpaid(5, 31, assign_bd_xcx_unpaid)
		self.im_get_num_paid(5, 31, assign_bd_xcx_paid)

		self.im_get_num_unpaid(5, 37, assign_weixin_xcx_unpaid)
		self.im_get_num_paid(5, 37, assign_weixin_xcx_paid)

		self.im_get_num_unpaid(5, 43, assign_toutiao_xcx_unpaid)
		self.im_get_num_paid(5, 43, assign_toutiao_xcx_paid)

		self.im_get_num_unpaid(5, 49, assign_baidu_mip_unpaid)
		self.im_get_num_paid(5, 49, assign_baidu_mip_paid)

		self.im_get_num_unpaid(5, 55, assign_3g_unpaid)
		self.im_get_num_paid(5, 55, assign_3g_paid)

		self.im_get_num_unpaid(5, 61, assign_kuaiyingyong_unpaid)
		self.im_get_num_paid_l(5, 61, assign_kuaiyingyong_paid)

		self.im_get_num_unpaid(5, 66, assign_baidu_unpaid)
		self.im_get_num_paid_l(5, 66, assign_baidu_paid)

		self.im_get_num_unpaid(5, 71, assign_sougou_unpaid)
		self.im_get_num_paid_l(5, 71, assign_sougou_paid)

		print('IM指定统计完成')

		#送心意
		assign_tip = {
			'RewardOrderSearch[pay_source]':'',
			'RewardOrderSearch[pay_status]':'2',
			'RewardOrderSearch[pay_type]':'',
			'RewardOrderSearch[keyword_type]':'',
			'RewardOrderSearch[keyword]':'',
			'RewardOrderSearch[bgDate]':'%s-%s-%s'%(self.cur.year,self.cur.month,self.cur.day),
			'RewardOrderSearch[edDate]':'%s-%s-%s'%(self.cur.year,self.cur.month,self.cur.day)
			}
		
		self.im_get_num_tip(0, 58, assign_tip)
		print('IM送心意统计完成')


if __name__ == '__main__':
	#测试运行
	A = Statistics_Im()
	if not A.im_login():
		print('登陆失败')
	else:
		print('成功')
	#A.im_get_data()
