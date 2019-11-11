import requests
from lxml import etree
import re
from concurrent import futures
def main():
	works=8
	with futures.ThreadPoolExecutor(works) as executor:
		to_do=[]
		for page in range(1,1001):
			urls=f'http://www.glidedsky.com/level/web/crawler-css-puzzle-1?page={page}'
			future=executor.submit(get_css,urls)
			to_do.append(future)
		results=[]
		for fut in futures.as_completed(to_do):
			res=fut.result()
			print(res)
			results.append(res)
		print('------end---------')
		print(sum(results))
		
def get_css(url):
    headers={
        'Cookie': '_ga=GA1.2.1629332843.1573102038; _gid=GA1.2.898906338.1573102038; Hm_lvt_020fbaad6104bcddd1db12d6b78812f6=1573102038,1573110161,1573177004; _gat_gtag_UA_75859356_3=1; footprints=eyJpdiI6ImIxbnVOaElMY2toS3h0WE9SVGhvcXc9PSIsInZhbHVlIjoiTE5haTNXd0RQVVwvMjFURElLWStvSWhYZXNha2s5T2dnZ2pTV0FiWWF1YnBCeFZ1Ymd1UlhURThPdWhCNHpTdVIiLCJtYWMiOiIwNzMzMTIxNmNhZWUxYTI2MDhkNzdmNmY3NDI1MjUxYzdmODU2YjQ0YTdiNDA2ZTcxNTA3NjY4N2IxMjliOTlmIn0%3D; XSRF-TOKEN=eyJpdiI6IjdVNXVVT1VRQUlseEZZNnIrSyt2Y0E9PSIsInZhbHVlIjoibVVjREJ0XC82b2t2eVlnNHlENGhaY2IyM3poNTNHTFlCa0xWZTRPRFRVZTlpWkpCbDFDN2ZzaTlWVU5YWUhKeFUiLCJtYWMiOiI4MTliMzYwMjZiMjBkMTE4YjA3OWYwN2UwZWViZWNlYjg4ODA5N2E3YTJjNDNiNWRiMjNlNTlkMzY2MmZjYWZmIn0%3D; glidedsky_session=eyJpdiI6Iitxait3ejBcL0d3ZlVNNVdXZTlnRnZnPT0iLCJ2YWx1ZSI6ImlUTmJCWlVzY1MyWXY5dHhEMFp4eE1SOHExZUYzSnVtK1lOK1pqK3lNUE5tMXBVWXZhTGNsODdXRjEyWndCbE8iLCJtYWMiOiIxMTgxZmQzOTQxMjIwNTE4YzVjYWQzOTdmMWIyYWY4NmVlOGRjNDllZjMwYTJiMGFmNmI1YWVkNzcxZDI4ZmRkIn0%3D; Hm_lpvt_020fbaad6104bcddd1db12d6b78812f6=1573177047',
        'Referer': 'http://www.glidedsky.com/level/web/crawler-basic-2?page=1',
    }
    resp=requests.get(url=url,headers=headers)
    data=etree.HTML(resp.text)
    dat=data.xpath('//div[@class="row"]/div')
    chars=[]
    for li in dat:
        key = True
        cop=li.xpath('./div/text()')
        clas=cop[:]
        cls=li.xpath('./div/@class')
        for n,i in enumerate(cls):
            res=finds(resp.text,i)
            if type(res) == type('s'):
                chars.append(int(res))
                key=False
                break
            else:
                if res==9:
                    cop.pop(n)
                    cop.insert(n,'')
                elif res==0:
                    continue
                else:
                    cop[n+res]=clas[n]
        if key:
            chars.append(int(''.join(cop)))
    print(chars)
    return sum(chars)

def finds(data,cs):
    dat=re.findall('<style>(.*?)</style>',data,re.S)[0]
    dats=re.findall('.*?(\..*?}).*?',dat,re.S)
    text=' '.join(dats)
    dat=''.join(re.findall('\.'+cs+' (\{ .*? \}?)',text,re.S))
    content=re.findall('\{ (.*?):.*? \}',dat)
    if content.count('margin-right')==0:
        if content.count('left')!=0:
            offset=re.findall('left:(.*?)em ',dat)[0]
            return int(offset)
        elif content.count('letter-spacing') != 0:
            offset = re.findall(f'\.{cs}:before.*?content:"(.*?)" ', text)[0]
            return offset
        else:
            return 0
    elif content.count('margin-right')!=0:
        return 9

	
if __name__=='__main__':
	main()
