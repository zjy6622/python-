import requests
from xpinyin import Pinyin
import time

headers={
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
}
url='https://trains.ctrip.com/TrainBooking/Ajax/SearchListHandler.ashx?Action=getSearchList'

def gettrian(place,wplace,time,char1,char2):
    values = f'"IsBus": false, "Filter": "0", "Catalog": "", "IsGaoTie": false, "IsDongChe": false, "CatalogName": "","DepartureCity": "{char1}", "ArrivalCity": "{char2}", "HubCity": "", "DepartureCityName": "{place}","ArrivalCityName": "{wplace}", "DepartureDate": "{time}", "DepartureDateReturn": "{time}","ArrivalDate": "", "TrainNumber": ""'
    data = {
        'value': '{'+values+'}'
    }
    res=requests.get(url=url,headers=headers,data=data)
    data=res.json().get('TrainItemsList')
    lists = []
    for li in data:
        seats=[]
        TrainName=li.get('TrainName')
        EndStation=li.get('EndStationName')
        StartStation=li.get('StartStationName')
        StratTime=li.get('StratTime')
        EndTime=li.get('EndTime')
        TakeTime=li.get('TakeTime')
        datas=li.get('SeatBookingItem')
        for seat in datas:
            seatnum=str(seat.get('Inventory'))
            seatprice=seat.get('Price')
            seatname=seat.get('SeatName')
            content='{}{}{}'.format('座位：'+seatname,'   价格：'+seatprice,'   余票：'+seatnum)
            seats.append(content)
        if len(seats) == 2:
            seats.append('座位：无')
        elif len(seats) == 1:
            seats.append('座位：无')
            seats.append('座位：无')
        contents='{}{}{}{}{}{}{}'.format('车次：'+TrainName,'   起始站：'+StartStation+'('+StratTime+')','   到达站：'+EndStation+'('+EndTime+')','   总时长：'+TakeTime,'\n'+seats[2],'\n'+seats[1],'\n'+seats[0])
        # print(contents)
        lists.append(contents)
    data='\n'.join(lists)
    return data



def savefile(content):
    with open(r'C:\Users\zjy\Desktop\火车票查询.txt','w',encoding='utf-8')as f:
        f.write(content)
def translate(char):
    pin=Pinyin()
    text = pin.get_pinyin(char, "")
    return text
if __name__=='__main__':
    place=input('请输入出发地：')
    wplace=input('请输入目的地：')
    times=input('请输入出发时间（以xxxx-xx-xx的格式）：')
    char1=translate(place)
    char2=translate(wplace)
    keyword=input('是否需要持续刷新，如果是请输入“y”：')
    sleeps=input('默认刷新间隔15秒，请输入间隔时间（不建议间隔过短，可能会导致ip封禁）：')
    if type(sleeps) == "<class 'int'>":
        sleeptime=sleeps
    else:
        sleeptime=15
    if keyword=='y' or 'Y':
        key=True
    else:
        key=False
    num=0
    while key:
        data=gettrian(place,wplace,times,char1,char2)
        savefile('刷新次数：'+str(num)+'\n'+data)
        print('刷新次数：'+str(num))
        time.sleep(sleeptime)
        num+=1

