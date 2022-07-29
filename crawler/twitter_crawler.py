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


def login():
    """
    登录 https://twitter.com/home
    请将账号和密码分别写在 twitter/settings.json 下的 'username' 和 'password' 中
    :return: driver 模拟浏览器
    """

    with open("twitter/settings.json", "r", encoding='utf-8') as f:
        settings = json.load(f)

    # 登录界面
    driver = selenium.webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.get("https://twitter.com/home")
    wdw(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//input[@autocomplete='username']")))
    logger.info('begin logging in')
    time.sleep(1)

    # 输入账号，并跳转
    username = driver.find_element(By.XPATH, "//input[@autocomplete='username']")
    username.send_keys(settings['username'])
    logger.info('sending username')
    btn = driver.find_element(By.XPATH, '//div[@class="css-901oao r-1awozwy r-6koalj r-18u37iz r-16y2uox r-37j5jr r-a023e6 r-b88u0q r-1777fci r-rjixqe r-bcqeeo r-q4m81j r-qvutc0"]')
    btn.click()

    # 输入密码，并跳转
    time.sleep(3)
    wdw(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//input[@name='password']")))
    passwd = driver.find_element(By.XPATH, "//input[@name='password']")
    passwd.send_keys(settings['password'])
    logger.info('sending password')
    btn = driver.find_element(By.XPATH, '//div[@class="css-901oao r-1awozwy r-6koalj r-18u37iz r-16y2uox r-37j5jr r-a023e6 r-b88u0q r-1777fci r-rjixqe r-bcqeeo r-q4m81j r-qvutc0"]')
    btn.click()
    wdw(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//input[@aria-label='Search query']")))

    return driver


def get_page(driver):
    """
    根据 twitter/settings.json 下的搜索关键词('query' 属性)，在 twitter 站内进行搜索，将结果写入 twitter/{date}.html
    query 格式: {keyword} until: 2012-10-01 since: 2012-09-01
    :param driver 浏览器
    :return:
    """

    with open("twitter/settings.json", "r", encoding="utf-8") as f:
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
                driver.execute_script("scrollBy(0, 3000)")
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


def main():
    get_page(login())


if __name__ == '__main__':
    main()
