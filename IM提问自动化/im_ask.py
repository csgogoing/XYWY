#coding=utf-8
import time
from time import sleep
from urllib import request,parse
import requests
import re


class Ask(object):
	'''
	qtype:1 免费，2悬赏，3指定
	'''
	def __init__(self):
		self.msg_id_origin = 1
		self.now_time = 0

	def get_id(self, user_id, zd=None, did=None):
		#获取加密参数与cookie
		url_login='http://test.admin.d.xywy.com/admin/user/login'
		#传入的user_id查找页
		url="http://test.admin.d.xywy.com/question/default/index?QuestionBaseSearch[keyword_type]=uid&QuestionBaseSearch[keyword]=%d"%user_id
		headers={
		"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
		}
		req=requests.get(url_login)
		m_value = re.findall(r'f" value="(.*)">', req.text)
		cookies=req.cookies.get_dict()
		#登录im后台
		data={
		'_csrf':m_value,
		'Login[username]':'admin',
		'Login[password]':'123456',
		'Login[verifyCode]':'testme'
		}
		#登陆IM后台获取Cookie
		req_login=requests.post(url_login,data=data,cookies=cookies)
		a_cookies=req_login.cookies.get_dict()
		#获取问题ID
		request_qid=requests.get(url,cookies=a_cookies)
		qids=re.findall(r'<td>(\d{5})</td>', request_qid.text)
		try:
			qid = int(qids[0])
		except:
			print('创建问题失败')
			return None
		#置问题状态
		if did:
			request.urlopen('http://test.admin.d.xywy.com/site/question-order-pay-status?qid=%d&zd=1&did=%d' %(qid,did))
		else:
			request.urlopen('http://test.admin.d.xywy.com/site/question-order-pay-status?qid=%d' %qid)

		return qid

	def persue(self, qid, resource_id, user_id):
		#追问接口
		headers = {
				'Connection': 'keep-alive',
				'Content-Type': 'application/x-www-form-urlencoded'
			}
		if resource_id == 200002:
			url = 'http://test.d.xywy.com/socket/ask'
			data = {
				'qid': qid,
				'resource_id': resource_id,
				'user_id': user_id,
				#'expert_id': '117333219',
				'content': '{"type":"text","text":"患者追问内容%d"}'%(self.msg_id_origin),
				'msg_id': '%s' %(int(time.time())),
				'atime': '%d' %(int(time.time())),
			}
		elif resource_id == 'sgjk':
			url = 'http://test.api.d.xywy.com/sogou/question/content-problem-create?safe_source_tag_wws=DJWE23_oresdf@ads'
			data = {
				'question_id': qid,
				'partner_key': 'xunyiwenyao',
				'source_key': 'sgjk',
				'user_id': user_id,
				#'expert_id': '117333219',
				'content': '[{"type":"text","text":"患者追问内容%d"}]'%(self.msg_id_origin),
				'msg_id': '%s' %(int(time.time())),
				'atime': '%d' %(int(time.time())),
			}
		else:
			url = 'http://test.api.d.xywy.com/user/question/add?safe_source_tag_wws=DJWE23_oresdf@ads'
			data = {
				'qid': qid,
				'source': resource_id,
				'uid': user_id,
				#'expert_id': '117333219',
				'content': '{"type":"text","text":"患者追问内容%d"}'%(self.msg_id_origin),
				'msg_id': '%s' %(int(time.time())),
				'atime': '%d' %(int(time.time())),
			}
		
		self.msg_id_origin = self.msg_id_origin + 1
		data = parse.urlencode(data).encode('utf-8')
		req = request.Request(url, headers=headers, data=data)
		try:
			page = request.urlopen(req).read()
			page = page.decode('utf-8')
		except:
			print('请检查环境绑定及网络连接')
			return(False)
		if 'Success!' in page:
			return(True)
		else:
			return(False)

	def baidu_page(self, q_type, user_id=456654, doctor_ids=117333219, pay_amount=300, firset_dep='内科', second_dep='呼吸内科', content=''):
		#百度来源提问—
		if q_type == 1:
			type_name = '免费'
		elif q_type == 2:
			type_name = '悬赏'
		elif q_type == 3:
			type_name = '指定'
		else:
			print('提问类型错误')
			return(False, None)
		url = 'http://test.d.xywy.com/socket/question'
		self.now_time = int(time.time())
		headers = {
			'Connection': 'keep-alive',
			'Content-Type': 'application/x-www-form-urlencoded'
		}
		if content == '':
			my_content = '自动化一级科室：%s，二级科室：%s，百度%s问题-%d' %(firset_dep, second_dep, type_name, self.msg_id_origin)
		else:
			my_content = content
		data = {
			'qid': '%d'%(self.now_time),
			'resource_id': 200002,
			'user_id': user_id,
			'patient_name': '汪测试',
			'patient_sex': 1,
			'patient_age': 20,
			'patient_age_month': 0,
			'patient_age_day': 0,
			'patient_phone': 17888888888,
			'content': my_content,
			'pic_urls': '',
			'q_type': q_type,
			'order_id': 'rtqa_%d' %(self.now_time),
			'doctor_ids': doctor_ids,
			'pay_type': 1,
			'pay_amount': pay_amount,
			'firset_dep': firset_dep,
			'second_dep': second_dep
		}
		self.msg_id_origin = self.msg_id_origin + 1
		if data['q_type'] == 3:
			del data['pay_amount']
			data['price'] = pay_amount
		data = parse.urlencode(data).encode('utf-8')
		req = request.Request(url, headers=headers, data=data)
		try:
			page = request.urlopen(req).read()
			page = page.decode('utf-8')
		except:
			print('请检查环境绑定及网络连接')
			return(False, None)
		if 'Success!' in page:
			print('百度问题提问成功')
			return(True, self.now_time)
		else:
			print('百度提问失败, 请重试或手动尝试')
			return(False, self.now_time)

	def other_page(self, resource_id, user_id=456654, q_type=2, pay_amount=300, doctor_ids='', pay_type=1, content=''):
		#其他来源提问
		url = 'http://test.api.d.xywy.com/user/question/ask?safe_source_tag_wws=DJWE23_oresdf@ads'
		self.now_time = int(time.time())
		headers = {
			'Connection': 'keep-alive',
			'Content-Type': 'application/x-www-form-urlencoded'
		}
		if content == '':
			my_content = '%s自动化感冒怎么办%d' %(resource_id, self.msg_id_origin)
		else:
			my_content = content
		data = {
			'qid': '%d'%(self.now_time),
			'source': resource_id,
			'uid': user_id,
			'patient_name': '张三',
			'patient_sex': 1,
			'patient_age': 20,
			'patient_age_month': 0,
			'patient_age_day': 0,
			'patient_phone': 17888888888,
			'content': my_content,
			'pic_urls': '',
			'q_type': q_type,
			'order_id': 'rtqa_%d' %(self.now_time),
			'doctor_ids': doctor_ids,
			'pay_type': 1,
			'pay_amount': pay_amount,
			'title': 'title',
			'intent': 'intent',
			'hospital': 0
		}
		data = parse.urlencode(data).encode('utf-8')
		req = request.Request(url, headers=headers, data=data)
		try:
			page = request.urlopen(req).read()
			page = page.decode('utf-8')
		except:
			print('请检查环境绑定及网络连接')
			return(False, None)
		if 'Success!' in page:
			print('%s来源问题提问成功'%resource_id)
			return(True, self.now_time)
		else:
			print('%s提问失败, 请重试或手动尝试'%resource_id)
			return(False, self.now_time)

	def sougou_page(self, q_type, user_id=456654, doctor_ids=117333219, pay_amount=300, content=''):
		#搜狗来源提问
		if q_type == 1:
			type_name = '免费'
			url = 'http://test.api.d.xywy.com/sogou/question/free-problem-create?safe_source_tag_wws=DJWE23_oresdf@ads'
		elif q_type == 2:
			type_name = '悬赏'
			url = 'http://test.api.d.xywy.com/sogou/question/paid-problem-create?safe_source_tag_wws=DJWE23_oresdf@ads' 
		elif q_type == 3:
			type_name = '指定'
			url = 'http://test.api.d.xywy.com/sogou/question/oriented-problem-create?safe_source_tag_wws=DJWE23_oresdf@ads'
		else:
			print('提问类型错误')
			return(False, None)
		self.now_time = int(time.time())
		headers = {
			'Connection': 'keep-alive',
			'Content-Type': 'application/x-www-form-urlencoded'
		}
		if content == '':
			my_content = '[{"type":"text","text":"自动化搜狗%s问题-%d"}]'%(type_name, self.msg_id_origin)
		else:
			my_content = '[{"type":"text","text":"%s"}]'%content
		data = {
			'question_id': '%d'%(self.now_time),
			'partner_key': 'xunyiwenyao',
			'source_key' : 'sgjk',
			'user_id' : user_id,
			'patient_name': '汪测试',
			'patient_sex': 1,
			'patient_age': 20,
			'content': my_content,
			'a_time': '%d' %(self.now_time),
			'order_id': 'rtqa_%d' %(self.now_time),
			'doctor_ids': doctor_ids,
			'pay_type': 1,
			'pay_amount': pay_amount
		}
		self.msg_id_origin = self.msg_id_origin + 1
		if q_type == 2:
			del data['doctor_ids']
		elif q_type == 3:
			del data['pay_type']
		else:			
			del data['order_id']
			del data['doctor_ids']
			del data['pay_type']
			del data['pay_amount']
		data = parse.urlencode(data).encode('utf-8')
		req = request.Request(url, headers=headers, data=data)
		try:
			page = request.urlopen(req).read()
			page = page.decode('utf-8')
		except:
			print('请检查环境绑定及网络连接')
			return(False, None)
		if 'Success!' in page:
			print('搜狗问题提问成功')
			return(True, self.now_time)
		else:
			print('搜狗提问失败, 请重试或手动尝试')
			return(False, self.now_time)

if __name__ == '__main__':
	#测试运行
	A = Ask()
	#A.baidu_page(2, user_id=456654)
	K = A.persue(14366, 'xywyapp', 456654)
	#print(K)
	#if 'Success!' in K:
	#	print(1)
	#A.other_page('xiaomi')