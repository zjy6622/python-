import execjs
import requests
headers={
    'Host': 'www.lrts.me',
    'Origin': 'http://www.lrts.me',
    'Referer': 'http://www.lrts.me/setting/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
    'Cookie': 'aliyungf_tc=AQAAADYERSDwoAoA9TxrchEs8Bg7BW7y; uid=1570591522677f5b5e36231374c71b74cd72d2d6537f0; CNZZDATA1254668430=1650427009-1570606279-http%253A%252F%252Fwww.lrts.me%252F%7C1570606279; Hm_lvt_ada61571fd48bb3f905f5fd1d6ef0ec4=1570591479,1570610812; JSESSIONID=6412736C7624F8224F84F43D703FDE54; sid=85241258C9B7113DC5E41349BD69CBBC56F7B59F5609A2934273F5ED237BF1763508F44AA735461E957F94C415ED51157B351A96FF21B26311EDF573EE12C5A4; Hm_lpvt_ada61571fd48bb3f905f5fd1d6ef0ec4=1570610845'
}

def get_token(name):
    data={
        'accountName': name
    }
    url='http://www.lrts.me/user/login_token.do'
    res=requests.post(url=url,headers=headers,data=data).json()
    token=res.get('data')
    return token
def get_js_function(js_path, func_name, func_args,arg1,arg2):
    with open(js_path, encoding='utf-8') as fp:
        js = fp.read()
        ctx = execjs.compile(js)
        return ctx.call(func_name, func_args,arg1,arg2)

def denglu(hasspass,name):
    data={
        'accountName': str(name),
        'hashPass': str(hasspass),
        'autoLogin': 0,
        'validateCode':''
    }
    res=requests.Session().post(url='http://www.lrts.me/user/login.do',headers=headers,data=data)
    print(res.text)
    print(res.json())

if __name__=='__main__':
    name='17352910858'
    password='zjy19970927'
    token=get_token(name)
    print(token)
    hasspass=get_js_function(r'C:\Users\zjy\WebstormProjects\untitled\懒人.js','res',name,password,token)
    print(hasspass)
    denglu(hasspass,name)
