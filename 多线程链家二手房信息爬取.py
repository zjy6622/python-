import threading
import requests
from parsel import Selector
import pymysql
from lxml import etree
import time
import queue
# pages=queue.Queue()
def pagespider():
    for page in range(1,101):
        url = f'https://hf.lianjia.com/ershoufang/pg{page}/'
        pages.put(url)
    return pages
class MyThread(threading.Thread):
    def __init__(self,name,pages):
        super(MyThread,self).__init__(name=name)
        self.pages=pages
    def run(self):
        print(self.name+'开始爬取')
        while not pages.empty():
            try:
                page=self.pages.get(block=False)
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'
                }
                print(self.name+'启动'+page)
                res=requests.get(url=page,headers=headers).text
                sel = Selector(res)
                name = sel.xpath('//a[@data-el="region"]/text()').getall()
                size = sel.xpath('//div[@class="houseInfo"]/text()').getall()
                timetype = sel.xpath('//div[@class="positionInfo"]/text()').getall()
                local = sel.xpath('//div[@class="positionInfo"]/a/text()').getall()
                price = sel.xpath('//div[@class="totalPrice"]/span/text()').getall()
                prices = sel.xpath('//div[@class="unitPrice"]/span/text()').getall()
                content = sel.xpath('//a[@data-el="ershoufang"][2]/text()').getall()
                for i in range(len(name)):
                    contents = '\n小区名称：{},\n介绍内容：{}\n房屋格局：{},\n楼板样式：{},\n地理位置：{},\n房屋总价：{}，\n每平方价格：{}'.format(name[i],content[i],size[i],timetype[i],local[i],price[i],prices[i])
                    saves.put(contents)
                # return saves
            except:
                print(self.name+'爬虫未获取url')
        print(self.name+'结束爬取')
class save(threading.Thread):
    def __init__(self,name,saves):
        super(save,self).__init__(name=name)
        self.saves=saves
    def run(self):
        print(self.name+'启动')
        while parser_thread_exit_flag:
            try:
                content=self.saves.get(block=False)
                # print(content)
                with open('链家多线程.csv','a',encoding='utf-8')as f:
                    f.write(content)
                print(self.name+'写入成功')
            except Exception :
               pass
        print(self.name+'多线程结束')

if __name__=='__main__':
    print('主线程开始')
    pages = queue.Queue()
    saves=queue.Queue()
    Page=pagespider()
    parser_thread_exit_flag=True
    lock = threading.Lock()
    threads=[]
    for i in range(5):
        thread=MyThread(name='爬虫'+str(i),pages=Page)
        threads.append(thread)
    for n in threads:
        n.start()
    savethreads=[]
    for i in range(5):
        savethread=save(name='存储爬虫'+str(i),saves=saves)
        savethreads.append(savethread)
    for n in savethreads:
        n.start()
    while not pages.empty():
        pass
    for i in threads:
        i.join()
    while not saves.empty():
        pass
    parser_thread_exit_flag = False
    for i in savethreads:
        i.join()
    print('-----主线程结束--------')


















