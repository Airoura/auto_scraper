# Generated by Selenium IDE
import time
import os
import json
from tqdm import tqdm
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
# from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from browsermobproxy import Server



class Scraper():
    def __init__(self) -> None:
        self.p_data = None
        self.load_mbti_data()
        self.setup_method()
        
    def setup_method(self):
        self.server = Server(r'D:\Airoura\ProgramFiles\browsermob-proxy-2.1.4\bin\browsermob-proxy.bat')
        self.server.start()
        self.proxy = self.server.create_proxy()
       
        print('proxy', self.proxy.proxy)
        options = webdriver.ChromeOptions()
        options.binary_location = "C:\Program Files\Google\Chrome\Application\chrome.exe"
        # options.add_argument('--no-sandbox')
        # options.add_argument('--single-process')
        # options.add_argument('--disable-dev-shm-usage')
        # options.add_argument("--start-maximized")
        # options.add_argument('--auto-open-devtools-for-tabs')
        # options.add_argument('--log-level=2')
        # options.add_argument('--disable-features=IsolateOrigins,site-per-process')
        # options.add_argument("--ignore_ssl")
        # options.add_argument('--ignore-ssl-errors')
        # options.add_argument('--ignore-certificate-errors')
        # options.add_argument('--allow-insecure-localhost')
        # 关闭自动控制 blink 特征
        options.add_argument('--ignore-certificate-errors')
        
        proxy = 'localhost:10808'
        options.add_argument('--proxy-server=socks5://' + proxy)
        options.add_argument('--proxy-server={0}'.format(self.proxy.proxy))
        options.add_argument('--disable-blink-features=AutomationControlled')
        self.driver = webdriver.Edge(options=options)

    def teardown_method(self):
        self.driver.quit()

    def load_mbti_data(self):
        # 读取json文件
        with open('mbti.json', 'r') as file:
            self.p_data = json.load(file)
    
    def save_results(self, data):
        # 使用ensure_ascii=False确保非ASCII字符正确编码为UTF-8
        with open('result.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    
    
    def save_cookie(self):
        # 登录成功后，保存Cookies到一个变量
        cookies = self.driver.get_cookies()
        jsonCookies = json.dumps(cookies)
        with open('cookies.json', 'w') as f:
            f.write(jsonCookies)

    def load_cookie(self):
        with open('cookies.json', 'r', encoding='utf-8') as f:
            listCookies = json.loads(f.read())
            for cookie in listCookies:
                self.driver.add_cookie(cookie)
    def scrap_list_id(self, keyword):
        
            # element = WebDriverWait(self.driver, 10).until(
            #     EC.presence_of_element_located((By.CSS_SELECTOR, ".r-30o5oe"))
            # )
            # element.click()
            # self.driver.find_element(
            #     By.CSS_SELECTOR, ".r-1yadl64 > .css-146c3p1").click()
            # element.send_keys(keyword)
            # element.send_keys(Keys.ENTER)
            self.driver.get(f"https://x.com/search?q={keyword}&src=recent_search_click&f=list")
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, ".css-175oi2r:nth-child(2) > .css-175oi2r:nth-child(1) > .css-175oi2r:nth-child(1) > .css-175oi2r:nth-child(1) > .css-175oi2r:nth-child(1) > .css-175oi2r:nth-child(1) .css-175oi2r:nth-child(1) > .css-175oi2r:nth-child(1) .css-1jxf684:nth-child(1)"))
            )
            element.click()
            # element = WebDriverWait(self.driver, 10).until(
            #     EC.presence_of_element_located(
            #         (By.CSS_SELECTOR, ".css-175oi2r:nth-child(1) > .css-175oi2r:nth-child(1) > .css-175oi2r:nth-child(1) > .css-175oi2r:nth-child(1) > .css-175oi2r:nth-child(1) > .css-175oi2r:nth-child(1) > .css-175oi2r:nth-child(1) > .css-175oi2r:nth-child(1) > .css-146c3p1:nth-child(1) > .r-4qtqp9:nth-child(1)"))
            # )
            # 获取当前URL
            # 清空之前获取的请求信息
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, ".css-175oi2r:nth-child(1) > .css-146c3p1 > .css-1jxf684:nth-child(2) > .css-1jxf684"))
            )
            self.proxy.new_har("douyin", options={'captureHeaders': True, 'captureContent': True})
            element.click()
            current_url = self.driver.current_url

            result = self.proxy.har
            print(result)
            # for entry in result['log']['entries']:
            #     _url = entry['request']['url']
            #     print(_url)
            #     # 根据URL找到数据接口
            #     # if "/api/v2/aweme/post" in _url:
            #     #     _response = entry['response']
            #     #     _content = _response['content']['text']
            #     #     # 获取接口返回内容
            #     #     print(_content)
            return current_url

            
    def login(self):
        if os.path.exists("cookies.json"):
            # 导航到登录页面
            self.driver.get("https://x.com/login")
            self.load_cookie()
        else:
            # 导航到登录页面
            self.driver.get("https://x.com/login")
            # 等待足够的时间，以便手动登录
            input("请登录后按Enter键继续...")
            self.save_cookie()
        self.driver.set_window_size(1512, 833)

    def scrap(self):
        self.login()
        results = {}
        for mbti_dic in tqdm(self.p_data[:1]):
            for mbti, keywords in mbti_dic.items():
                results[mbti] = {}
                for keyword in keywords:
                    url = self.scrap_list_id(keyword)
                    if url:
                        list_id = url.split("/")[-1]
                    else:
                        list_id = ""
                    results[mbti][keyword] = {
                        "url": url,
                        "id": list_id
                    }
                    time.sleep(30)
        self.save_results(results)
        
if __name__ == '__main__':
    sc = Scraper()
    sc.scrap()
