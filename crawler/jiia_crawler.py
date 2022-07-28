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
    根据所给的 keyword 在 google 上搜索相应的结果，搜索将从第 page 页开始
    文件将写入 crawler/jiia/url.txt 中
    :param page: 希望开始的 google 搜索页面数
    :param keyword: 希望搜索的关键词
    :return:
    """
    with open("jiia/settings.txt", "r") as f:
        settings = json.load(f)

    while True:  # 也可以改成改成for i in range( page , {谷歌搜索该关键词的总页数})

        headers = {
            # 注意这里不能使用 ua(use_cache_server=False).random! 否则返回的结果和预期的会不一样！
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko)\
             Chrome/103.0.0.0 Safari/537.36",
            "cookie": settings['cookie']
        }
        resp = requests.get(f"https://www.google.com.hk/search?q=site:www.jiia.or.jp+{keyword}\
        &newwindow=1&ei=j6TiYsr3FoyemAWM8YjADw&start={page}0&sa=N&ved=2ahUKEwiK-_Lb7Jv5AhUMD6YKHYw4Avg4ChDy0wN6BAgBEDc&biw=568&bih=701&dpr=2",
                            headers=headers)

        # 谷歌经常 429，所以多休息休息！
        if resp.status_code != 200:
            logger.info(f"Response: {resp.status_code}")
            time.sleep(random.uniform(60, 120))
            continue

        # 查找 href
        soup = BS(resp.text, 'lxml')
        href_list = set(map(lambda x: x['href'],
                            filter(lambda x: 'class' not in x.attrs,
                                   soup.find_all("a", target="_blank")
                                   )
                            )
                        )

        # 如果成功找到了
        if href_list:
            logger.info(f"{page} finished!")
            with open("jiia/url.txt", "a+") as f:
                f.write("\n".join(href_list) + '\n')
            logger.info("finished: \n" + '\n'.join(href_list))
            page += 1
            time.sleep(10)

        # 不确定是错误还是结束了所以输出 text ，并返回 page ，结束程序
        else:
            logger.info(f"{resp.text}")
            return page


def jiia_pdf_downloader():
    """
    利用 selenium 下载 /jiia/url.txt 下所有 .pdf 网页中的 pdf 文件，下载地址保存在 jiia/settings.txt 中
    函数中每次time.sleep(5)，但网页似乎并没有设防，如果觉得太慢可以减小
    :return:
    """
    with open("jiia/settings.txt", "r", encoding='utf-8') as f:
        settings = json.load(f)

    with open("jiia/url.txt", "r") as f:
        url_list = f.read().split('\n')

    # 打开浏览器，设置下载地址和设置（自动下载 pdf 网页）
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
            logger.info(f"getting pdf from {url}")
            with open("jiia/written.txt", "a+", encoding='utf-8') as f:
                f.write(url + '\n')
            time.sleep(5)


def jiia_html_downloader():
    with open("jiia/jiia.txt", "r") as f:
        url_list = f.read().split()

    for index, url in enumerate(url_list):

        # avoid redundant visit!
        with open("jiia/written.txt", "r") as f:
            written_list = f.read().split()
        if url in written_list:
            continue

        # 只访问不以 .pdf 结尾的网页
        data_type = re.findall("\.\w+", url)[-1]
        if data_type == '.pdf':
            continue
        else:
            try:
                resp = requests.get(url, headers={"user-agent": ua(use_cache_server=False).random})
                logger.info(f"getting {url}")

                # 如果失败就多休息休息啦
                if resp.status_code != 200:
                    logger.info(f"Response: {resp.status_code}")
                    time.sleep(random.uniform(10, 50))
                    continue

                # 日语可能出现乱码
                resp.encoding = 'utf-8'

                with open(f"jiia/{index}.html", "w") as f:
                    f.write(resp.text)

                with open("jiia/written.txt", "a+") as f:
                    f.write(url + '\n')

                logger.info(f"{index} - {url} written")
                time.sleep(10)

            except Exception as e:
                logger.info(e)
                time.sleep(random.uniform(10, 50))

