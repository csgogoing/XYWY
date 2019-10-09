#coding=utf-8
import time
from selenium import webdriver

#launch
def browser():
	#使用Firefox()
	driver = webdriver.Firefox()
	return driver

if __name__ == '__main__':
	#测试SeleniumDriver可用
	dr = browser()
	dr.get("https://www.sohu.com/")
	time.sleep(5)
	dr.quit()
	

