from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time, json, os, threading

class Vmall():
    def __init__(self):
        # 默认链接
        self.driver_path = 'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe'
        self.url = 'https://www.vmall.com/product/10086726905036.html'
        self.product_choose = '#pro-skus > dl.product-choose.clearfix.product-choosepic > div > ul > li.attr4.attr19.attr34'
        self.product_purchase = '#pro-operation > a:nth-child(2)'

    def addLogin(self,name):
        # 增加登录的cookies 登录账号
        driver = webdriver.Chrome(executable_path=self.driver_path)
        driver.get(self.url)
        # 获取cookie并通过json模块将dict转化成str
        input(f'账号:{name} 请在网页登录,成功后回车:')
        dictCookies = driver.get_cookies()
        jsonCookies = json.dumps(dictCookies)
        # 登录完成后将cookie保存到本地
        print('获取cookies成功!')
        with open(f'.cookies/{name}.json', 'w') as f:
            f.write(jsonCookies)
        driver.close()

    def start(self,name):
        # 创建浏览器
        driver = webdriver.Chrome(executable_path=self.driver_path)
        # 超时
        driver.set_page_load_timeout(5000)
        # 访问一次,不然容易设置不了cookies
        driver.get(self.url)
        # 删除第一次建立连接时的cookie
        driver.delete_all_cookies()
        # 读取登录时存储到本地的cookie
        with open(f'.cookies/{name}.json', 'r', encoding='utf-8') as f:
            listCookies = json.loads(f.read())
        for cookie in listCookies:
            #driver.delete_cookie(cookie['name'])
            driver.add_cookie({
                "domain": cookie['domain'],
                "httpOnly": cookie['httpOnly'],
                "name": cookie['name'],
                "path": cookie['path'],
                "secure": cookie['secure'],
                "value": cookie['value']
            })
        driver.get(self.url)
        # 自动选规格尺寸 默认白色
        self.selector = self.product_choose
        print(f'账号:{name} 选规格尺寸....目标按钮:{driver.find_element_by_css_selector(self.selector).text}')
        try:
            elem = driver.find_element_by_css_selector(self.selector)
            elem.click()
        except:
            pass
        input(f'账号:{name} 选规格尺寸信息,并回车(可能会多次):\n')

        self.selector = self.product_purchase
        print(f'账号:{name} 开始干活....目标按钮:{driver.find_element_by_css_selector(self.selector).text}')
        while True:
            #print('目标按钮:{driver.find_element_by_css_selector(self.selector).text}')
            try:
                elem = driver.find_element_by_css_selector(self.selector)
                elem.click()
            except:
                break
            time.sleep(0.1)
        # 没买到过 后续判断等一个有缘人来写
        input(f'账号:{name} 点击成功!是否抢到请自己看!')
        driver.close()

if __name__ == '__main__':
    print('本工具会自动拼命的点购买按钮 \n默认抢 华为 Mate40 Pro')
    hw = Vmall()
    while True:
        key=input('选择功能: 1.增加账号 2.开始拼命抢购 \n')
        if key=='1':
            name = input('输入本次登录帐号的备注(请勿重复):\n')
            hw.addLogin(name)
        elif key=='2':
            t=[]
            for item in os.listdir(path='.cookies', ):
                # 多线程
                if item.endswith('.json'):
                    t.append(threading.Thread(target=hw.start,args=(item.split('.')[0],)))
                    t[-1].setDaemon(True)
                    t[-1].start()
            for item in t:
                item.join()
            break
        else:
            print('输入有误或者已经退出!')
            continue
