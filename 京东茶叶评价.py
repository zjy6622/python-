#由于协程本身是乱序的，I/O阻塞存在，无法保证写入得评价是连续的
#js破解文件在我JS项目里


# coding=gbk
from gevent import monkey
monkey.patch_all()
import requests
import gevent
import execjs
from lxml import etree
import re
import json
import time

lists=[]
headers={
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
}
def ip():
    ip=requests.get(url='http://127.0.0.1:5010/get/').text
    proxies = {
        "http": "http://" + ip,
        "https": "http://" + ip
    }
    res=requests.get(url='https://www.baidu.com',headers=headers)
    if res.status_code==200:
        return proxies
    else:
        ip()

def get_js_function(js_path, func_name):
    with open(js_path, encoding='utf-8') as fp:
        js = fp.read()
        ctx = execjs.compile(js)
        return ctx.call(func_name)

def get_html(keyword,pvid,num):
    g_lists=[]
    headers={
        'Referer': f'https://search.jd.com/Search?keyword=%E8%8C%B6%E5%8F%B6&enc=utf-8&wq=&pvid={pvid}',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
    }
    for pages in range(1,num+1):
        params = {
            'keyword':keyword ,
            'enc': 'utf-8',
            'wq': keyword,
            'page': pages,
        }
        s = gevent.spawn(get_href,params,headers)
        g_lists.append(s)
        gevent.joinall(g_lists)
    return lists
def get_href(params,headers):
    res = requests.get(url='https://search.jd.com/s_new.php?', headers=headers, params=params)
    # print(res.text)
    data = etree.HTML(res.text)
    li = data.xpath('//li[@class="gl-item"]')
    for i in li:
        href = i.xpath('.//div[@class="p-name p-name-type-2"]/a[@target="_blank"]/@href')[0]
        res2 = requests.get(url=f'https:{href}', headers=headers)
        comment = re.search("commentVersion:'(\d+)'", res2.text, re.S).group(1)
        productId = re.search('item.jd.com/(\d+).html', href).group(1)
        ls = (comment, productId)
        lists.append(ls)


def comment_json(key):
    callback=key[0]
    productId=key[1]
    num=3
    headers={
        'Referer': f'https://item.jd.com/{productId}.html',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
    }
    for pg in range(1,num+1):
        params={
            'callback': f'fetchJSON_comment98vv{callback}',
            'productId': productId,
            'score': 0,
            'sortType': 5,
            'page': pg,
            'pageSize': 10,
            'isShadowSku': 0,
            'rid': 0,
            'fold': 1
        }
        res=requests.get(url='https://sclub.jd.com/comment/productPageComments.action?',headers=headers,params=params)
        # print(res.text)
        try:
            data=re.search('fetchJSON_comment98vv\d*\((.*)\)',res.text).group(1)
            jsondata = json.loads(data)
            comments=jsondata.get('comments')
            for n in comments:
                pj=n.get('content')
                pjtime=n.get('creationTime')
                idname=n.get('id')
                commodity=n.get('referenceName')
                dat='{}{}{}{}'.format('\n商品：'+commodity,'   用户id：'+str(idname),'   评价内容：'+str(pj),'    评价时间：'+str(pjtime))
                save(dat)
        except AttributeError:
            print('无评价')
            pass


def save(data):
    with open('京东评价采集.csv','a+',encoding='utf-8')as f:
        f.write(data)



if __name__=="__main__":
    pvid=get_js_function(r'C:\Users\zjy\WebstormProjects\untitled\京东商品检索JS破解.js','genPvid')
    ks=get_html('茶叶',pvid,5)
    print(ks)
    time_begin = time.time()
    g_list = []
    for i in ks:
        s = gevent.spawn(comment_json, i)
        g_list.append(s)
    gevent.joinall(g_list)
    print(time.time() - time_begin)








