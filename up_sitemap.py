#!/usr/bin/python3
#coding:utf-8
#此脚本用于更新网站地图

import pymysql
import datetime
import time
import config
from xml.dom.minidom import Document

CONFIG1 = config.CONFIG1
biaotou = config.biaotou

PATH = "/home/wrtyr/572rek/"
SITEURL = "http://www.fsech.com"

doc = Document()
urlset = doc.createElement("urlset")
urlset.setAttribute("xmlns","http://www.sitemaps.org/schemas/sitemap/0.9")
doc.appendChild(urlset)


conn = pymysql.connect(**CONFIG1)
cur = conn.cursor()
query_string1 = "select id,starttime from "+biaotou+"goods order by starttime desc, id desc"
cur.execute(query_string1)
result1 = cur.fetchall()
result1_list = list(result1)
result1_list_len = len(result1_list)
for i in range(result1_list_len):
	url = doc.createElement("url")
	urlset.appendChild(url)

	paragraph1 = doc.createElement("loc")
	url.appendChild(paragraph1)
	ptext = doc.createTextNode(SITEURL+'/item/'+str(result1_list[i][0])+'.html')
	paragraph1.appendChild(ptext)

	paragraph2 = doc.createElement("lastmod")
	url.appendChild(paragraph2)
	ptext2 = doc.createTextNode(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(result1_list[i][1])))
	paragraph2.appendChild(ptext2)

query_string2 = "select id,addtime from "+biaotou+"article order by id desc"
cur.execute(query_string2)
result2 = cur.fetchall()
result2_list = list(result2)
result2_list_len = len(result2_list)
for i in range(result2_list_len):
	url = doc.createElement("url")
	urlset.appendChild(url)

	paragraph1 = doc.createElement("loc")
	url.appendChild(paragraph1)
	ptext = doc.createTextNode(SITEURL+'/article/'+str(result2_list[i][0])+'.html')
	paragraph1.appendChild(ptext)

	paragraph2 = doc.createElement("lastmod")
	url.appendChild(paragraph2)
	ptext2 = doc.createTextNode(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(result2_list[i][1])))
	paragraph2.appendChild(ptext2)

query_string3 = "select id,addtime from "+biaotou+"mall order by sort desc,id desc"
cur.execute(query_string3)
result3 = cur.fetchall()
result3_list = list(result3)
result3_list_len = len(result3_list)
for i in range(result3_list_len):
	url = doc.createElement("url")
	urlset.appendChild(url)

	paragraph1 = doc.createElement("loc")
	url.appendChild(paragraph1)
	ptext = doc.createTextNode(SITEURL+'/mall/'+str(result3_list[i][0])+'.html')
	paragraph1.appendChild(ptext)

	paragraph2 = doc.createElement("lastmod")
	url.appendChild(paragraph2)
	ptext2 = doc.createTextNode(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(result3_list[i][1])))
	paragraph2.appendChild(ptext2)


sitemap = doc.toprettyxml(indent=" ")
wmap = open(PATH+"sitemap.xml","w")
wmap.write(sitemap)
