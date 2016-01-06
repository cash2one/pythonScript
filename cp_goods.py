#!/usr/bin/python3
#coding:utf-8
#此脚本用于从goods_bak表中复制产品到goods表

import config
import pymysql

CONFIG1 = config.CONFIG1
biaotou = config.biaotou

conn = pymysql.connect(**CONFIG1)
cur = conn.cursor()
cur.execute("select id,iid from "+biaotou+"goods_bak order by id desc")
result = cur.fetchall()
result_list = list(result)
for i in result_list:
	cur.execute("select id from "+biaotou+"goods where iid = "+str(i[1])+" limit 1")
	result2 = cur.fetchone()
	if not result2:
		sql = "insert into `"+biaotou+"goods` (cid,iid,pic_url,price,title,nick,sort,addtime,credit,promotion_price,tuijian,baoyou,goodtype,postfee,istaoke,provcity,pricebackup,starttime,tao_title,imgsrc,firstprice,description,xiajia,yongjin,gaijia) select cid,iid,pic_url,price,title,nick,sort,addtime,credit,promotion_price,tuijian,baoyou,goodtype,postfee,istaoke,provcity,pricebackup,starttime,tao_title,imgsrc,firstprice,description,xiajia,yongjin,gaijia from `"+biaotou+"goods_bak` where id= "+str(i[0])
		cur.execute(sql)
		cur.execute("delete from `"+biaotou+"goods_bak` where id = "+str(i[0]))

 

