import asyncio
from pyppeteer import launch
def screen_size():
    import tkinter
    tk=tkinter.Tk()
    width=tk.winfo_screenwidth()
    height=tk.winfo_screenheight()
    tk.quit()
    return width,height
async def main():
    js1 = '''() =>{

        Object.defineProperties(navigator,{
        webdriver:{
            get: () => false
            }
        })
    }'''
    browser = await launch(headless= False,args=['--no-sandbox'])
    page=await browser.newPage()
    width, height = screen_size()
    await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36')
    await page.setViewport({
        "width":width,
        "height":height,
    })
    await page.goto('https://login.taobao.com/member/login.jhtml')
    button1=await page.xpath('//*[@id="J_QRCodeLogin"]/div[5]/a[1]')
    await button1[0].click()
    name=await page.xpath('//*[@id="J_Form"]/div[2]/span')
    await name[0].type('tb39981237')
    await asyncio.sleep(1)
    passwd=await page.xpath('//*[@id="TPL_password_1"]')
    await passwd[0].type('zjy19970927.')
    await page.evaluateOnNewDocument(js1)                #执行js重写webdriver属性，无视页面刷新跳转
    await asyncio.sleep(3)
    await try_validation(page)
    await asyncio.sleep(1)
    button2=await page.xpath('//*[@id="J_SubmitStatic"]')
    await button2[0].click()
    await asyncio.sleep(100)


async def try_validation(page, distance=300):
    distance1 = distance
    # distance2 = 100                                    #分别获取按钮的x，y坐标，高度和宽度
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
    await page.mouse.move(x + distance1, y, {'steps': 35}) #尝试后发现，如果滑块速度很快的滑动有几率成功
    await page.waitFor(800)
    await page.mouse.up()
asyncio.get_event_loop().run_until_complete(main())