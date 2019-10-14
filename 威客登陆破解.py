import execjs
import requests
from aip import AipOcr
from chaojiying import Chaojiying_Client
headers={
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'referer': 'https://www.epwk.com/login.html',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
    # 'Cookie': 'Hm_lvt_387b8f4fdb89d4ea233922bdc6466394=1570501643,1570501842; cookie_login_multi_domain=login_domain; UM_distinctid=16da93523c53b3-0641a1c98d9da-67e1b3f-1fa400-16da93523c690c; Hm_lpvt_387b8f4fdb89d4ea233922bdc6466394=1570525141; visit_page_time=1570525364; PHPSESSID=6f0fface52157e04c4520b4ab3b6be5530d1edfd'

}
def jpg(path,num):
    params = {
        'pre': 'login',
        'sid': num
    }
    url = 'https://www.epwk.com/secode_show.php?'
    res = requests.Session().get(url=url, params=params, headers=headers)
    with open(path,'wb')as f:
        f.write(res.content)
    chaojiying=Chaojiying_Client('zjy6622', 'zjy19970927', '901769')
    im = open(path, 'rb').read()
    data=chaojiying.PostPic(im, 1902)
    return data['pic_str']
def hash(num):
    params={
        'do': 'ajax',
        'view': 'user_status',
        'rand': str(num),
        'index': 'login'
    }
    res=requests.post(url='https://www.epwk.com/index.php?',headers=headers,params=params).json()
    fromhash=res['data']['formhash']
    return  fromhash



def get_js_function(js_path, func_name, func_args):
    with open(js_path, encoding='utf-8') as fp:
        js = fp.read()
        ctx = execjs.compile(js)
        return ctx.call(func_name, func_args)
def denglu(account,password):
    data={
        'formhash': '9aaea8',
        'txt_account': account,
        'pwd_password': get_js_function('测试.js','user_login',password)[0],
        'login_type': 3,
        'ckb_cookie': 0,
        'hdn_refer':'https://i.epwk.com/Home/Index/index.html',
        'txt_code':'',
        'pre': 'login',
        'inajax': 1,
    }
    print(type(account))
    print(type(get_js_function('测试.js','user_login',password)[0]))
    s=requests.Session()
    res=s.post(url='https://www.epwk.com/index.php?do=login',headers=headers,data=data)
    res.text.encode('utf-8')
    # print(res.json())
    response=s.get(url='https://i.epwk.com/Home/Index/index.html',headers=headers)
    with open('k.html','a',encoding='utf-8')as f:
        f.write(response.text)
if __name__=='__main__':
    # num=get_js_function('测试.js','user_login','l')
    # print(num)
    # print((get_js_function('测试.js','user_login','3.1415926df'))[0])
    denglu('123123','123456')


