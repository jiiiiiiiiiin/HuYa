import os
import time
import requests
from pathlib import Path
from PIL import Image

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class HuYa:
    def __init__(self, dri: webdriver.Chrome):
        self.url_userIndex = "https://i.huya.com/"
        self.driver = dri

    def login_check(self):

        # try to get huyaNum
        try:
            status = self.driver.execute_script('''return document.getElementById("huyaNum")''')
        except:
            status = None

        # check whether get huyaNum successfully
        if status != None:
            username = status.get_attribute("textContent")
            return True
        else:
            return False

    def get_qr(self, usn, url, attach_cookie=False):
        sess = requests.Session()
        # 将selenium的cookies放到session中, 虎牙的验证码不带cookie也能访问, 绝绝子
        if attach_cookie:
            cookies = self.driver.get_cookies()
            sess.headers.clear()
            for cookie in cookies:
                sess.cookies.set(cookie['name'], cookie['value'])

        ret = sess.get(url)
        with open('qr-{}.png'.format(usn), 'wb') as f:
            print("qr-code saved success.")
            f.write(ret.content)
            f.close()
            img = Image.open(f.name)
            img.show()

    def login(self, username, password):

        print("user:{} start to login.".format(username))

        # go to login page
        self.driver.get(self.url_userIndex)
        self.driver.implicitly_wait(2)  # 等待跳转

        # check whether user has logged in
        if self.login_check():
            print("user:{} has logged in.".format(username))
            return True

        # fill in username and password, and click login button
        self.driver.switch_to.frame('UDBSdkLgn_iframe')
        js = '''
            document.getElementsByClassName("udbstat on")[0].click();
            document.getElementsByClassName("udb-input-account")[0].value = "''' + str(username) + '''";
            document.getElementsByClassName("udb-input-pw")[0].value = "''' + str(password) + '''";
            document.getElementById("login-btn").click();
        '''
        self.driver.execute_script(js)
        self.driver.implicitly_wait(4)  # 等待跳转

        if not self.login_check():
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'qr-image')))
            qr_url = self.driver.execute_script('return document.getElementById("qr-image").src;')
            print('qr-code url:', qr_url)
            self.get_qr(username, qr_url)
            while not self.login_check():
                print(self.login_check())
                time.sleep(3)

    def into_room(self, room_id, send_hl):

        total_hl = int(self.get_hl())
        print("The remaining HL is {}".format(total_hl))
        if total_hl == 0 or send_hl <= 0:
            return False
        elif total_hl < send_hl:
            send_hl = total_hl

        print("Enter room:{}".format(room_id))

        self.driver.get("https://huya.com/{}".format(room_id))
        self.driver.implicitly_wait(3)  # 等待跳转
        time.sleep(5)

        self.driver.execute_script('''document.getElementsByClassName('player-face-arrow')[0].click()''')
        time.sleep(1)

        try_times = 10
        while True:

            gift_hl_id = self.driver.execute_script('''
                var gift_hl_id = 0;
                gifts = document.getElementsByClassName("gift-panel-item");
                for(var i=0;i<gifts.length;i++){
                    propsid = gifts[i].getAttribute("propsid");
                    if(propsid === "4"){
                        gift_hl_id = i;
                        break;
                    }
                }
                return gift_hl_id;
            ''')

            if gift_hl_id != 0:
                print("gift_hl_id", gift_hl_id)
                break

            if try_times == 0:
                print("room:{} send failure".format(room_id))
                return False
            else :
                try_times -= 1
                time.sleep(1)

        for i in range(send_hl):
            self.driver.execute_script('''
                gifts[''' + str(gift_hl_id) + '''].click();
                if(document.getElementsByClassName("btn confirm").length != 0){
                    document.getElementsByClassName("btn confirm")[0].click();
                }
            ''')
            print('Room:{} send out the {}th HL.'.format(room_id, i))
            time.sleep(1)

    def get_hl(self):
        # 进入充值页面查询虎粮
        self.driver.get("https://hd.huya.com/pay/index.html?source=web")
        self.driver.implicitly_wait(3)  # 等待跳转

        self.driver.execute_script('''document.getElementById("packTab").click();''')
        time.sleep(1)

        n = self.driver.execute_script('''
            var n = 0;
            lis = document.getElementsByTagName("li");
            for(var i=0;i<lis.length;i++){
                if(lis[i].title.search("个虎粮") != -1){
                    n = lis[i].getAttribute("data-num");
                    break;
                }
            }
            return n;
        ''')
        print("number of HL:{}".format(n))
        return n

if __name__ == '__main__':
    debug = False

    path_chrome_data = os.getcwd() + '/chromeData'
    if not Path(path_chrome_data).exists():
        os.mkdir(path_chrome_data)

    chrome_options = Options()
    chrome_options.add_argument(r'user-data-dir=' + path_chrome_data)
    if not debug:
        chrome_options.add_argument('--headless')  # 无头模式
        chrome_options.add_argument("--ignore-certificate-errors")  # 忽略证书错误
        chrome_options.add_argument("--disable-popup-blocking")  # 禁用弹出拦截
        chrome_options.add_argument("no-sandbox")  # 取消沙盒模式
        chrome_options.add_argument("no-default-browser-check")  # 禁止默认浏览器检查
        chrome_options.add_argument("disable-extensions")  # 禁用扩展
        chrome_options.add_argument("disable-glsl-translator")  # 禁用GLSL翻译
        chrome_options.add_argument("disable-translate")  # 禁用翻译
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--hide-scrollbars")  # 隐藏滚动条, 应对一些特殊页面
        chrome_options.add_argument("blink-settings=imagesEnabled=false")  # 不加载图片, 提升速度

    driver = webdriver.Chrome(options=chrome_options)

    hy = HuYa(driver)
    hy.login(username="", password="")
    hy.into_room(998, 50)

    driver.quit()
