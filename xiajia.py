#! /usr/bin/python3
#coding:utf-8


import config
import pymysql
import time

CONFIG1 = config.CONFIG1
biaotou = config.biaotou

conn = pymysql.connect(**CONFIG1)
cur = conn.cursor()
cur.execute("select id,starttime,addtime from "+biaotou+"goods where xiajia = 0")
result = cur.fetchall()
result_list = list(result)
ti  = int(time.time()) - 86400*7
print(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(ti)))
for i in result_list:
	if ti > i[1]:
		#此处更新数据库修改该产品为下架状态
		cur.execute("update "+biaotou+"goods set xiajia = 1 where id = "+str(i[0]))
		print(str(i[0]))
cur.close()
