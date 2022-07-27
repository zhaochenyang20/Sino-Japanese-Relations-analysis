import time
import logging

from selenium.webdriver.remote.webdriver import WebDriver as wd
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wdw
from selenium.webdriver.support import expected_conditions as EC
import selenium
import json


fmt = '%(asctime)s.%(msecs)03d [%(levelname)s] %(message)s'
datefmt = '%Y-%m-%d %H:%M:%S'
level = logging.INFO

formatter = logging.Formatter(fmt, datefmt)
logger = logging.getLogger()
logger.setLevel(level)

file = logging.FileHandler('facebook/facebook.log', encoding='utf-8')
file.setLevel(level)
file.setFormatter(formatter)
logger.addHandler(file)

console = logging.StreamHandler()
console.setLevel(level)
console.setFormatter(formatter)
logger.addHandler(console)


class FacebookCrawler:
    def __init__(self):
        with open("facebook/settings.txt", "r", encoding='utf-8') as f:
            self.settings = json.load(f)
        logger.info("Settings loaded")
        self.driver = None

    def login(self):
        """
        登入 facebook
        :return:
        """
        # open chrome
        driver = selenium.webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        self.driver = driver

        driver.get("https://www.facebook.com")
        wdw(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//button[@name='login']")))
        logger.info("visiting https://www.facebook.com")
        time.sleep(0.5)

        # fill in email and password

        email = driver.find_element(By.XPATH, "//input[@name='email']")
        passwd = driver.find_element(By.XPATH, "//input[@type='password']")

        email.send_keys(self.settings['email'])
        passwd.send_keys(self.settings['password'])

        # login
        login_btn = driver.find_element(By.XPATH, "//button[@name='login']")
        login_btn.click()
        logger.info("logging in...")
        time.sleep(10)

    def get_information(self):
        """
        搜索 facebook 信息
        注意：请手动搜索
        :return:
        """
        driver = self.driver

        # !!!此处请手动搜索!!!操作太麻烦了!!!

        page = 1
        prev_height = 0
        while True:
            try:
                driver.execute_script("scrollBy(0, 3500)")
                logger.info("begin scrolling...")
                time.sleep(1)
                now_height = driver.execute_script("return document.documentElement.scrollHeight")

                # 如果滑动到页面地步，那么就停止
                # 注意!!!如果你滑走页面的话这里可能有 bug !!!可能会不滑动到底部就停下
                if prev_height == now_height:
                    logger.info("finish crawling!!")
                    break

                if page % 5 == 0:
                    with open(f"res/{page // 10}.html", "w") as f:
                        f.write(driver.page_source)

                page += 1
                logger.info(f"the {page}th page finished")
                prev_height = now_height
                time.sleep(20)

            except Exception as e:
                print(str(e))