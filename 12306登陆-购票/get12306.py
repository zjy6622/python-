import requests,re,time
from chaojiyin import Chaojiying_Client
from PIL import Image
from find_tick import cli
from urllib.parse import unquote,quote
from stations import stations
class dl_12306:
    def __init__(self,name,password,data,fromstation,tostation,dev=False,yz=True):#dev:调试模式，返回携带的cookies  yz：True-手动填写验证码 False-超级鹰
        self.name=name
        self.dev=dev
        self.yz=yz
        self.password=password
        self.session=requests.session()
        self.data=data
        self.fromstation = fromstation
        self.tostation = tostation
        self.headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
        }

    def get_code(self):
        self.session.get(url='https://kyfw.12306.cn',headers=self.headers)
        url = 'https://kyfw.12306.cn/passport/captcha/captcha-image?login_site=E&module=login&rand=sjrand'
        resp = self.session.get(url=url)
        with open('12306_code.png','wb')as f:
            f.write(resp.content)
        answer = {"1": "40,40","2": "110,40","3": "180,40","4": "260,40","5": "40,120","6": "110,120","7": "180,120","8": "260,120"}
        img = Image.open('12306_code.png').show()
        print("+----------+----------+----------+----------+")
        print("|    1     |    2     |    3     |    4     |")
        print("|----------|----------|----------|----------|")
        print("|    5     |    6     |    7     |    8     |")
        print("+----------+----------+----------+----------+")
        input_code = input("请在1—8中选择输入验证图片编号，以半角','隔开。(例如：1,3,5):")
        answer_code = ''
        for i in input_code.split(','):
            answer_code += ',' + answer[i] if (i is not input_code[0]) else answer[i]
        self.code=answer_code
        print(answer_code)
        requests.utils.add_dict_to_cookiejar(self.session.cookies, {'RAIL_DEVICEID':'eNGRsGtUwUiNZRa4WEN64EW_5stjGbpcu0fJLA-xQ2bGHOGlD6OIKDs7Y19y--rQu8wR9mWClrrzqfYk0aADMSDt33m7C-Qqf6S5YpU2fehq3yhtAs8qVrPuhYMd9b0KOCgHUEsUoIwmXLcWl-u3DEmcBYml6QgN','RAIL_EXPIRATION':'1575086207975'})
        if self.dev==True:
            t = re.findall("name='(.*?)', value='(.*?)'", str(self.session.cookies.get_dict))
            cook = {li[0]: li[1] for li in t}
            print('get_code--cookies',end='')
            print(cook)

    def get_code2(self):
        print('-------------------------')
        url = 'https://kyfw.12306.cn/passport/captcha/captcha-image?login_site=E&module=login&rand=sjrand'
        resp = self.session.get(url=url)
        with open(r'C:\Users\zjy\Desktop\s.png', 'wb')as f:
            f.write(resp.content)
        chaojiying = Chaojiying_Client('', '', '901769')
        im = open(r'C:\Users\zjy\Desktop\s.png', 'rb').read()
        print("---------等待code识别---------")
        codes = chaojiying.PostPic(im, 9008)
        cod = codes.get('pic_str')
        self.im_id = codes.get('pic_id')
        self.code = re.sub('\|', ',', cod)
        requests.utils.add_dict_to_cookiejar(self.session.cookies, {'RAIL_DEVICEID': 'eNGRsGtUwUiNZRa4WEN64EW_5stjGbpcu0fJLA-xQ2bGHOGlD6OIKDs7Y19y--rQu8wR9mWClrrzqfYk0aADMSDt33m7C-Qqf6S5YpU2fehq3yhtAs8qVrPuhYMd9b0KOCgHUEsUoIwmXLcWl-u3DEmcBYml6QgN','RAIL_EXPIRATION': '1575086207975'})
        print(self.code)
        if self.dev == True:
            t = re.findall("name='(.*?)', value='(.*?)'", str(self.session.cookies.get_dict))
            cook = {li[0]: li[1] for li in t}
            print('get_code2--cookies', end='')
            print(cook)


    def code_check(self):
        print('-------------------------')
        headers={
            'Host': 'kyfw.12306.cn',
            'Referer': 'https://kyfw.12306.cn/otn/resources/login.html',
            'Sec-Fetch-Mode': 'no-cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
        }
        url='https://kyfw.12306.cn/passport/captcha/captcha-check?'
        params={
            'answer': self.code,
            'rand': 'sjrand',
            'login_site': 'E'
        }
        resp=self.session.get(url=url,params=params,headers=headers)
        print(resp.text)
        if resp.json().get('result_code')=='5':
            print('验证码校验失败')
            return False
        else:
            if self.dev == True:
                t = re.findall("name='(.*?)', value='(.*?)'", str(self.session.cookies.get_dict))
                cook = {li[0]: li[1] for li in t}
                print('check--cookies', end='')
                print(cook)
            return True

    def login(self):
        print('-------------------------')
        url='https://kyfw.12306.cn/passport/web/login'
        headers={
            'Host': 'kyfw.12306.cn',
            'Origin': 'https://kyfw.12306.cn',
            'Referer': 'https://kyfw.12306.cn/otn/resources/login.html',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',

        }
        data={
            'username': self.name,
            'password': self.password,
            'appid': 'otn',
            'answer': self.code,
        }
        resp=self.session.post(url=url,data=data,headers=headers)
        print(resp.text)
        if self.dev == True:
            t = re.findall("name='(.*?)', value='(.*?)'", str(self.session.cookies.get_dict))
            cook = {li[0]: li[1] for li in t}
            print('login--cookies', end='')
            print(cook)

    def userlogin(self):
        print('-------------------------')
        self.session.cookies.set('_passport_ct',None)
        self.session.cookies.set('_passport_session', None)
        url='https://kyfw.12306.cn/otn/login/userLogin'
        headers = {
            'Host': 'kyfw.12306.cn',
            'Origin': 'https://kyfw.12306.cn',
            'Referer': 'https://kyfw.12306.cn/otn/resources/login.html',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',

        }
        resp=self.session.get(url=url,headers=headers)
        print('userlogin')
        # print(resp.text)
        if self.dev == True:
            t = re.findall("name='(.*?)', value='(.*?)'", str(self.session.cookies.get_dict))
            cook = {li[0]: li[1] for li in t}
            print('userlogin--cookies', end='')
            print(cook)
    def passport(self):
        print('-------------------------')
        url='https://kyfw.12306.cn/otn/passport?redirect=/otn/login/userLogin'
        headers = {
            'Host': 'kyfw.12306.cn',
            'Origin': 'https://kyfw.12306.cn',
            'Referer': 'https://kyfw.12306.cn/otn/resources/login.html',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',

        }
        resp=self.session.get(url=url,headers=headers)
        print('passport')
        # print(resp.text)
        if self.dev == True:
            t = re.findall("name='(.*?)', value='(.*?)'", str(self.session.cookies.get_dict))
            cook = {li[0]: li[1] for li in t}
            print('passport--cookies', end='')
            print(cook)

    def umart(self):
        print('-------------------------')
        url='https://kyfw.12306.cn/passport/web/auth/uamtk'
        headers={
            'Host': 'kyfw.12306.cn',
            'Origin': 'https://kyfw.12306.cn',
            'Referer': 'https://kyfw.12306.cn/otn/passport?redirect=/otn/login/userLogin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',

        }
        data={
            'appid':'otn'
        }
        resp=self.session.post(url=url,headers=headers,data=data)
        print(resp.text)
        self.newapptk=resp.json().get('newapptk')
        if self.dev == True:
            t = re.findall("name='(.*?)', value='(.*?)'", str(self.session.cookies.get_dict))
            cook = {li[0]: li[1] for li in t}
            print('umart--cookies', end='')
            print(cook)


    def uamauthclient(self):
        self.session.cookies.set('_passport_session', None)
        print('-------------------------')
        # print(self.newapptk)
        url='https://kyfw.12306.cn/otn/uamauthclient'
        headers={
            'Host': 'kyfw.12306.cn',
            'Origin': 'https://kyfw.12306.cn',
            'Referer': 'https://kyfw.12306.cn/otn/passport?redirect=/otn/login/userLogin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',

        }
        data={
            'tk':self.newapptk
        }
        resp=self.session.post(url,headers=headers,data=data)
        print(resp.text)
        if self.dev == True:
            t = re.findall("name='(.*?)', value='(.*?)'", str(self.session.cookies.get_dict))
            cook = {li[0]: li[1] for li in t}
            print('uamauthclient--cookies', end='')
            print(cook)

    def checklogin(self):
        url = 'https://exservice.12306.cn/excater/login/checkLogin'
        headers = {
            'Host': 'exservice.12306.cn',
            'Origin': 'https://exservice.12306.cn',
            'Referer': 'https://exservice.12306.cn/otn/index.html',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
        }
        resp = self.session.post(url=url, headers=headers)
        print('-------------------------')
        try:
            print('12306用户：' + resp.json().get('data').get('name') + ' 验证通过，登陆成功')
            return True
        except:
            print(resp.text)
            return False

    def userLogins(self):
        print('-------------------------')
        url='https://kyfw.12306.cn/otn/login/userLogin'
        headers={
            'Host': 'kyfw.12306.cn',
            'Origin': 'https://kyfw.12306.cn',
            'Referer': 'https://kyfw.12306.cn/otn/passport?redirect=/otn/login/userLogin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
        }
        resp=self.session.get(url=url,headers=headers)
        print('userLogins')
        # print(resp.content.decode('utf-8'))
        if self.dev == True:
            t = re.findall("name='(.*?)', value='(.*?)'", str(self.session.cookies.get_dict))
            cook = {li[0]: li[1] for li in t}
            print('userLogins--cookies', end='')
            print(cook)

    def api(self):
        print('-------------------------')
        url='https://kyfw.12306.cn/otn/index/initMy12306Api'
        headers={
            'Host': 'kyfw.12306.cn',
            'Origin': 'https://kyfw.12306.cn',
            'Referer': 'https://kyfw.12306.cn/otn/view/index.html',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',

        }
        resp=self.session.post(url=url,headers=headers)
        print(resp.text)

    def find_ticket(self):
        print('-------------------------')
        # session.get(url='https://www.12306.cn/index/index.html', headers=headers)
        self.session.get(url='https://kyfw.12306.cn/otn/leftTicket/init?', headers=self.headers)
        # self.data = '2019-11-27'
        # self.fromstation = '合肥'
        # self.tostation = '上海'
        self.from_station = stations.get(self.fromstation)
        self.to_station = stations.get(self.tostation)
        print('*' * 15 + '余票查询' + '*' * 15)
        content=cli(self.session, self.data, self.from_station, self.to_station)
        if self.dev == True:
            t = re.findall("name='(.*?)', value='(.*?)'", str(self.session.cookies.get_dict))
            cook = {li[0]: li[1] for li in t}
            print('ticket--cookies', end='')
            print(cook)
        keys=input('输入需要购买的车次：')
        if content.get(keys, None):
            self.secret=content.get(keys,None)
            print(self.secret)
        else:
            print('列车不存在或停运！')
    def submitOrderRequest(self):
        print('-------------------------')
        tstation=str(self.fromstation.encode("unicode-escape")).replace("\\\\","%")[1:]
        tstations=re.findall('\'(.*?)\'',tstation)[0]
        fstation=str(self.tostation.encode("unicode-escape")).replace("\\\\","%")[1:]
        fstations=re.findall('\'(.*?)\'',fstation)[0]
        print(f'{tstations}%2C{self.from_station}')
        url='https://kyfw.12306.cn/otn/leftTicket/submitOrderRequest'
        requests.utils.add_dict_to_cookiejar(self.session.cookies, {
            '_jc_save_fromDate': self.data,
            '_jc_save_fromStation': f'{tstations}%2C{self.from_station}',
            '_jc_save_toDate':self.data,
            '_jc_save_toStation': f'{fstations}%2C{self.to_station}',
            '_jc_save_wfdc_flag':'dc',
        })

        headers={
            'Host': 'kyfw.12306.cn',
            'Origin': 'https://kyfw.12306.cn',
            'Referer': f'https://kyfw.12306.cn/otn/leftTicket/init?linktypeid=dc&fs={quote(self.fromstation,"utf-8")},{self.from_station}&ts={quote(self.tostation,"utf-8")},{self.to_station}&date={self.data}&flag=N,N,Y',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
        }
        data = {
            'secretStr': unquote(self.secret[0], 'utf-8'),
            'train_date': self.data,
            'back_train_date': self.data,
            'tour_flag': 'dc',
            'purpose_codes': 'ADULT',
            'query_from_station_name': self.fromstation,
            'query_to_station_name': self.tostation,
            'undefined': '',
        }
        resp=self.session.post(url=url,headers=headers,data=data)
        print(resp.text)
        if self.dev == True:
            t = re.findall("name='(.*?)', value='(.*?)'", str(self.session.cookies.get_dict))
            cook = {li[0]: li[1] for li in t}
            print('submit--cookies', end='')
            print(cook)

    def initDC(self):
        print('-------------------------')
        url = 'https://kyfw.12306.cn/otn/confirmPassenger/initDc'
        headers = {
            'Host': 'kyfw.12306.cn',
            'Origin': 'https://kyfw.12306.cn',
            'Referer': f'https://kyfw.12306.cn/otn/leftTicket/init?linktypeid=dc&fs={quote(self.fromstation,"utf-8")},{self.from_station}&ts={quote(self.tostation,"utf-8")},{self.to_station}&date={self.data}&flag=N,N,Y',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
        }
        data={'_json_att':''}
        resp=self.session.post(url=url,data=data,headers=headers)
        try:
            self.token=re.findall("var globalRepeatSubmitToken = '(.*?)'",resp.text)[0]
            self.check_key=re.findall("'key_check_isChange':'(.*?)'",resp.text)[0]
            print(self.token,self.check_key)
        except:
            print('登陆失败')

    def passenger(self):
        print('-------------------------')
        url='https://kyfw.12306.cn/otn/confirmPassenger/getPassengerDTOs'
        headers={

            'Host': 'kyfw.12306.cn',
            'Origin': 'https://kyfw.12306.cn',
            'Referer': 'https://kyfw.12306.cn/otn/confirmPassenger/initDc',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',

        }
        data={
            '_json_att':'',
            'REPEAT_SUBMIT_TOKEN':self.token
        }
        resp=self.session.post(url=url,headers=headers,data=data)
        datas=resp.json()
        normal=datas.get('data').get('normal_passengers')
        lists=list()
        ns=list()
        for li in normal:
            estr=li.get('allEncStr')
            names=li.get('passenger_name')
            ns.append(names)
            nameid=li.get('passenger_id_no')
            flag=li.get('passenger_flag')
            id_type_code=li.get('passenger_id_type_code')
            buy_type=li.get('passenger_type')
            content=(estr,names,nameid,flag,id_type_code,buy_type)
            lists.append(content)
        print('输入购买人姓名')
        for i in enumerate([n for n in ns],start=1):
            print(i)
        num=input('购买人编号：')
        self.information=lists[int(num)-1]

    def checkOrderInfo(self):
        print('-------------------------')
        print('高铁:一等座-M，\n  二等座-O（大写英文字母）\n普通车：硬座-1，\n  软座-2，\n  硬卧-3，\n  软卧-4')
        self.key=input('输入购买车票类型:')
        print('成人票-1，\n学生票-3\n(参数没改只支持成人票，太懒了)')
        self.type=input('输入购票人购票身份类型（使用默认请回车）:')
        if self.type=='':
            type=self.information[5]
        url='https://kyfw.12306.cn/otn/confirmPassenger/checkOrderInfo'
        headers={

            'Host': 'kyfw.12306.cn',
            'Origin': 'https://kyfw.12306.cn',
            'Referer': 'https://kyfw.12306.cn/otn/confirmPassenger/initDc',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
        }
        data={
            'cancel_flag': '2',
            'bed_level_order_num': '000000000000000000000000000000',
            'passengerTicketStr': f'{self.key},0,{self.type},{self.information[1]},{self.information[4]},{self.information[2]},,N,{self.information[0]}',
            'oldPassengerStr': f'{self.information[1]},{self.information[4]},{self.information[2]},{self.type}_',
            'tour_flag': 'dc',
            'randCode': '',
            'whatsSelect': '1',
            '_json_att': '',
            'REPEAT_SUBMIT_TOKEN': self.token,
        }
        print(data)
        resp=self.session.post(url=url,headers=headers,data=data)
        print(resp.text)

    def getQueueCount(self):
        print('-------------------------')
        times=self.trans_data(self.data)
        url='https://kyfw.12306.cn/otn/confirmPassenger/getQueueCount'
        headers={

            'Host': 'kyfw.12306.cn',
            'Origin': 'https://kyfw.12306.cn',
            'Referer': 'https://kyfw.12306.cn/otn/confirmPassenger/initDc',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
        }
        data={
            'train_date': times,
            'train_no': self.secret[1],
            'stationTrainCode': self.secret[2],
            'seatType': self.key,
            'fromStationTelecode': self.from_station,
            'toStationTelecode': self.to_station,
            'leftTicket': self.secret[3],
            'purpose_codes': '00',
            'train_location': self.secret[4],
            '_json_att': '',
            'REPEAT_SUBMIT_TOKEN': self.token,

        }
        print(data)
        resp=self.session.post(url=url,headers=headers,data=data)
        print(resp.text)

    def confirmGoForQueue(self):
        # self.session.cookies.set('uamtk', None)
        print('-------------------------')
        url='https://kyfw.12306.cn/otn/confirmPassenger/confirmSingleForQueue'
        headers = {

            'Host': 'kyfw.12306.cn',
            'Origin': 'https://kyfw.12306.cn',
            'Referer': 'https://kyfw.12306.cn/otn/confirmPassenger/initDc',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
        }
        data={
            'passengerTicketStr':  f'{self.key},0,{self.type},{self.information[1]},{self.information[4]},{self.information[2]},,N,{self.information[0]}',
            'oldPassengerStr': f'{self.information[1]},{self.information[4]},{self.information[2]},{self.type}_',
            'randCode': '',
            'purpose_codes': '00',
            'key_check_isChange': self.check_key,
            'leftTicketStr': self.secret[3],
            'train_location':self.secret[4],
            'choose_seats': '',
            'seatDetailType': '000',
            'whatsSelect': '1',
            'roomType': '00',
            'dwAll': 'N',
            '_json_att': '',
            'REPEAT_SUBMIT_TOKEN': self.token,
        }
        print(data)
        resp=self.session.post(url=url,headers=headers,data=data)
        print(resp.text)
        if self.dev == True:
            t = re.findall("name='(.*?)', value='(.*?)'", str(self.session.cookies.get_dict))
            cook = {li[0]: li[1] for li in t}
            print('confirmGoForQueue--cookies', end='')
            print(cook)
    def queryOrderWaitTime(self):
        print('-------------------------')
        self.qtimes=int(round(time.time() * 1000))
        print(self.qtimes)
        url='https://kyfw.12306.cn/otn/confirmPassenger/queryOrderWaitTime?'
        params={
            'random': self.qtimes,
            'tourFlag': 'dc',
            '_json_att': '',
            'REPEAT_SUBMIT_TOKEN': self.token,
        }
        headers = {

            'Host': 'kyfw.12306.cn',
            'Origin': 'https://kyfw.12306.cn',
            'Referer': 'https://kyfw.12306.cn/otn/confirmPassenger/initDc',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
        }
        resp=self.session.get(url=url,headers=headers,params=params)
        print(resp.text)
        try:
            self.orderId=resp.json().get('data').get('orderId')
            print(self.orderId)
        except:
            print('error')
            print(resp.text)

    def queryOrderWaitTime2(self):
        print('-------------------------')
        times=self.qtimes+18
        print(times)
        url='https://kyfw.12306.cn/otn/confirmPassenger/queryOrderWaitTime?'
        params={
            'random': times,
            'tourFlag': 'dc',
            '_json_att': '',
            'REPEAT_SUBMIT_TOKEN': self.token,
        }
        headers = {

            'Host': 'kyfw.12306.cn',
            'Origin': 'https://kyfw.12306.cn',
            'Referer': 'https://kyfw.12306.cn/otn/confirmPassenger/initDc',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
        }
        resp=self.session.get(url=url,headers=headers,params=params)
        try:
            self.orderId=resp.json().get('data').get('orderId')
            print(self.orderId)
        except:
            print('error')
            print(resp.text)

    def resultOrderForWcQueue(self):
        print('-------------------------')
        url='https://kyfw.12306.cn/otn/confirmPassenger/resultOrderForWcQueue'
        headers = {
            'Host': 'kyfw.12306.cn',
            'Origin': 'https://kyfw.12306.cn',
            'Referer': 'https://kyfw.12306.cn/otn/confirmPassenger/initDc',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
        }
        data={
            'orderSequence_no': self.orderId,
            '_json_att': '',
            'REPEAT_SUBMIT_TOKEN': self.token,
        }
        resp=self.session.post(url=url,headers=headers,data=data)
        print(resp.text)

    @staticmethod
    def trans_data(data):
        yf = re.findall('(.*?)-(.*?)-(\d{2})', data)[0]
        # print(yf)
        time_tupl = (int(yf[0]), int(yf[1]), int(yf[2]), 0, 0, 0, 0, 0, 0)
        bt = re.findall('(.*?) 00:00:00 (\d{4})', time.asctime(time_tupl))[0]
        # print(bt[0])
        stime = f'{bt[0]} {bt[1]} 00:00:00 GMT+0800 (中国标准时间)'
        print(stime)
        return stime
    def queryMyOrderNoComplete(self):
        print('-------------------------')
        url='https://kyfw.12306.cn/otn/queryOrder/queryMyOrderNoComplete'
        resp=self.session.post(headers=self.headers,url=url,data={'_json_att': ''})
        # print(resp.text)
        try:
            print(resp.json())
            print('成功订票，请前往12306支付')
        except:
            print('订票失败')
    def main(self):
        try:
            if self.yz:
                self.get_code()
            else:
                self.get_code2()
            if self.code_check():
                self.login()
                self.userlogin()
                self.passport()
                self.umart()
                self.uamauthclient()
                self.userLogins()
                self.api()
                self.find_ticket()
                self.submitOrderRequest()
                self.initDC()
                self.passenger()
                self.checkOrderInfo()
                self.getQueueCount()
                self.confirmGoForQueue()
                self.queryOrderWaitTime()
                self.resultOrderForWcQueue()
                self.queryMyOrderNoComplete()
            else:
                self.main()
        except BaseException as f:
            print(f)
            
