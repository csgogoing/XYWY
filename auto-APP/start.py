#coding=utf-8
import sys
import urllib
from Quick_ask import quick_ask
from Find_doctor import find_doctor
from doctor import Im_doctor
from im_id import Im_id

if __name__ == '__main__':
	print('正在努力连接手机...')
	while True:
		try:
			mtype = int(input('''请选择你要进行的操作：
		1：快速问诊
		2：找专家-预约挂号
		3：找专家-图文咨询
		4：挂号
		5：电话医生
		6：家庭医生
		Others：关闭
请选择：'''))
		except:
			sys.exit()
			break
		else:
			if mtype == 1:
				myphone = quick_ask()
				while True:
					try:
						choose = int(input('''请选择要创建的问题类型：
		1：妇产科医生指定问题
		2：3元悬赏问题
		3：5元悬赏问题
		4：10元悬赏问题
		5：免费问题
		Others：返回
请选择：'''))
					except:
						try:
							myphone.mquit()
						except urllib.error.URLError:
							print('请重启appium服务')
							break
						else:
							break
					else:
						try:
							if choose in range(1, 5):
								#app创建问题
								myphone.actions(choose)
								#将订单状态置为已支付
								m_id = Im_id('http://test.admin.d.xywy.com/question/default/index')
								m_id.Actions()
								#医生端登陆并回答问题
								print('启动医生端并答题')
								doctor = Im_doctor('http://test.dr.xywy.com/site/login')
								doctor.Actions(choose)
							elif choose == 5:
								#app创建问题
								myphone.actions(choose)
								#医生端登陆并回答问题
								doctor = Im_doctor('http://test.dr.xywy.com/site/login')
								doctor.Actions(choose)
							else:
								myphone.mquit()
								break
						except urllib.error.URLError:
							print('连接错误，请重启appium服务')
							break
						else:
							continue
			if mtype == 2:
				#myphone = find_doctor()
				#find_doctor.actions(2)
				print('working on')
			if mtype == 3:
				#myphone = find_doctor()
				#find_doctor.actions(3)
				print('working on')
			if mtype in range(4, 7):
				print('Next woking, please wait')
			else:
				sys.exit()
				break


