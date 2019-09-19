#coding=utf-8
from login import Login
from statistics_im import Statistics_Im
from statistics_tiezi import Statistics_Tiezi
from statistics_dianhua import Statistics_Dianhua
from statistics_jiating import Statistics_Jiating
from statistics_yuyue import Statistics_Yuyue
from statistics_yhq import Statistics_Yhq
from statistics_jsdh import Statistics_Jsdh
from xlutils.copy import copy
from time import sleep
import win32com.client
import re
import sys
import random
import os
import xlrd
import time
import datetime

class Write_Excel():
	#表格处理类
	def __init__(self):
		day = 7 #最多统计日期数
		cur = datetime.datetime.now()
		self.datetime_need=[]
		for i in range(day):
			cur = cur-datetime.timedelta(days=1)
			self.datetime_need.append(cur)
			excel_path = os.getcwd()+'\\%d年统计数据_基础服务&后台组-%d月%d日.xlsx'%(cur.year, cur.month, cur.day)
			if os.path.exists(excel_path):
				self.wpsApp = win32com.client.Dispatch("ket.Application")
				self.wpsApp.Visible = 0
				self.xlBook = self.wpsApp.Workbooks.Open(excel_path,ReadOnly=0, Editable=1)
				print('已找到%d年%d月%d日的统计表格'%(cur.year, cur.month, cur.day))
				break
			else:
				if i == day-1:
					sys.exit('当前目录下未找到前%s日内的统计表格'%day)
 
	def save(self):
		save_path = os.getcwd()+'\\%d年统计数据_基础服务&后台组-%d月%d日.xlsx'%(datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day)
		if os.path.exists(save_path):
			os.remove(save_path)
		self.xlBook.SaveAs(save_path)
		self.xlBook.Close()
		self.wpsApp.Quit()

	#根据所选日期进行统计
	def statistics(self):
		#所有平台登陆
		login = Login()
		#根据日期逐一统计
		for date_time in self.datetime_need:
			print('开始统计%s-%s-%s的数据'%(date_time.year,date_time.month,date_time.day))
			# 所有来源统计，可拓展
			Statistics_Jsdh(self.xlBook, date_time, login.jsdh_req).jsdh_get_data()
			Statistics_Yhq(self.xlBook, date_time, login.yhq_req).yhq_get_data()
			Statistics_Im(self.xlBook, date_time, login.im_req).im_get_data()
			Statistics_Tiezi(self.xlBook, date_time, login.tiezi_req).tiezi_get_data()
			Statistics_Dianhua(self.xlBook, date_time, login.dianhua_req).dianhua_get_data()
			Statistics_Jiating(self.xlBook, date_time, login.jiating_req).jiating_get_data()
			Statistics_Yuyue(self.xlBook, date_time, login.yuyue_req).yuyue_get_data()

			print('--------------------------------------------------------------')
		print('%d年-%d月-%d日自动化统计完成'%(datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day))

if __name__ == '__main__':
	we = Write_Excel()
	we.statistics()
	we.save()