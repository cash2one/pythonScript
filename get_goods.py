#!/usr/bin/python3
#coding:utf-8
#此脚本用于从九块邮的api中获取产品列表

import config

CONFIG1 = config.CONFIG1
biaotou = config.biaotou
headers_dict = config.headers_dict

#获取api的xml数据
def get_api_xml():
	import urllib.request
	
	jiu_api = 'http://api.juanpi.com/open/jiukuaiyou'
	req = urllib.request.Request(jiu_api,headers = headers_dict)
	data = urllib.request.urlopen(req)
	readdata = data.read().decode('utf-8')
	return readdata


#解析xml并写入数据
def parse_xml():
	from xml.etree import ElementTree
	import time
	import pymysql
	import urllib.request
	import re

	title_list = ('丝袜','方便面','玛咖','前掌垫','发夹','书籍','果冻','保健枕','唇彩','口红','连衣裙','手拿包','文胸','键盘','鼠标','U盘','弹力背心','面筋','辣条','洞洞鞋','左旋肉碱','雪纺衫','指甲油','棒球棍','老花镜','女包','腰带','网鞋','电子表','瑜珈球','项链','香水','酸梅汤','连裤袜','耳钉','染发','睫毛膏','相框','哈伦裤','剃须刀','收音机','WIFI','内存卡','红酒','工字背心','足浴药粉','玉米软糖','脱毛膏','单肩包','燃油宝','化妆包','芝麻酱','维生素','直发器','安全头盔','罐头','鲜花饼','奔跑吧','睫毛','皮带','血糖仪','维D','小方包','腊肉','鱼饵','鼻毛修剪器','炼乳','猪油渣','凉鞋','移动电源','舒适女鞋','发蜡','眼线笔','头绳','胶囊','COCO','卫生巾','鱼嘴袜','葡萄酒','维生素片','手提大包','胎蜡','神皂','纹身贴','股市','包臀短裙','TF卡','对戒','表','信封包','假发','精油','眉笔','润滑剂','发卡')
	
	conn = pymysql.connect(**CONFIG1)
	cur = conn.cursor()
	root = ElementTree.fromstring(get_api_xml())
	for deal in root.iter('deal'):
		deal_list = {}
		is_have = False
		for n in list(deal):
			if n.tag == 'deal_title':
				deal_title_tmp = n.text
				deal_list['deal_title'] = n.text
				for tmp in tuple(title_list):
					if deal_title_tmp.find(tmp) != -1:
						print('KeyWord:'+tmp+' Title:'+deal_title_tmp)
						is_have = True
						break
			elif n.tag == 'deal_taobao_link':
				deal_list['deal_taobao_link'] = n.text
				deal_list['iid'] = n.text.split('=')[1]
			elif n.tag == 'deal_class_id':
				#母婴
				if n.text == '6':
					deal_list['cid'] = '67'
				#美妆
				elif n.text == '3':
					deal_list['cid'] = '66'
				#居家
				elif n.text == '187':
					deal_list['cid'] = '40'
				#服装
				elif (n.text == '2' or n.text == '275'):
					deal_list['cid'] = '36'
				#数码
				elif n.text == '188':
					deal_list['cid'] = '39'
				#文体
				elif n.text == '8':
					deal_list['cid'] = '41'
				#美食
				elif n.text == '5':
					deal_list['cid'] = '38'
				#其他
				else:
					deal_list['cid'] = '41'
			elif n.tag == 'deal_price':
				deal_list['promotion_price'] = n.text[:-2]
			elif n.tag == 'deal_start_time':
				deal_list['starttime'] = str(time.mktime(time.strptime(n.text,'%Y-%m-%d %H:%M:%S')))[:-2]
			elif n.tag == 'deal_cost_price':
				deal_list['price'] = n.text[:-2]
			elif n.tag == 'deal_image':
				#此处替换错误的jpg后缀
				if re.search(r"\.jpg\?t=\d+$",n.text) != None:
					deal_list['image'] = re.sub(r"jpg\?t=\d+$","jpg",n.text)
				elif re.search(r"jpg_\d{3}x\d{3}(q\d{2})?\.jpg$",n.text) != None:
					deal_list['image'] = re.sub(r"jpg_\d{3}x\d{3}(q\d{2})?\.jpg$","jpg",n.text)
				else:
					deal_list['image'] = n.text
			else:
				deal_list[n.tag] = n.text
		if not is_have:
			cur.execute("select id from "+biaotou+"goods_bak where iid = "+deal_list['iid']+" limit 1")
			result = cur.fetchone()
			cur.execute("select id from "+biaotou+"goods where iid = "+deal_list['iid']+" limit 1")
			result2 = cur.fetchone()
			
			if result2:
				print("Update:" + str(deal_list['iid']))
				update_sql = "update "+biaotou+"goods set xiajia=0 , starttime='"+deal_list['starttime']+"' where iid="+str(deal_list['iid'])
				cur.execute(update_sql)
			elif not result and not result2:
				print("Insert:"+str(deal_list['iid']))
				insert_sql = "insert into `"+biaotou+"goods_bak` (`cid`,`iid`,`price`,`title`,`addtime`,`promotion_price`,`goodtype`,`starttime`,`imgsrc`,`firstprice`) values ("+deal_list['cid']+","+deal_list['iid']+","+deal_list['price']+",'【包邮】"+deal_list['deal_title']+"',"+str(time.time())+","+deal_list['promotion_price']+",1,"+deal_list['starttime']+",'"+deal_list['image']+"',"+deal_list['promotion_price']+")"
				cur.execute(insert_sql)
			else:
				print('Have:'+str(deal_list['iid']))
		time.sleep(0.03)

parse_xml()
