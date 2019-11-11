import base64
from fontTools.ttLib import TTFont
import requests
from lxml import etree
import re


def base(strs, name):
    num_dict = {
        '0': 'zero',
        '1': 'one',
        '2': 'two',
        '3': 'three',
        '4': 'four',
        '5': 'five',
        '6': 'six',
        '7': 'seven',
        '8': 'eight',
        '9': 'nine',
    }
    find_dict = {'nine': 0, 'eight': 1, 'seven': 2, 'two': 3, 'five': 4, 'three': 5, 'zero': 6, 'one': 7, 'six': 8,
                 'four': 9}  # font1中的编码值对应
    jm = base64.b64decode(strs)
    with open('fonts.tff', 'wb')as f:
        f.write(jm)
    font = TTFont('fonts.tff')
    font1 = TTFont('font.tff')
    font1_name = font1.getGlyphOrder()[1:]
    font_name = font.getGlyphOrder()[1:]
    data = []
    for i in name:
        ky = num_dict[i]
        objs = font['glyf'][ky]
        for n in font1_name:
            obj1 = font1['glyf'][n]
            if obj1 == objs:
                # print(name+':'+str(find_dict[n]))
                data.append(str(find_dict[n]))
    return ''.join(data)


def get_html(url):
    print('ok')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36',
        'Cookie': '_ga=GA1.2.1629332843.1573102038; _gid=GA1.2.898906338.1573102038; Hm_lvt_020fbaad6104bcddd1db12d6b78812f6=1573193452,1573193786,1573262997,1573263015; footprints=eyJpdiI6ImlmMndHRUtmbjk3cjRxNzZ5R0hLK1E9PSIsInZhbHVlIjoiQkQ0c2RENmNTNmR6KzJyYStVY3pcLzZONjJUVVVESnh6SnRuUzV6dVhHdkJ1eEFpcTRDYlJCWmJ2RzNNQWRhS04iLCJtYWMiOiIwZjAxMDg0NjlkMDhmMjk1ZGU2YWFiNGE0OGUyNThjMzYwNzJhNTRjNjdiYzQ0YjM4Zjg0ZGJmYzI1ZDc0MmE4In0%3D; Hm_lpvt_020fbaad6104bcddd1db12d6b78812f6=1573273629; XSRF-TOKEN=eyJpdiI6InlUSVwvYllCMGU0UkZDc0E1dkY5NGdnPT0iLCJ2YWx1ZSI6Ik1VdnBMZkhsczM1YnU4S0VBTjlFRG1qckVjVVJFc0hnV01RVEVmY0pjY0Y3VzU3dFRNZXhQNWNRdmducTU5T24iLCJtYWMiOiJiZTVmODA2ZWIyZWJhZDQzYTRjZGJkN2ZmZTNiNjY5MWUyYWE0M2QzNTE1NGUwMzVmNDhmOTZiMzQ0YTNjYzA4In0%3D; glidedsky_session=eyJpdiI6ImsreUQ2Wm54YUI3UUl0bXFnSGRxK3c9PSIsInZhbHVlIjoibVwvcWtVck9vWmRHbGlWWVVpZmllRWt2M0VHUUM1Vm8rYXhlVkRjZ25neTJ6QjBWVDBwbEJsRTc2eExxMG1YZWQiLCJtYWMiOiI5MDc4MTFhNmUyMWZlNzdhZmY4ZjJjZDAwZGY5MzM4MDVkNzQ5ZDM1ZmIyZWZiYmJjZjMzYWYxNWU4ZWM3YWMzIn0%3D',
		'Referer': 'http://www.glidedsky.com/level/web/crawler-basic-2?page=1',
    }
    resp = requests.get(url=url, headers=headers)
    strs = re.findall(';base64,(.*?=)', resp.text, re.S)[0]
    data = etree.HTML(resp.text)
    li = data.xpath('//div[@class="row"]/div')
    lists = []
    for i in li:
        num = re.search('\d+', i.xpath('./text()')[0], re.S).group()
        name = list(str(num))
        numbers = base(strs, name)
        lists.append(int(numbers))
    print(sum(lists))
    return sum(lists)
    
    
if __name__ == '__main__':
    res = []
    for page in range(1, 1001):
        url = f'http://www.glidedsky.com/level/web/crawler-font-puzzle-1?page={page}'
        print('page:'+str(page))
        data = get_html(url)
        res.append(data)
    print(sum(res))

		
