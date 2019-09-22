import xlrd
from xlutils.copy import copy

class write_result():
	def __init__(self, file):
		rb = xlrd.open_workbook(file, formatting_info=True)
		self.wb = copy(rb)
		self.ws = self.wb.get_sheet(0)
		self.ws.write(0, 10, '问题ID')
		self.ws.write(0, 11, '执行结果')
		self.wb.save('result.xls')

	def conclude(self, row, name_source, name_type, qid, result='流程正常结束'):
		self.ws.write(row, 0, '%s'%name_source)
		self.ws.write(row, 1, '%s'%name_type)
		self.ws.write(row, 10, '%s'%qid)
		self.ws.write(row, 11, '%s'%result)
		self.wb.save('result.xls')
