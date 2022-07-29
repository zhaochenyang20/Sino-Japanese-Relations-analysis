import requests
import logging
import time
import json
import random
import re

from bs4 import BeautifulSoup as BS
from fake_useragent import UserAgent as ua

fmt = '%(asctime)s.%(msecs)03d [%(levelname)s] %(message)s'
datefmt = '%Y-%m-%d %H:%M:%S'
level = logging.INFO

formatter = logging.Formatter(fmt, datefmt)
logger = logging.getLogger()
logger.setLevel(level)

file = logging.FileHandler('tieba/tieba.log', encoding='utf-8')
file.setLevel(level)
file.setFormatter(formatter)
logger.addHandler(file)

console = logging.StreamHandler()
console.setLevel(level)
console.setFormatter(formatter)
logger.addHandler(console)


def get_proxy():
    """
    Get available proxy.
    :return: str - proxy_tag (eg. '123.33.22.11:12345')
    """

    # 获取 IP 池
    with open("tieba/settings.json", "r", encoding='utf-8') as f:
        settings = json.load(f)
    api = settings['api']
    proxy_list = requests.get(api).json()['data']

    # 筛选 IP
    for proxy in proxy_list:

        proxy_tag = f"{proxy['ip']}:{proxy['port']}"

        # 筛去已经使用过的 IP
        with open("tieba/used_proxy.txt", "r") as f:
            used_list = f.read().split()
        if proxy_tag in used_list:
            continue

        logger.info(f"checking proxy {proxy_tag}")

        # 测试 IP 的可用性
        try:
            ip_resp = requests.get(
                "http://ipinfo.io/ip",
                proxies={"http": proxy_tag},
                headers={"User-Agent": ua(use_cache_server=False).random},
                timeout=3
            )
        except (
                requests.exceptions.ReadTimeout,
                requests.exceptions.ConnectTimeout,
                requests.exceptions.ProxyError
        ):
            logger.warning("Timeout for " + proxy_tag)
            time.sleep(3)
            continue

        # 写入已用 proxy 并返回
        logger.info("Proxy: " + proxy_tag)
        with open("tieba/used_proxy.txt", "a+") as f:
            f.write(proxy_tag + '\n')

        return proxy_tag

    raise RuntimeError("Not enough IP")


def get_url(keyword):
    """
    Search for {keyword} in tieba.
    :param keyword: str Searching keyword
    :return:
    """

    page = 0

    while True:
        try:
            headers = {'user-agent': ua(use_cache_server=False).random}
            resp = requests.get(f"https://tieba.baidu.com/f/search/res?isnew=1&kw=&qw={keyword}&rn=10\
                                &un=&only_thread=0&sm=1&sd=&ed=&pn={page}",
                                headers=headers,
                                proxies={'http': get_proxy()},
                                timeout=8
                                )
            logger.info(f"Header {resp.request.headers}")

            soup = BS(resp.text, 'lxml')
            link_list = soup.find_all("a", class_="bluelink")
            url_list = list(map(lambda x: 'https://tieba.baidu.com' + x['href'], link_list))
            filtered_list = list(filter(lambda x: 'cid' in x, url_list))

            if not filtered_list:
                logger.info(f"{resp.text}")
                break

            with open("tieba/url.txt", "a+") as f:
                f.write('\n'.join(filtered_list) + '\n')
            logger.info('get url: \n' + '\n'.join(filtered_list) + '\n')
            time.sleep(10)

        except Exception as e:
            logger.exception(e)


def get_tieba_post():
    """
    Get the source code of all the websites in tieba/url.txt.
    :return:
    """

    with open("tieba/url.txt", "r") as f:
        url_list = f.read().split()

    for url in url_list:

        # 首先筛选已经访问过的网址
        id = re.findall('\d+', url)[0]
        with open("tieba/written.txt", "r") as w:
            if id in w.read():
                continue

        proxy_tag = get_proxy()
        try:
            # 尝试访问
            resp = requests.get(
                url,
                proxies={"https": proxy_tag},
                headers={'user-agent': ua(use_cache_server=False).random},
                timeout=8
            )
            logger.info(f"Header {resp.request.headers}")
            logger.info(f"Response {url + str(resp.status_code)}")

            # 如果不成功访问
            if '<!--STATUS OK-->' not in resp.text:
                with open("tieba/record.txt", "a") as f:
                    f.write(str(int(time.time())) + ":" + proxy_tag + "\n")
                time.sleep(random.uniform(10, 50))
                continue

            # 如果则成功访问，写入文件
            with open("tieba/record.txt", "a") as f:
                f.write(str(int(time.time())) + ":" + proxy_tag + "\n")
            with open(f"tieba/written.txt", "r") as w:
                w.write(url + '\n')
            with open(f"tieba/{id}.html", "w") as page:
                page.write(resp.text)
                logger.info(f"{id}.html written")

        except Exception as e:
            with open("tieba/record.txt", "a") as f:
                f.write(str(int(time.time())) + ":" + proxy_tag + "\n")
            time.sleep(random.uniform(10, 50))
            logger.exception(e)