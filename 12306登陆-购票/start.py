from get12306 import dl_12306

name=input('输入用户名：')
password=input('输入密码：')
data=input('输入需购票日期（例：2019-10-01）：')
fromstation=input('输入出发城市：')
tostation=input('输入到达城市：')

op=dl_12306(name,password,data,fromstation,tostation)
op.main()
