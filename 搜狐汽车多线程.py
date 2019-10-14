import queue
import requests
import re
import threading
import time
headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'
}

def idnames():
    idlist=queue.Queue()
    res=requests.get(url='http://db.auto.sohu.com/cxdata/xml/basic/brandList.xml',headers=headers)
    # print(res.text)
    lists={}
    name=re.findall('<brand name="(.*?)" id',res.text)
    id=re.findall('id="(.*?)">',res.text)
    for i in range(len(id)):
        lists={
            'name':name[i],
            'ids':id[i],
        }
        idlist.put(lists)
    return idlist
class MyThread(threading.Thread):#爬虫部分
    def __init__(self,id,name):
        super(MyThread,self).__init__(name=name)
        self.id=id
    def run(self):
        print(self.name+'开始爬取')
        while not self.id.empty():
            try:
                ID=self.id.get(block=False)
                # print(ID)
                idname=ID['ids']
                # print(idname)
                response=requests.get(url=f'http://db.auto.sohu.com/cxdata/xml/sales/brand/brand{idname}sales.xml',headers=headers)
                list={
                    'name':ID['name'],
                    'content':response.text,
                }
                print(self.name+'爬取内容成功')
                res.put(list)
            except Exception as e:
                print(e)
                pass
                print(self.name+'未获得url')
class parseThread(threading.Thread):#分析部分
    def __init__(self,content,name):
        super(parseThread, self).__init__(name=name)
        self.content=content
    def run(self):
        print(self.name+'开始')
        while parser_thread_exit_flag:
            try:
                contents=self.content.get(block=False)
                post=contents['content']
                time=re.findall('<sales date="(.*?)"',post)
                salenum=re.findall('salesNum="(.*?)"/>',post)
                lock.acquire()
                for i in range(len(time)):
                    with open('搜狐汽车.csv','a',encoding='utf-8')as f:
                        f.write('\n品牌{},时间{},销量{}\n'.format(contents['name'],time[i],salenum[i]))
                print(self.name+'保存成功')
                lock.release()
            except Exception as e:
                print(e)
                print(self.name+'未获取爬取内容')
                pass


if __name__=='__main__':
    print('主线程启动')
    frist=time.time()
    idname=idnames()
    res=queue.Queue()
    lock = threading.Lock()
    crawlspider=[]
    for i in range(1,6):
        mythread=MyThread(name='爬取爬虫'+str(i),id=idname)
        crawlspider.append(mythread)
    for n in crawlspider:
        n.start()
    parserspider=[]
    for i in range(1,15):
        parsethread=parseThread(name='分析爬虫'+str(i),content=res)
        parserspider.append(parsethread)
    parser_thread_exit_flag = True
    for n in parserspider:
        n.start()
    while not idname.empty():
        pass
    for n in crawlspider:
        n.join()
    while not res.empty():
        pass
    parser_thread_exit_flag = False
    for n in parserspider:
        n.join()
    last=time.time()
    print('-------------------------------主线程结束-----------------------------------')
    print('总时长：'+str(last-frist))


