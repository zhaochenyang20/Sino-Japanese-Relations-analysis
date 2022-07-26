import json
import requests
import re
import random
import selenium
import time
import logging

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup as BS
from fake_useragent import UserAgent as ua


fmt = '%(asctime)s.%(msecs)03d [%(levelname)s] %(message)s'
datefmt = '%Y-%m-%d %H:%M:%S'
level = logging.INFO

formatter = logging.Formatter(fmt, datefmt)
logger = logging.getLogger()
logger.setLevel(level)

file = logging.FileHandler('jiia/jiia.log', encoding='utf-8')
file.setLevel(level)
file.setFormatter(formatter)
logger.addHandler(file)

console = logging.StreamHandler()
console.setLevel(level)
console.setFormatter(formatter)
logger.addHandler(console)


def get_url_from_google(keyword, page):

    """
    根据所给的keyword在google上搜索相应的结果，搜索将从第page页开始
    文件将写入crawler/jiia/url.txt中
    :param page: 希望开始的google搜索页面数
    :param keyword: 希望搜索的关键词
    :return:
    """

    with open("jiia/settings.txt", "r", encoding='utf-8') as f:
        settings = json.load(f)

    while True:  # 如果对自动化要求不是非常高可以改成for i in range(page, {谷歌搜索该关键词的总页数})

        headers = {
            "user-agent": ua(use_cache_server=False).random,
            "cookie": settings['cookie']
        }
        resp = requests.get(f"https://www.google.com.hk/search?q=site:www.jiia.or.jp/+{keyword}\
        &newwindow=1&ei=vVreYsr8IbqZkPIPmtiReA&start={page}0&sa=N&ved=2ahUKEwiKz9vg1ZP5AhW6DEQIHRpsBA84PBDy0wN6BAgBED8&biw=1323&bih=705&dpr=2",
        headers=headers)

        # 谷歌经常429，所以多休息休息！
        if resp.status_code != 200:
            logger.info(f"Response: {resp.status_code}")
            time.sleep(random.uniform(60, 120))
            continue

        # 查找href
        soup = BS(resp.text, 'lxml')
        href_list = list(map(lambda x: x['href'], soup.find_all("a", target="_blank")[0:20:2]))

        # 如果成功找到了
        if href_list:
            logger.info(f"{page} finished!")
            page += 1
            time.sleep(10)

        # 不确定是错误还是结束了所以输出text，并返回page，结束程序
        else:
            logger.info(f"{resp.text}")
            return page


def jiia_pdf_downloader():
    """
    利用selenium下载/jiia/url.txt下所有.pdf网页中的pdf文件，下载地址保存在jiia/settings.txt中
    函数中每次time.sleep(5)，但网页似乎并没有设防，如果太慢可以减小
    :return:
    """
    with open("jiia/settings.txt" "r", encoding='utf-8') as f:
        settings = json.load(f)

    with open("jiia/url.txt", "r") as f:
        url_list = f.read().split('\n')

    # 打开浏览器，设置下载地址和设置（自动下载pdf网页）
    options = webdriver.ChromeOptions()
    options.add_experimental_option('prefs', {
        "download.default_directory": settings['download_directory'],
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "plugins.always_open_pdf_externally": True
    })
    driver = selenium.webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

    for url in url_list:

        # avoid redundant visit!
        with open("jiia/written.txt", "r") as f:
            written_list = f.read().split()
        if url in written_list:
            continue

        # 只访问以.pdf结尾的网站
        data_type = re.findall("\.\w+", url)[-1]
        if data_type == '.pdf':
            driver.get(url)
            logger.info(f"getting pdf from{url}")
            time.sleep(5)
        else:
            continue


def jiia_html_downloader():

    with open("jiia/jiia.txt", "r") as f:
        url_list = f.read().split()

    for index, url in enumerate(url_list):

        # avoid redundant visit!
        with open("jiia/written.txt", "r") as f:
            written_list = f.read().split()
        if url in written_list:
            continue

        # 只访问不以.pdf结尾的网页
        data_type = re.findall("\.\w+", url)[-1]
        if data_type == '.pdf':
            continue
        else:
            try:
                resp = requests.get(url, headers={"user-agent": ua(use_cache_server=False).random})

                # 如果失败就多休息休息啦
                if resp.status_code != 200:
                    logger.info(f"Response: {resp.status_code}")
                    time.sleep(random.uniform(10, 50))
                    continue

                with open(f"res/{index}.html", "w") as f:
                    f.write(resp.text)

                with open("jiia/written.txt", "a+") as f:
                    f.write(url + '\n')

                logger.info(f"{index} - {url} written")
                time.sleep(5)

            except Exception as e:
                logger.info(e)
                time.sleep(random.uniform(10, 50))

