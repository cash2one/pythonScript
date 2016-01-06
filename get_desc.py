#!/usr/bin/python3
#coding:utf-8
#此脚本用于抓取产品详情以及更新产品信息
'''
from html.parser import HTMLParser
from html.entities import name2codepoint

class MyHTMLParser(HTMLParser):
	def __init__(self):
		HTMLParser.__init__(self)
		self.tagname = None
		self.data = ''
	def handle_starttag(self, tag, attrs):
		self.tagname = tag
	def handle_data(self, data):
		if self.tagname == 'txt':
			self.data += "<p><span span style=\"line-height:2;color:#666666;\">"+data+"</span></p>"
		elif self.tagname == 'img':
			self.data += "<p><img src=\""+data+"\"/></p>"
'''
import config

CONFIG1 = config.CONFIG1
biaotou = config.biaotou
headers_dict = config.headers_dict

#此函数用于抓取产品详情
def get_desc():
	import pymysql
	import urllib.request
	import urllib.parse
	import time
	import json
	
	conn = pymysql.connect(**CONFIG1)
	cur = conn.cursor()
	cur.execute("select id,iid from "+biaotou+"goods_bak where description is null  order by id desc")
	result = cur.fetchall()
	result_list = list(result)
	for i in result_list:
		url = "http://hws.m.taobao.com/cache/mtop.wdetail.getItemFullDesc/4.1/?data="+urllib.parse.quote_plus("{\"item_num_id\":\""+str(i[1])+"\"}")
		req = urllib.request.Request(url,headers=headers_dict)
		newdata = urllib.request.urlopen(req)
		readnewdata = newdata.read().decode('utf-8')
		try:
			json_newdata = json.loads(readnewdata)
			#此处进行正则替换，去除无效图片等
			newdesc = json_newdata['data']['desc']
			cur.execute("update "+biaotou+"goods_bak set description= '"+newdesc+"' where id = "+str(i[0]))
			print('suc'+str(i[0]))
		except:
			print('fail'+str(i[0]))
			continue
		finally:
			time.sleep(1)
	cur.close()

def get_et():
	import time
	
	m = str(int(time.time()))[2:10]
	o = [6,3,7,1,5,2,0,4]
	n = []
	for i in list(o):
		n.append(m[i])
	n[2] = str(9 - int(n[2]))
	n[4] = str(9 - int(n[4]))
	n[5] = str(9 - int(n[5]))
	return "".join(n)

def get_pgid():
	import random
	import hashlib
	
	num = random.uniform(1000,9999)
	m = hashlib.md5()
	m.update(str(num).encode('utf-8'))
	return m.hexdigest()


#此函数用于去淘宝抓取数据并更新数据
#sleep 3-10秒不等，避免被屏蔽
#模拟客户端user-agent
def update_goods():
	import random
	import urllib.parse
	import pymysql
	import urllib.request
	import json
	import time

	pid_list = {'alipid':'mm_44438063_4276096_15184916'}
	refer = "http://www.fsech.com/"
	
	conn = pymysql.connect(**CONFIG1)
	cur = conn.cursor()
	cur.execute("select id,iid,promotion_price from "+biaotou+"goods_bak where nick='' order by id desc")
	result = cur.fetchall()
	result_list = list(result)
	w_log = open('./pylog/get_desc_log.log','w')
	for i in result_list:
		jsonp = "jsonp_callback_0"+ str(random.randint(100000000,999999999))
		url = 'itemid%3d'+str(i[1])
		getjson_url = "http://g.click.taobao.com/display?cb="+jsonp+'&pid='+pid_list['alipid']+'&wt=0&rd=1&ct='+url+'&st=1&rf='+urllib.parse.quote_plus(refer)+'&et='+get_et()+'&pgid='+get_pgid()+'&v=2.0'
		req = urllib.request.Request(getjson_url,headers = headers_dict)
		data = urllib.request.urlopen(req)
		readdata = data.read().decode('utf-8')[26:-1]
		datatext = json.loads(readdata)
		#print(datatext)
		try:
			items = datatext['data']['items'][0]

			credit = 0
			if items['ds_istmall'] == 1:
				credit = 21
			else:
				credit = items['ds_rank']
			baoyou = 0
			if items['ds_postfee'] == 0:
				baoyou = 1
			gaijia = 1
			if items['ds_discount_price'] -1 > i[2]:
				gaijia = 2
			insert_sql = "update `"+biaotou+"goods_bak` set `nick`='"+items['ds_nick']+"',`tao_title`='"+items['ds_title']+"', `credit`='"+str(credit)+"',`baoyou`='"+str(baoyou)+"',`postfee`='"+str(items['ds_postfee'])+"',`istaoke`='"+str(items['ds_taoke'])+"',`provcity`='"+items['ds_provcity']+"',`gaijia`='"+str(gaijia)+"' where id = "+str(i[0])
			cur.execute(insert_sql)
			print(i[0])
			time.sleep(1)
		except:
			cur.execute("delete from "+biaotou+"goods_bak where id="+ str(i[0]))
			print('err:'+str(i[0]))
			w_log.write('err:'+str(i[0])+'\r\n')
	cur.close()
	w_log.close()

update_goods()
#get_desc()
