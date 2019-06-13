import requests
import json
import jsonpath
import re
import time
import pdfkit
import xlwt
import xlrd
##import excel_style # 自制库
from mitmproxy import ctx
import random
import os

os.system("ipconfig")
input("")

def response(flow):
    # 初始化excel文件
    workbook = xlwt.Workbook(encoding='utf-8')
    worksheet = workbook.add_sheet('data')
    worksheet.write(0, 0, u'序列',excel_style.set_color(0x00,True))
    worksheet.write(0, 1, u'标题',excel_style.set_color(0x00,True))
    worksheet.write(0, 2, u'作者',excel_style.set_color(0x00,True))
##    worksheet.write(0, 3, u'发文时间',excel_style.set_color(0x00,True))
    worksheet.write(0, 3, u'原文链接',excel_style.set_color(0x00,True))


    Referer = flow.request.headers['Referer']#Referer参数
    Cookie = flow.request.headers['Cookie']#Cookie参数
    Url = flow.request.url#Url


    if Referer and Cookie:
        headers = {
            'Host': 'mp.weixin.qq.com',
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 5.1.1; vivo x6s a Build/LMY47I) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/39.0.0.0 Mobile Safari/537.36 MMWEBID/3861 MicroMessenger/6.7.3.1360(0x260703B3) NetType/WIFI Language/zh_CN Process/toolsmp',
            'X-Requested-With': 'XMLHttpRequest',
            'Accept': '*/*',
            'Referer': Referer,
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,en-US;q=0.8',
            'Cookie': Cookie
        }

        #拆分Url的offset参数
        url1 = re.findall(r'(.*)offset=',Url)
        url2 = re.findall(r'offset=\d\d(.*)',Url)

        #初始化一些数据
        page = 0#页数
        titles = []
        links = []
        authors = []
        datetimes = []
        while True:
            #拼接url
            link = ''.join(url1)+'offset='+str(page*10)+''.join(url2)
            r = requests.get(link,headers=headers)#请求url
            r_json = json.loads(r.text)#转换成json格式
            can_msg_continue = jsonpath.jsonpath(r_json,'$..can_msg_continue')#can_msg_continue判断下一页的参数
            #判断有没有下一页，0，1
            if can_msg_continue[0] == 0: # "can_msg_continue":这个参数对应的是是否还有文章
                print('*'*32,'数据读取完毕！','*'*32)
                time.sleep(2)
                break
            else:
                json_data_list = jsonpath.jsonpath(r_json,'$..general_msg_list')#数据在general_msg_list里
                json_data = json.loads(''.join(json_data_list))#列表转字符串
                #数据提取
                title = jsonpath.jsonpath(json_data,'$..title')
                link = jsonpath.jsonpath(json_data,'$..content_url')
                author = jsonpath.jsonpath(json_data,'$..author')
##                datetime = jsonpath.jsonpath(json_data,'$..datetime')
                print('*'*24,'正在读取第',page,'页数据,请稍等……','*'*24)
                
                #聚合参数
                for i in range(len(title)):
                    titles.append(title[i])
                    links.append(link[i])
                    authors.append(author[i])
##                    datetimes.append(datetime[i])
            page += 1#控制页数
            time.sleep(random.randint(1,3))


        #写入excel数据
        print('*'*26,'数据写入中，请等待……','*'*26)
        for i in range(len(titles)):
            worksheet.write(i+1,0,label=i)
            worksheet.write(i+1,1,label=titles[i])
            worksheet.write(i+1,2,label=authors[i])
##            worksheet.write(i+1,3,label=datetimes[i])
            worksheet.write(i+1,3,label=links[i])
        workbook.save('data.xls')
        time.sleep(3)

        #读取数据
        print('*'*28,'正在读取数据……','*'*28)
        wb = xlrd.open_workbook('data.xls')
        sheet1 = wb.sheet_by_index(0)
        cols_title = sheet1.col_values(1)
        cols_url = sheet1.col_values(3)
        
        #整合并将网页保存为pdf
        try:
            sum_cols = dict(zip(cols_title,cols_url))
            for k,v in sum_cols.items():
                if k == '标题':
                    pass
                else:
                    print('-'*80)
                    print('\n采集数据中···：  ',k,'\n')
                    pdfkit.from_url(v,'F:\python\lei\pdf\\'+re.sub('[?\*\"/]','',k)+'.pdf')#网页保存为pdf格式
                    time.sleep(random.randint(0,2))
        except:
            pass


