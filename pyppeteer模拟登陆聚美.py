# coding=gbk
import asyncio
from pyppeteer import launch
def screen_size():
    import tkinter
    tk = tkinter.Tk()
    width = tk.winfo_screenwidth()
    height = tk.winfo_screenheight()
    tk.quit()
    return width, height

async def main():
    js1 = '''() =>{
    
        Object.defineProperties(navigator,{
        webdriver:{
            get: () => false
            }
        })
    }'''
    browser = await launch({'headless': False, 'args': ['--no-sandbox'], })
    width, height = screen_size()
    page = await browser.newPage()
    await page.setViewport({
        "width":width,
        "height":height
    })
    await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36')
    await page.goto('https://passport.jumei.com/i/account/login')
    await page.evaluate(js1)                                   #执行js文件改变window.navigator.webdriver变量
    button2=await page.xpath('//*[@id="radio_normal"]')
    await button2[0].click()
    name=await page.xpath('//*[@id="username"]')
    pswd=await page.xpath('//*[@id="login_password"]')
    await name[0].type('name')                                 #账户名和密码
    await pswd[0].type('password')
    button1=await page.xpath('//*[@id="nc_1_n1z"]')
    await button1[0].click()
    await try_validation(page)
    button3=await page.xpath('//*[@id="login-user-form"]/input[3]')
    await asyncio.sleep(3)
    await button3[0].click()
    await asyncio.sleep(100)
    await browser.close()

async def try_validation(page, distance=300):
    distance1 = distance - 100
    distance2 = 100                                          #分别获取按钮的x，y坐标，高度和宽度
    btn_position = await page.evaluate('''                          
       () =>{
        return {
         x: document.querySelector('#nc_1_n1z').getBoundingClientRect().x,                  
         y: document.querySelector('#nc_1_n1z').getBoundingClientRect().y,
         width: document.querySelector('#nc_1_n1z').getBoundingClientRect().width,
         height: document.querySelector('#nc_1_n1z').getBoundingClientRect().height
         }}
        ''')
    x = btn_position['x'] + btn_position['width'] / 2
    y = btn_position['y'] + btn_position['height'] / 2
    await page.mouse.move(x, y)                             #调整鼠标位置
    await page.mouse.down()
    await page.mouse.move(x + distance1, y, {'steps': 100}) #steps可选参数控制速度
    await page.waitFor(800)
    await page.mouse.move(x + distance1 + distance2, y, {'steps': 200})
    await page.waitFor(800)
    await page.mouse.up()

asyncio.get_event_loop().run_until_complete(main())


#代码参考https://blog.csdn.net/qq393912540/article/details/91956136