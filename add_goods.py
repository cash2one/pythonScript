#!/usr/bin/python3
#coding:utf-8
#此脚本用于从九块邮的api中获取产品列表

import config

CONFIG1 = config.CONFIG1
biaotou = config.biaotou
headers_dict = config.headers_dict

newsize = {'width':310,'height':310}
#root_path = "D:/D/PHPnow/htdocs/mydd/"
#tmp_path = "D:/D/PHPnow/htdocs/mydd/upload/tmp/"
root_path = "/home/wrtyr/572rek/"
tmp_path = "/home/wrtyr/572rek/upload/tmp/"

class AddGood():
    def __init__(self):
       pass    

    #获取api的xml数据
    def get_api_xml(self):
        import urllib.request
        
        jiu_api = 'http://api.juanpi.com/open/jiukuaiyou'
        req = urllib.request.Request(jiu_api,headers = headers_dict)
        data = urllib.request.urlopen(req)
        readdata = data.read().decode('utf-8')
        return readdata


    #解析xml并写入数据
    def parse_xml(self):
        from xml.etree import ElementTree
        import time
        import pymysql
        import urllib.request
        import re

        title_list = ('丝袜','方便面','玛咖','前掌垫','发夹','书籍','果冻','保健枕','唇彩','口红','连衣裙','手拿包','文胸','键盘','鼠标','U盘','弹力背心','面筋','辣条','洞洞鞋','左旋肉碱','雪纺衫','指甲油','棒球棍','老花镜','女包','腰带','网鞋','电子表','瑜珈球','项链','香水','酸梅汤','连裤袜','耳钉','染发','睫毛膏','相框','哈伦裤','剃须刀','收音机','WIFI','内存卡','红酒','工字背心','足浴药粉','玉米软糖','脱毛膏','单肩包','燃油宝','化妆包','芝麻酱','维生素','直发器','安全头盔','罐头','鲜花饼','奔跑吧','睫毛','皮带','血糖仪','维D','小方包','腊肉','鱼饵','鼻毛修剪器','炼乳','猪油渣','凉鞋','移动电源','舒适女鞋','发蜡','眼线笔','头绳','胶囊','COCO','卫生巾','鱼嘴袜','葡萄酒','维生素片','手提大包','胎蜡','神皂','纹身贴','股市','包臀短裙','TF卡','对戒','表','信封包','假发','精油','眉笔','润滑剂','发卡')
        
        conn = pymysql.connect(**CONFIG1)
        cur = conn.cursor()
        root = ElementTree.fromstring(self.get_api_xml())
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

    def auto_cut(self):
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


    #此函数用于抓取产品详情
    def get_desc(self):
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

    def get_et(self):
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

    def get_pgid(self):
        import random
        import hashlib
        
        num = random.uniform(1000,9999)
        m = hashlib.md5()
        m.update(str(num).encode('utf-8'))
        return m.hexdigest()


    #此函数用于去淘宝抓取数据并更新数据
    #sleep 3-10秒不等，避免被屏蔽
    #模拟客户端user-agent
    def update_goods(self):
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
            getjson_url = "http://g.click.taobao.com/display?cb="+jsonp+'&pid='+pid_list['alipid']+'&wt=0&rd=1&ct='+url+'&st=1&rf='+urllib.parse.quote_plus(refer)+'&et='+self.get_et()+'&pgid='+self.get_pgid()+'&v=2.0'
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

 #   update_goods()

p = AddGood()
p.parse_xml()
p.auto_cut()
#p.update_goods()
p.get_desc()
