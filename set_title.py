#!/usr/bin/python3
#coding:utf-8
#此脚本用于获取产品的标题信息

import config
import pymysql
import json
import urllib.request
import random
import time

CONFIG1 = config.CONFIG1
biaotou = config.biaotou
headers_dict = config.headers_dict

conn = pymysql.connect(**CONFIG1)
cur = conn.cursor()
cur.execute("select id,iid from `"+biaotou+"goods` where tao_title = '' order by id desc")
result = cur.fetchall()
result_list = list(result)
print(len(result_list))
for i in result_list:
	url = "http://hws.m.taobao.com/cache/wdetail/5.0/?id="+str(i[1])+"&callback=backToDetail&_="+str(random.uniform(1420000000000,1426247150913))
	req = urllib.request.Request(url,headers = headers_dict)
	result = urllib.request.urlopen(req)
	result_data = result.read().decode('utf-8').strip()
	#print(result_data[13:-1])
	try:
		result_json = json.loads(result_data[13:-1])
		cur.execute("update `"+biaotou+"goods` set tao_title = '"+result_json['data']['itemInfoModel']['title']+"' where id = "+str(i[0]));
		print('success:'+str(i[0]))
	except:
		print('fail:'+str(i[0]))
	finally:
		stime = random.uniform(1,8)
		time.sleep(stime)
cur.close()
