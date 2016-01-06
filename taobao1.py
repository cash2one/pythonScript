#!/usr/bin/python3
#coding:utf-8
#此脚本用于更新产品的链接

import urllib.request
#import http.cookiejar
import json
import time
import pymysql

#推广位id
adzoneid = ''
#网站id
siteid = '4276***'
#淘宝客群id
groupid = '1375'
#http://pub.alimama.com/common/code/getAuctionCode.json?auctionid="+link+"&adzoneid="+adzoneid+"&siteid="+siteid+"&groupid="+groupid
#http://pub.alimama.com/urltrans/urltrans.json?adzoneid="+adzoneid+"&siteid="+siteid+"&promotionURL=http://detail.tmall.com/item.htm?id=43686313702"
CONFIG1 = {
	'host' : 'localhost', 
	'port' : 3306, 
	'user' : 'root', 
	'passwd' : '123456', 
	'db' : 'test1', 
	'charset' : "utf8"
}


biaotou = "f_"
cookie = "t=247dea4b982e7c8f4805716e16e165a8;cna=P8wJDcMACF8CAXPM5XG27ZQv;lzstat_uv=2594803490759702009|1774292@1774054@633924@2876347@2650839@2650835;pub-message-center=1;cookie2=7b8c70f7718d1793d41c68b0cb941df8;_tb_token_=XXIM233a7o;v=0;cookie32=986d17661c11125f04ee402ef65cf1f6;cookie31=NDQ0MzgwNjMsYmRzaDU4MTYseHM1ODE2QDE2My5jb20sVEI%3D;alimamapwag=TW96aWxsYS81LjAgKFdpbmRvd3MgTlQgNi4xKSBBcHBsZVdlYktpdC81MzcuMzYgKEtIVE1MLCBsaWtlIEdlY2tvKSBDaHJvbWUvNDEuMC4yMjQwLjAgU2FmYXJpLzUzNy4zNg%3D%3D;login=VT5L2FSpMGV7TQ%3D%3D;alimamapw=B10QCQBZAgM%2FAAxVVwdTAlYEBwxUWAcCVQVVAw4CUFMDAlBSUQgHBFc%3D;isg=F1293CCBF9DCC4C88AA638F78C2DA27D"

def setclick():
	conn = pymysql.connect(**CONFIG1)
	cur = conn.cursor()
	#query_string1 = "select id,iid from "+biaotou+"goods order by id desc"
	query_string1 = "select id,iid from "+biaotou+"goods where clickurla not like '%s.click.taobao%' order by id desc"
	cur.execute(query_string1)
	result1 = cur.fetchall()
	result1_list = list(result1)
	print(result1_list)
	result1_list_len = len(result1_list)
	for i in range(result1_list_len):
		geturl = "http://pub.alimama.com/urltrans/urltrans.json?adzoneid="+adzoneid+"&siteid="+siteid+"&promotionURL=http://item.taobao.com/item.htm?id="+str(result1_list[i][1])
		request = urllib.request.Request(geturl)
		request.add_header('Cookie', cookie)
		testre = urllib.request.urlopen(request)
		try:
			testtext = testre.read().decode('utf-8')
			testnewtext = json.loads(testtext)
			cur.execute("update "+biaotou+"goods set clickurla = '"+testnewtext['data']['sclick']+"' where id = "+str(result1_list[i][0]))
			print(str(result1_list[i][0]))
		except:
			cur.execute("update "+biaotou+"goods set clickurla = '' where id = "+str(result1_list[i][0]))
			continue
		finally:
			time.sleep(1)

setclick()

