from mitmproxy import ctx
import requests,re,time,json,jsonpath,pdfkit,xlwt

def request(flow):
    headersd = {
        'Host': 'www.66ip.cn',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Cookie': 'Hm_lvt_1761fabf3c988e7f04bec51acd4073f4=1560137487,1560215210; __jsluid=cae5e4337ecf616bd8c3b970db29dc26; __jsl_clearance=1560215207.978|0|eHtJEuGnFHq4v23USJwztU9uUao%3D; Hm_lpvt_1761fabf3c988e7f04bec51acd4073f4=1560215213',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'max-age=0'
    }

    
    flow.request.headers['User-Agent'] = 'Mozilla/5.0 (Linux; Android 5.1.1; vivo x6s a Build/LMY47I) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/39.0.0.0 Mobile Safari/537.36 MMWEBID/3861 MicroMessenger/6.7.3.1360(0x260703B3) NetType/WIFI Language/zh_CN Process/toolsmp'
    referer = ''.join(flow.request.headers['Referer']).encode()
    cookie = ''.join(flow.request.headers['Cookie']).encode()
    url = flow.request.url#完整的url链接
    xg_url1 = re.findall(r'(.*)offset=',url)
    xg_url2 = re.findall(r'offset=\d\d(.*)',url)
    page = -1
    if referer and cookie:
        headers = {
            'Host': 'mp.weixin.qq.com',
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 5.1.1; vivo x6s a Build/LMY47I) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/39.0.0.0 Mobile Safari/537.36 MMWEBID/3861 MicroMessenger/6.7.3.1360(0x260703B3) NetType/WIFI Language/zh_CN Process/toolsmp',
            'X-Requested-With': 'XMLHttpRequest',
            'Accept': '*/*',
            'Referer': referer,
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,en-US;q=0.8',
            'Cookie': cookie
        }


        
        #创建excel数据表
        workbook = xlwt.Workbook(encoding = 'utf-8')
        worksheet = workbook.add_sheet('data')

        title = []
        urls = []
        author = []
        datetime = []
        while True:
            page = page+1
            link = ''.join(xg_url1)+'offset='+str(page*10)+''.join(xg_url2)
            r = requests.get(link,headers=headers,verify=False)

            html = json.loads(r.text)#转换成json格式
            json_data = jsonpath.jsonpath(html,'$..general_msg_list')
            json_data1 = json.loads(''.join(json_data))#列表转字符串
            json_title = jsonpath.jsonpath(json_data1,'$..title')#文章标题
            json_url = jsonpath.jsonpath(json_data1,'$..content_url')#url地址
            json_author = jsonpath.jsonpath(json_data1,'$..author')#文章作者
##            json_datetime = jsonpath.jsonpath(json_data1,'$..datetime')#文章更新日期
            content = jsonpath.jsonpath(json_data1,'$..id')#文章的id
            for i in range(len(json_url)):
                
                title.append(json_title[i])
                urls.append(json_url[i])
                author.append(json_author[i])
                datetime.append(json_datetime[i])
            title_url = dict(zip(json_title,json_url))
            try:
                for k,v in title_url.items():#获取页面文章
                    print('-'*80)
                    print('\n采集数据中···：',k,'\n')
                    r1 = requests.get(v,headers=headers)
                    r1.encoding='utf-8'
                    file = open('wangye.html','w',encoding='utf-8')
                    file.write(r1.text)
                    file.close()#保存网页文件
                    pdfkit.from_file('wangye.html','F:\python\lei\pdf\\'+k+'.pdf')#网页保存为pdf格式
            except:
                pass


        #行，列
        worksheet.write(0,0,label='序列')    
        worksheet.write(0,1,label='标题')
        worksheet.write(0,2,label='作者')
        worksheet.write(0,3,label='原文链接')
        for j in range(len(title)):
            worksheet.write(j+1,0,label=j)
            worksheet.write(j+1,1,label=title[j])
            worksheet.write(j+1,2,label=author[j])
            worksheet.write(j+1,3,label=urls[j])
            workbook.save('data.xls')
            
