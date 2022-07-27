import requests
import time
import logging

from bs4 import BeautifulSoup as BS

fmt = '%(asctime)s.%(msecs)03d [%(levelname)s] %(message)s'
datefmt = '%Y-%m-%d %H:%M:%S'
level = logging.INFO

formatter = logging.Formatter(fmt, datefmt)
logger = logging.getLogger()
logger.setLevel(level)

file = logging.FileHandler('geron_npo/geron_npo.log', encoding='utf-8')
file.setLevel(level)
file.setFormatter(formatter)
logger.addHandler(file)

console = logging.StreamHandler()
console.setLevel(level)
console.setFormatter(formatter)
logger.addHandler(console)


def npo_get_urls_from_npo(target):
    """
    输入希望查找的关键词，在 npo 站内进行搜索
    搜索结果写入 ./jiia/url.txt 中
    :param target: str
    :return:
    """

    page = 1
    while True:

        # 获取网页源码
        resp = requests.get(f"https://www.genron-npo.net/mtos/mt-search.cgi?search={target}&IncludeBlogs=\
        11%2C7%2C2%2C22%2C18%2C23%2C13%2C6%2C9%2C12%2C14%2C15%2C8%2C10%2C19%2C5&blog_id=9&limit=20&page={page}")
        logger.info(f'getting the {page}th page')

        # 获取文章 url
        soup = BS(resp.text, 'lxml')
        box_links = soup.find_all("a", class_="boxlink")
        urls = list(map(lambda x: x['href'], box_links))
        time.sleep(3)

        # 如果已经找不到任何结果，就停止循环，否则在 list 后添加新的网址
        if not urls:
            logger.info("finish searching")
            break
        else:
            page += 1
            logger.info("finish searching: \n" + '\n'.join(urls))
            with open("genron_npo/url.txt", "a+") as f:
                f.write('\n'.join(urls) + '\n')


def npo_write_articles():
    """
    获取文章的 url, 在 genron-npo 文件夹下生成文章
    :return:
    """
    with open("jiia/url.txt", "r") as f:
        url_list = f.read().split('\n')

    for url in url_list:
        # 获取网页
        resp = requests.get(url)
        resp.encoding = 'utf-8'
        logger.info(f"getting {url}")

        # 获取信息
        soup = BS(resp.text, 'lxml')
        title = soup.find_all("h1")[1].text
        body = soup.find("section", class_="entry")

        with open(f"./genron_npo/{title}.txt", "w") as f:
             f.write(body.text)

        # 如果需要 html 可以用以下的语句
        # with open(f"./genron_npo{title}.html", "w") as f:
            # f.write(resp.text)

        time.sleep(3)
