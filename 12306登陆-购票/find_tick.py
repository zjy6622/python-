import requests
from prettytable import PrettyTable
from colorama import Fore
from stations import station,stations


def cli(session,data,from_station,to_station):
    # data = '2019-11-20'

    url = f'https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date={data}&leftTicketDTO.from_station={from_station}&leftTicketDTO.to_station={to_station}&purpose_codes=ADULT'
    headers={
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        # 'Cookie': 'JSESSIONID=E5600FC1F19DA0BBE66A74A87435A6C0; _jc_save_wfdc_flag=dc; RAIL_EXPIRATION=1574504448100; RAIL_DEVICEID=G0fZOpKktbO9HYlpZGDk-RLrKhOue7n5WxjM7ry2aVUNWmmUsbIHa4ur07L6I5KFali4_S-LIj1as8zBZxgDy7vqjOhdBkF-MA3RDVlbc6WGEnMYGbhoaCpgikNzbJ_bIPgKUtaLfD4SAFB1c5XwuXLQhXaAEeVw; ten_key=N2JvTcIoiW6cNB/DDGwRYM2VS5YG0czv; ten_js_key=N2JvTcIoiW6cNB%2FDDGwRYM2VS5YG0czv; route=6f50b51faa11b987e576cdb301e545c4; BIGipServerotn=720372234.50210.0000; BIGipServerpool_passport=233636362.50215.0000; _jc_save_fromStation=%u5408%u80A5%2CHFH; _jc_save_toStation=%u6DEE%u5357%2CHAH; _jc_save_toDate=2019-11-20; _jc_save_fromDate=2019-11-20',
        'Host': 'kyfw.12306.cn',
        'If-Modified-Since': '0',
        'Referer': 'https://kyfw.12306.cn/otn/leftTicket/init?linktypeid=dc&fs=%E5%90%88%E8%82%A5,HFH&ts=%E6%B7%AE%E5%8D%97,HAH&date=2019-11-20&flag=N,N,Y',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }
    content={}
    r = session.get(url,headers=headers)
    # 　　requests得到的是一个json格式的对象，ｒ.json()转化成python字典格式数据来提取，所有的车次结果result
    raw_trains = r.json()['data']['result']
    pt = PrettyTable()
    pt._set_field_names("车次　车站　时间　经历时　一等座　二等座　软卧　硬卧 硬座　无座)".split())
    for raw_train in raw_trains:
        # split切割之后得到的是一个列表
        data_list = raw_train.split("|")
        content.setdefault(data_list[3],(data_list[0],data_list[2],data_list[3],data_list[12],data_list[15]))
        # print(data_list)
        train_no = data_list[3]
        initial = train_no[0].lower()
        # print(train_no[0])
        # 判断是否是查询特定车次的信息

        from_station_code = data_list[6]
        to_station_code = data_list[7]
        start_time = data_list[8]
        arrive_time = data_list[9]
        time_duration = data_list[10]
        first_class_seat = data_list[31] or "--"
        second_class_seat = data_list[30] or "--"
        soft_sleep = data_list[23] or "--"
        hard_sleep = data_list[28] or "--"
        hard_seat = data_list[29] or "--"
        no_seat = data_list[33] or "--"
        pt.add_row([
            train_no,
            '\n'.join([Fore.GREEN + station.get(from_station_code) + Fore.RESET,
                       Fore.RED + station.get(to_station_code) + Fore.RESET]),
            '\n'.join([Fore.GREEN + start_time + Fore.RESET, Fore.RED + arrive_time + Fore.RESET]),
            time_duration,
            first_class_seat,
            second_class_seat,
            soft_sleep,
            hard_sleep,
            hard_seat,
            no_seat,
        ])

    print(pt)
    return content

if __name__ == '__main__':
    cli()