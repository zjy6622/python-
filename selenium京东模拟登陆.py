# coding=gbk
#本来想用selenium登陆京东，利用CV2识别出距离后，却死在滑块拖动上，用了两个方法都没能过京东的识别（应该不是webdriver被识别导致的）
#第一种模拟滑动方法有几率成功，第一种在前两次都会成功，如果连续使用一种滑动方法会被识别就会被识别

from selenium import webdriver
import time
import base64
import cv2
import random
import numpy as np
from selenium.webdriver import ActionChains
from selenium.webdriver import ChromeOptions


def selenuim_moni():
    option = ChromeOptions()
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    brow=webdriver.Chrome(options=option)
    brow.get('https://passport.jd.com/new/login.aspx?')
    click1=brow.find_element_by_xpath('//*[@id="content"]/div[2]/div[1]/div/div[3]').click()
    name=brow.find_element_by_id('loginname').send_keys('name')
    passwd=brow.find_element_by_id('nloginpwd').send_keys('password')
    click2=brow.find_element_by_id('loginsubmit').click()
    time.sleep(2)
    button=brow.find_element_by_xpath('//*[@id="JDJRV-wrap-loginsubmit"]/div/div/div/div[2]/div[3]')
    bj=brow.find_element_by_xpath('//div[@class="JDJRV-bigimg"]/img')
    bjpng=bj.get_attribute('src')
    hk=brow.find_element_by_xpath('//div[@class="JDJRV-smallimg"]/img')
    hkpng=hk.get_attribute('src')
    distance=get_distance(bjpng,hkpng)
    get_tracks(brow,distance,button)
    time.sleep(10)
    brow.quit()


def get_distance(bj,hk):
    bj_base=bj.replace('data:image/png;base64,','')
    hk_base=hk.replace('data:image/png;base64,','')
    slider_body = base64.b64decode(hk_base)
    with open('hk.jpg','wb')as f:
        f.write(slider_body)
    background_body = base64.b64decode(bj_base)
    with open('bj.jpg','wb')as f:
        f.write(background_body)
    target = cv2.imread('hk.jpg', 0)
    template = cv2.imread('bj.jpg', 0)
    temp = 'temp.jpg'
    targ = 'targ.jpg'
    cv2.imwrite(temp, template)
    cv2.imwrite(targ, target)
    target = cv2.imread(targ)
    target = cv2.cvtColor(target, cv2.COLOR_BGR2GRAY)
    target = abs(255 - target)
    cv2.imwrite(targ, target)
    target = cv2.imread(targ)
    template = cv2.imread(temp)
    result = cv2.matchTemplate(target, template, cv2.TM_CCOEFF_NORMED)
    x, y = np.unravel_index(result.argmax(), result.shape)
    return y*(278/360)


def move_mouse(browser,distance,element):#第一种轨迹模拟方法（三段随机速度）成功几率高
    has_gone_dist=0
    remaining_dist = distance
    ActionChains(browser).click_and_hold(element).perform()
    time.sleep(0.5)
    while remaining_dist > 0:
        ratio = remaining_dist / distance
        if ratio < 0.1:
            span = random.randint(3, 5)
        elif ratio > 0.9:
            span = random.randint(5, 8)
        else:
            span = random.randint(15, 20)
        ActionChains(browser).move_by_offset(span, random.randint(-5, 5)).perform()
        remaining_dist -= span
        has_gone_dist += span
        time.sleep(random.randint(5, 20) / 100)
    ActionChains(browser).move_by_offset(remaining_dist, random.randint(-5, 5)).perform()
    ActionChains(browser).release(on_element=element).perform()

def get_tracks(browser,distance,element): #第二种轨迹模拟方法（先慢后快，最后反方向拖动，模仿人类行为）成功几率一般
    distance += 8
    v = 0
    t = 0.3
    forward_tracks = []
    current = 0
    mid = distance * 4 / 5
    while current < distance:
        if current < mid:
            a = 2
        else:
            a = -3
        v0 = v
        s = v0 * t + 0.5 * a * (t ** 2)
        current += s
        forward_tracks.append(round(s))
        v = v0 + a * t
    back_tracks = [-3, -2, -2, -1]
    ActionChains(browser).click_and_hold(element).perform()
    for x in forward_tracks:
        ActionChains(browser).move_by_offset(x, 0).perform()
    # for x in back_tracks:
    #     ActionChains(browser).move_by_offset(x, 0).perform()
    ActionChains(browser).release(on_element=element).perform()

if __name__=='__main__':
    pngdata=selenuim_moni()

