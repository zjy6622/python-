import hashlib,time
import requests
from lxml import etree
from concurrent import futures


def main():
	works=5
	with futures.ThreadPoolExecutor(works) as executor:
		to_do=[]
		for page in range(1,1001):
			future=executor.submit(get_data,page)
			to_do.append(future)
		results=0
		for fut in futures.as_completed(to_do):
			res=fut.result()
			print(res)
			results+=res
		print('-----end------')
		print(results)
		

def sha1(time):
	t=time
	tsha1=hashlib.sha1()
	keys='Xr0Z-javascript-obfuscation-1'+str(t)
	tsha1.update(keys.encode('utf-8'))
	res=tsha1.hexdigest()
	return res


def get_data(page):
	headers={
		'Accept': '*/*',
		'Accept-Encoding': 'gzip, deflate',
		'Accept-Language': 'zh-CN,zh;q=0.9',
		'Connection': 'keep-alive',
		'Cookie': '_ga=GA1.2.1629332843.1573102038; _gid=GA1.2.898906338.1573102038; Hm_lvt_020fbaad6104bcddd1db12d6b78812f6=1573193452,1573193786,1573262997,1573263015; footprints=eyJpdiI6ImlmMndHRUtmbjk3cjRxNzZ5R0hLK1E9PSIsInZhbHVlIjoiQkQ0c2RENmNTNmR6KzJyYStVY3pcLzZONjJUVVVESnh6SnRuUzV6dVhHdkJ1eEFpcTRDYlJCWmJ2RzNNQWRhS04iLCJtYWMiOiIwZjAxMDg0NjlkMDhmMjk1ZGU2YWFiNGE0OGUyNThjMzYwNzJhNTRjNjdiYzQ0YjM4Zjg0ZGJmYzI1ZDc0MmE4In0%3D; Hm_lpvt_020fbaad6104bcddd1db12d6b78812f6=1573273629; XSRF-TOKEN=eyJpdiI6InlUSVwvYllCMGU0UkZDc0E1dkY5NGdnPT0iLCJ2YWx1ZSI6Ik1VdnBMZkhsczM1YnU4S0VBTjlFRG1qckVjVVJFc0hnV01RVEVmY0pjY0Y3VzU3dFRNZXhQNWNRdmducTU5T24iLCJtYWMiOiJiZTVmODA2ZWIyZWJhZDQzYTRjZGJkN2ZmZTNiNjY5MWUyYWE0M2QzNTE1NGUwMzVmNDhmOTZiMzQ0YTNjYzA4In0%3D; glidedsky_session=eyJpdiI6ImsreUQ2Wm54YUI3UUl0bXFnSGRxK3c9PSIsInZhbHVlIjoibVwvcWtVck9vWmRHbGlWWVVpZmllRWt2M0VHUUM1Vm8rYXhlVkRjZ25neTJ6QjBWVDBwbEJsRTc2eExxMG1YZWQiLCJtYWMiOiI5MDc4MTFhNmUyMWZlNzdhZmY4ZjJjZDAwZGY5MzM4MDVkNzQ5ZDM1ZmIyZWZiYmJjZjMzYWYxNWU4ZWM3YWMzIn0%3D',
		'Host': 'www.glidedsky.com',
		'Referer': 'http://www.glidedsky.com/level/web/crawler-javascript-obfuscation-1?page=1',
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36',
		'X-Requested-With': 'XMLHttpRequest',
	}
	res=requests.get(url=f'http://www.glidedsky.com/level/web/crawler-javascript-obfuscation-1?page={page}',headers=headers)
	content=etree.HTML(res.text)
	time=content.xpath('//main[@class="py-4"]/div/@t')[0]
	t = int((int(time) - 99) / 99)
	params={
		'page':page,
		't':t,
		'sign':sha1(t),
	}
	resp=requests.get(url='http://www.glidedsky.com/api/level/web/crawler-javascript-obfuscation-1/items?',headers=headers,params=params)
	data=resp.json()
	dat=data.get('items')
	return sum(dat)
	
if __name__=='__main__':
	main()
