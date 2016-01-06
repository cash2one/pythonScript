#!/usr/bin/python3
#coding:utf-8
#此脚本用于删除无效的图片

#mydd_path = 'D:/D/PHPnow/htdocs/mydd'
#upload_path = mydd_path + '/upload'
mydd_path = "/home/wrtyr/572rek"
upload_path = mydd_path +"/upload/2015"

import os
import pymysql
import config

CONFIG1 = config.CONFIG1
biaotou = config.biaotou

conn = pymysql.connect(**CONFIG1)
cur = conn.cursor()

w_log = open('pylog/del_img_log.log','w')
for root,dirs,files in os.walk(upload_path):
	for fn in files:
		file_dir = root+'/'+fn
		if 'avatar' not in file_dir:
			mydd_file_dir = file_dir.replace(mydd_path, " ").replace("\\",'/').strip()[1:]
			cur.execute("select id from "+biaotou+"goods where pic_url='"+mydd_file_dir+"' limit 1")
			result = cur.fetchone()
			cur.execute("select id from "+biaotou+"goods_bak where pic_url='"+mydd_file_dir+"' limit 1")
			result2 = cur.fetchone()
			if not result and not result2:
				print(file_dir)
				w_log.write(file_dir+'\r\n')
				os.remove(file_dir)
w_log.close()
cur.close()
