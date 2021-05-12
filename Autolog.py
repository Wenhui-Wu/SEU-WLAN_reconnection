import os
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import requests
import ctypes

username_str = "一卡通号"
password_str = "密码"

class Login: 

    #WLAN热点连接函数
    #返回值：True-连接成功；False-连接失败
    def reconnect(self):
        os.system('netsh wlan disconnect')
        time.sleep(3)
        try:
            os.system("netsh wlan connect name=%s" % 'seu-wlan')
            time.sleep(3)
            return True
        except:
            print(self.getCurrentTime(),'(；´・∀・)没能连接上seu-wlan')
            return False

    #注销再登陆函数
    #返回值：True-登录成功；Flase-登录失败
    def login(self):
        try:
            driver = webdriver.Chrome()
            driver.get("https://w.seu.edu.cn/")
            time.sleep(3)
        except:
            print(self.getCurrentTime(),'(；´・∀・)浏览器调用出错了')
            driver.close()
            return False
        
        try:
            logout_button = driver.find_element_by_id("logout")
            logout_button.click()
            print(self.getCurrentTime(),u'(●´∀`●)注销成功~')
            time.sleep(3)
        except:
            print(self.getCurrentTime(),u'(●´∀`●)还没登录哦~')
        try:
            username_input = driver.find_element_by_id("username")
            password_input = driver.find_element_by_id("password")
            login_button = driver.find_element_by_id("login")
        except:
            print(self.getCurrentTime(),u'(；´・∀・)登陆界面打不开诶……')
            driver.close()
            return False

        username_input.send_keys(username_str)
        password_input.send_keys(password_str)
        login_button.click()
        time.sleep(3)

        try:
            logout_button = driver.find_element_by_id("logout")
            print(self.getCurrentTime(),u'(●´∀`●)登陆成功~')
            driver.close()
            return True
        except:
            print(self.getCurrentTime(),u'(；´・∀・)登陆账号或密码错误……')
            driver.close()
            return False

    #获取当前时间
    def getCurrentTime(self):
        return time.strftime('[%Y-%m-%d %H:%M:%S]',time.localtime(time.time()))

    #判断联网
    #返回值：3-墙外；2-墙内；1-仅seu；0-都不行
    def canConnect(self):
        flag=0
        try:
            baidu_request=requests.get("http://www.baidu.com")
            if(baidu_request.status_code==200):
                baidu_request.encoding = 'utf-8'
                baidu_request_bsObj = BeautifulSoup(baidu_request.text, 'html.parser')
                baidu_input = baidu_request_bsObj.find(value="百度一下")
                if baidu_input!=None:
                    flag=1
        except:
            pass

        if flag==1:
            try:
                requests.get("http://www.google.com")
                return 3
            except:
                return 2
        else:
            try:
                requests.get("http://w.seu.edu.cn")
                return 1
            except:
                return 0

    #主函数
    def main(self):
        print (self.getCurrentTime(), u"(●´(ｴ)`●)你的WiFi已经被俺承包了")
        
        '''
        whnd = ctypes.windll.kernel32.GetConsoleWindow()  
        if whnd != 0:  
            ctypes.windll.user32.ShowWindow(whnd, 0)  
            ctypes.windll.kernel32.CloseHandle(whnd)
        '''
        
        while True:
            status = self.canConnect()
            if status == 3:
                print(self.getCurrentTime(), u"(●´∀`●)一切正常嘿嘿嘿~")
                #time.sleep(5)
                continue
            if status == 2:
                print(self.getCurrentTime(), u"(●´∀`●)一切正常哦~")
                #time.sleep(5)
                continue
            if status == 1:
                if not self.login():
                    continue
                if self.canConnect()>=2:
                    print(self.getCurrentTime(), u"(●´∀`●)重连成功辣！")
                    #time.sleep(3)
                    continue
                else:
                    print(self.getCurrentTime(), u"Σ(゜ロ゜)重连失败了！")
                    continue
            if status == 0:
                if not self.reconnect():
                    continue
                if self.canConnect()>=2:
                    print(self.getCurrentTime(), u"(●´∀`●)重连成功~")
                    #time.sleep(3)
                    continue

                if not self.login():
                    continue
                if self.canConnect()>=2:
                    print(self.getCurrentTime(), u"(●´∀`●)重连成功~")
                    #time.sleep(3)
                    continue
                else:
                    print(self.getCurrentTime(), u"Σ(゜ロ゜)重连失败了！")
                    continue
                
login = Login()
login.main()

#参考文献
'''
ppingfann：python爬虫——校园网自动重连脚本
https://blog.csdn.net/hty46565/article/details/72822447

light_jiang2016：python 自动重连wifi windows
https://blog.csdn.net/light_jiang2016/article/details/52474322

zcy0xy：拒绝掉线！利用selenium实现校园网自动重连
https://blog.csdn.net/zcy0xy/article/details/78675334

shootercheng：Python wifi掉线重连接
https://www.cnblogs.com/shootercheng/p/6279666.html

agentfitz：python爬虫---requests库的用法
https://www.cnblogs.com/mzc1997/p/7813801.html

王小涛_同學：Python3.4 控制台窗口隐藏
https://blog.csdn.net/u013511642/article/details/43908999
'''
