import logging
import time
import selenium
import json
import re

from selenium.webdriver.remote.webdriver import WebDriver as wd
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait as wdw
from selenium.webdriver.support import expected_conditions as EC

fmt = '%(asctime)s.%(msecs)03d [%(levelname)s] %(message)s'
datefmt = '%Y-%m-%d %H:%M:%S'
level = logging.INFO

formatter = logging.Formatter(fmt, datefmt)
logger = logging.getLogger()
logger.setLevel(level)

file = logging.FileHandler('twitter/twitter.log', encoding='utf-8')
file.setLevel(level)
file.setFormatter(formatter)
logger.addHandler(file)

console = logging.StreamHandler()
console.setLevel(level)
console.setFormatter(formatter)
logger.addHandler(console)


def get_page():
    """
    根据twitter/settings.txt下的搜索请求，在twitter站内进行搜索，将结果写入twitter/{query}.html
    利用selenium自动翻页到最底部
    :return:
    """

    # 手动操作登录twitter，有空了可能会补充自动登录吧
    driver = selenium.webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.get("https://twitter.com/home")

    with open("twitter/settings.txt", "r", encoding="utf-8") as f:
        query_list = json.load(f)['query']

    for query in query_list:

        # 先进行搜索
        search = driver.find_element(By.XPATH, "//input[@aria-label='Search query']")
        search.send_keys(query)
        time.sleep(2)
        search.send_keys(Keys.ENTER)
        time.sleep(10)
        pre_height = 0
        logger.info(f"start searching {query}")

        # 然后清除搜索框内的东西
        search = driver.find_element(By.XPATH, "//input[@aria-label='Search query']")
        search.click()
        time.sleep(1)
        btn = driver.find_element(By.XPATH, "//div[@data-testid='clearButton']")
        btn.click()
        time.sleep(1)

        while True:
            try:
                # 一直往下翻页！
                driver.execute_script("scrollBy(0, 10000)")
                time.sleep(20)

                # 获取最新的高度，如果最新高度等于原先的高度，认为已经结束这一页的爬取
                now_height = driver.execute_script("return document.documentElement.scrollHeight")
                if now_height == pre_height:
                    dates = re.findall('\d+-\d+-\d+', query)
                    date = dates[1] + '-to-' + dates[0]
                    with open(f"twitter/{date}.html", "w") as f:
                        f.write(driver.page_source)
                    logger.info(f'{query} finished!')
                    time.sleep(30)
                    break

                # 更新高度
                pre_height = now_height

            except Exception as e:
                logger.exception(e)


def login():
    """
    未完工，事实上实操的时候我是手动登录的
    真的太麻烦了，而且相比真实操作，自动操作浏览器会导向另一个界面?
    :return:
    """

    with open("twitter/settings.txt", "r", encoding='utf-8') as f:
        settings = json.load(f)

    # 登录界面啦
    driver = selenium.webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.get("https://twitter.com/i/flow/login")
    wdw(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//div[@class="css-901oao r-1awozwy r-6koalj r-18u37iz r-16y2uox r-37j5jr r-a023e6 r-b88u0q r-1777fci r-rjixqe r-bcqeeo r-q4m81j r-qvutc0"]')))
    time.sleep(1)

    # 输入账号
    email = driver.find_element(By.XPATH, "//input[@autocomplete='username']")
    email.send_keys(settings['email'])
    time.sleep(0.5)

    # 跳转，输入密码
    btn = driver.find_element(By.XPATH, '//div[@class="css-901oao r-1awozwy r-6koalj r-18u37iz r-16y2uox r-37j5jr r-a023e6 r-b88u0q r-1777fci r-rjixqe r-bcqeeo r-q4m81j r-qvutc0"]')
    btn.click()



