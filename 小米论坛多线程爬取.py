import queue
import threading
import requests
from lxml import etree
import time
headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'
}
def start_url(page):
    pages=int(page)
    baseurl='http://bbs.xiaomi.cn/'
    for num in range(pages):
        surl=baseurl+f'/d-{num+1}'
        que.put(surl)

class urlthread(threading.Thread):
    def __init__(self,name,que):
        super(urlthread, self).__init__(name=name)
        self.que=que
    def run(self):
        while not que.empty():
            try:
                print(f'"{self.name}"启动')
                url=self.que.get()
                res = requests.get(url=url, headers=headers)
                data = etree.HTML(res.text)
                ul = data.xpath('//ul/li[@class="theme_list clearfix"]')
                for li in ul:
                    urls = li.xpath('.//div[@class="title"]/a/@href')[0]
                    que1.put(urls)
                print(f'"{self.name}"结束')
            except:
                print('起始队列空了')

class praserlthread(threading.Thread):
    def __init__(self,name,que1):
        super(praserlthread,self).__init__(name=name)
        self.que1=que1
    def run(self):
        while praserlthread_key:
            try:
                datas=[]
                print(f'"{self.name}"启动')
                url=self.que1.get(block=False)
                res=requests.get(url=url,headers=headers)
                data=etree.HTML(res.text)
                title=data.xpath('//h1/span[@class="name"]/text()')[0]
                datas.append(title)
                content=data.xpath('//div[@class="invitation_content"]//text()')
                contents = ''.join(content).strip()
                datas.append(contents)
                contenturl=data.xpath('//div[@class="invitation_content"]/p/img/@data-original')
                contenturls='    '.join(contenturl).strip()
                datas.append(contenturls)
                que2.put(datas)
                print(f'"{self.name}"结束')
            except:
                print('网址队列空了')

class save(threading.Thread):
    def __init__(self,name,que2):
        super(save,self).__init__(name=name)
        self.que2=que2
    def run(self):
        while save_key:
            try:
                print(f'"{self.name}"启动')
                data=self.que2.get(block=False)
                lock.acquire()
                content = '{}{}{}'.format('\n标题：' + data[0], '\n内容：' + data[1], '\n内容的图片链接：' + data[2])
                with open('小米论坛.csv','a+',encoding='utf-8')as f:
                    f.write(content)
                lock.release()
                print(f'"{self.name}"结束')
            except Exception as e:
                print(e)
                print('数据队列空了')

if __name__=='__main__':
    que=queue.Queue()
    start_url('30')
    lock=threading.Lock()
    que1=queue.Queue()
    urlthreads=[]
    praserlthreads=[]
    saves=[]
    praserlthread_key = True
    save_key = True
    print('————主线程启动————')
    stime=time.time()
    for n in range(3):
        t=urlthread(f'详情网页爬虫"{n}',que)
        t.start()
        urlthreads.append(t)
    que2 = queue.Queue()
    for s in range(3):
        p=praserlthread(f'网址爬虫"{s}',que1)
        p.start()
        praserlthreads.append(p)
    praserlthread_key = True
    for m in range(3):
        k=save(f'存储爬虫"{m}',que2)
        k.start()
        saves.append(k)
    save_key = True
    while not que.empty():
        pass
    for i in urlthreads:
        i.join()
    while not que1.empty():
        pass
    praserlthread_key=False
    for i in praserlthreads:
        i.join()
    while not que2.empty():
        print('*************************************************')
        pass
    save_key=False
    for i in saves:
        i.join()
    print('————主线程结束————')
    etime=time.time()
    stime=round(etime-stime,2)
    print('总时长：'+str(stime))






