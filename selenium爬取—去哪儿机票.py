from selenium import webdriver
from selenium.webdriver import ChromeOptions
import time
import re
contents=[]
def jipiao():
    url='https://flight.qunar.com/'
    option=ChromeOptions()
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    driver=webdriver.Chrome(options=option)
    driver.get(url)
    chufa=driver.find_element_by_xpath('//*[@id="dfsForm"]/div[2]/div[1]/div/input')
    chufa.clear()
    chufa.send_keys('合肥')
    time.sleep(2)
    daoda=driver.find_element_by_xpath('//input[@name="toCity"]')
    daoda.clear()
    daoda.send_keys('重庆')
    time.sleep(2)
    times=driver.find_element_by_xpath('//*[@id="fromDate"]')
    times.clear()
    times.send_keys('2019-10-23')
    click1=driver.find_element_by_xpath('//*[@id="dfsForm"]/div[4]/button')
    click1.click()
    driver.implicitly_wait(3)
    while True:
        data=driver.find_elements_by_xpath('//div[@class="b-airfly"]')
        js = 'window.scrollBy(0, 8000)'
        driver.execute_script(js)
        for i in data:
            company=i.find_elements_by_xpath('.//div[@class="air"]/span')
            airnum = i.find_elements_by_xpath('.//div[@class="num"]/span[1]')
            airs=i.find_elements_by_xpath('.//div[@class="num"]/span[2]')
            stime=i.find_elements_by_xpath('.//div[@class="sep-lf"]/h2')[0]
            atime=i.find_elements_by_xpath('.//div[@class="sep-rt"]/h2')[0]
            ctime=i.find_elements_by_xpath('.//div[@class="range"]')[0]
            splane=i.find_elements_by_xpath('.//div[@class="sep-lf"]//p[@class="airport"]/span[1]')[0]
            aplane=i.find_elements_by_xpath('.//div[@class="sep-rt"]//p[@class="airport"]/span[1]')[0]
            if len(company) > 1:
                aircompany=company[0].text+'  '+company[1].text
                airnums=airnum[0].text+'  '+airnum[1].text
                airss=airs[0].text+'  '+airs[1].text
            else:
                aircompany=company[0].text
                airnums=airnum[0].text
                airss=airs[0].text
            price1=i.find_elements_by_xpath('.//em/b')
            price=jishuan(price1)
            content='航空公司：'+aircompany+'  航班号：'+airnums+'  '+airss+'\n起飞时间：'+stime.text+'  到达时间：'+atime.text+'  总航时：'+ctime.text+'\n起飞机场：'+splane.text+'  降落机场：'+aplane.text+'\n票价：'+price+'\n'+'='*10
            contents.append(content)
            print('ok')
        try:
            pagenext = driver.find_elements_by_xpath('//div[@class="container"]/a[@class="page-link"]')
            if len(pagenext) == 2:
                pagenext = driver.find_elements_by_xpath('//div[@class="container"]/a[@class="page-link"]')[1]
                print(pagenext.text)
                pagenext.click()
                time.sleep(2)
            else:
                sb=driver.find_elements_by_xpath('//em[@class="page-link page-link-disabled"]')[0]
                if sb.text == '上一页':
                    pagenext = driver.find_elements_by_xpath('//div[@class="container"]/a[@class="page-link"]')[0]
                    print(pagenext.text)
                    pagenext.click()
                    time.sleep(2)
                else:
                    break
        except Exception as e:
            print(e)
            break
    driver.quit()
    return contents

def jishuan(num):
    base=num[0].text
    lists=[]
    for i in base:
        lists.append(i)
    a=0
    while a < len(num)-1:
        a+=1
        key=num[a].get_attribute('style')
        basenum = re.search('left: -(.*?)px', key).group(1)
        res=-int(int(basenum)/16)
        lists[res]=num[a].text
    return ''.join(lists)


if __name__=='__main__':
    for i in jipiao():
        print(i)
