import time
import requests
import logging
from fake_useragent import UserAgent as ua

fmt = '%(asctime)s.%(msecs)03d [%(levelname)s] %(message)s'
datefmt = '%Y-%m-%d %H:%M:%S'
level = logging.INFO

formatter = logging.Formatter(fmt, datefmt)
logger = logging.getLogger()
logger.setLevel(level)

file = logging.FileHandler('peace_forum/peace_forum.log', encoding='utf-8')
file.setLevel(level)
file.setFormatter(formatter)
logger.addHandler(file)

console = logging.StreamHandler()
console.setLevel(level)
console.setFormatter(formatter)
logger.addHandler(console)


def get_articles():
    """
    Get the source code of all the websites in peace_forum/url.txt.
    :return:
    """
    with open("peace_forum/url.txt", "r") as f:
        url_list = f.read().split()

    for index, url in enumerate(url_list):

        resp = requests.get(url, headers={"user-agent": ua(use_cache_server=False).random})
        resp.encoding = 'UTF-8'
        logger.info(f"getting {url}")

        with open(f"peace_forum/{index}.html", "w") as f:
            f.write(resp.text)
        logger.info(f"{url} written")
        time.sleep(5)