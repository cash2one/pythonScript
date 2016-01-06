#!/usr/bin/python3
#coding:utf-8

import urllib.request
import config
import pymysql
import json
import time

CONFIG1 = config.CONFIG1
biaotou = config.biaotou

conn = pymysql.connect(**CONFIG1)
cur = conn.cursor()
cur.execute("select id,ip from "+biaotou+"click_log where `addr` is null order by id desc");
result = cur.fetchall()
list_re = list(result)
for i in list_re:
	re = urllib.request.urlopen("http://apistore.baidu.com/microservice/iplookup?ip="+str(i[1]))
	re_data = re.read().decode('utf-8');
	try:
		json_re = json.loads(re_data)
		country = json_re['retData']['country']
		province = json_re['retData']['province']
		city = json_re['retData']['city']
		district =  json_re['retData']['district']
		addr = country + "-" + province + "-" + city + "-" + district + "("+json_re['retData']['carrier'] + ")"
		cur.execute("update `"+biaotou+"click_log` set addr = '"+addr+"' where id = "+str(i[0]));
		print('success:'+str(i[0]))
	except:
		cur.execute("update `"+biaotou+"click_log` set addr = 'error' where id = "+str(i[0]));
		print('error:'+str(i[0]))
	finally:
		time.sleep(1)
