#!/usr/bin/python3
#coding:utf-8
#此脚本用于自动剪裁图片

import config
import re

CONFIG1 = config.CONFIG1
biaotou = config.biaotou
headers_dict = config.headers_dict

newsize = {'width':310,'height':310}
#root_path = "D:/D/PHPnow/htdocs/mydd/"
#tmp_path = "D:/D/PHPnow/htdocs/mydd/upload/tmp/"
root_path = "/home/wrtyr/572rek/"
tmp_path = "/home/wrtyr/572rek/upload/tmp/"

def auto_cut():
	import pymysql
	import os
	from PIL import Image
	import urllib.request
	import random
	import time
	import os.path
	
	conn = pymysql.connect(**CONFIG1)
	cur = conn.cursor()
	cur.execute("select id,imgsrc from "+biaotou+"goods_bak where pic_url='' order by id desc")
	result = cur.fetchall()
	result_list = list(result)
	nowtime = time.localtime(time.time())
	year = time.strftime("%Y", nowtime)
	month_day = time.strftime("%m%d", nowtime)
	pic_dir = 'upload/'+year+'/'+month_day+'/'
	if not os.path.exists(root_path + pic_dir):
		os.makedirs(root_path + pic_dir)
	for i in result_list:
		req = urllib.request.Request(i[1],headers = headers_dict)
		try:
			data = urllib.request.urlopen(req)
			readdata = data.read()
			filename = i[1][-13:-4]
			houzui = i[1][-4:]
			new_name = filename + '_'+ str(random.randint(10000,99999)) + houzui
			newpath = tmp_path + new_name 
			file = open(newpath,'wb')
			file.write(readdata)
			file.flush()
			file.close()

			img = Image.open(newpath)
			img = img.resize((newsize['width'], newsize['height']), Image.ANTIALIAS)
			pic_path = pic_dir + time.strftime("%H%M%S", time.localtime(time.time()))+str(random.randint(10000,99999)) + houzui
			img.save(root_path + pic_path)
			img.close()
			cur.execute("update "+biaotou+"goods_bak set pic_url = '"+pic_path+"' where id = "+str(i[0]))
			print(i[0])
			os.remove(newpath)
		except Exception as e:
			cur.execute("delete from "+ biaotou + "goods_bak where id="+str(i[0]))
			print("delete: "+ str(i[0]))
			print(e)
	cur.close()

auto_cut()
