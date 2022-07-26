import json
import requests
import re
import random
import time
import logging

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


def get_url(target):

    """
    根据target查找搜索结果
    :param target: 搜索关键词
    :return:
    """

    page = 1

    while True:
        resp = requests.get(
            f"https://search.tianya.cn/bbs?q={target}&pn={page}",
            headers= {"user-agent": ua(use_cache_server=False).random}
        )

        logger.info(f"Headers: {resp.headers}")
        logger.info(f"searching for https://search.tianya.cn/bbs?q={target}&pn={page}")

        # 当status_code为500，说明已经没有更多内容了
        if resp.status_code == 500:
            logger.info("stop searching")
            break

        # extract and parse content
        soup = BS(resp.text, 'lxml')
        headings = soup.find_all("h3")
        links = list(map(lambda x: x.contents[0]['href'], headings))

        # 搜索有可能失败，所以反复尝试;尝试成功进入下一页，否则反复尝试该页
        time.sleep(10)
        if links:
            logger.info(f"page{page} succeeded")
            page += 1
            with open("tianya/url.txt", "a+") as f:
                f.write('\n'.join(links) + '\n')

def get_page():
    """
    根据url访问页面并保存网页源码
    天涯不设防，非常难出错
    :return:
    """
    with open("tianya/url.txt", "r") as f:
        url_list = f.read().split()

    for index, url in enumerate(url_list):
        try:
            resp = requests.get(url, headers={"user-agent": ua(use_cache_server=False).random})
            logger.info(f"searching for {url}")

            if resp.status_code == 200:
                with open(f"./tianya/{index}.html", "w") as f:
                    f.write(resp.text)
                logger.info(f"{index} written")
                time.sleep(5)

            else:
                logger.info(f"status: {resp.status_code}")
                time.sleep(random.uniform(10, 50))

        except Exception as e:
            logger.exception(e)

