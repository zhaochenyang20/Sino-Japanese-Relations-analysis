import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from IPython import embed
from tqdm import tqdm
import re
import utils


name = 'peace_forum'
raw_dir = './raw/peace_forum/'
save_dir = './data/peace_forum/'


def parse_html(html_list: np.ndarray) -> None:
    """Parse html contents to get peace_forum post information.

    Args:
        html_list: a np.ndarray of html contents

    Returns:
        None
    """
    try:
        for html in tqdm(html_list):
            soup = BeautifulSoup(html, 'lxml')

            # title
            title = soup.find('p', class_='post_ttl').string

            # content
            content = ''
            text_list = soup.find('div', class_='post post-details').find_all('p')
            for text_ in text_list:
                if text_.get_text() != None and text_.get_text() != 'このページの先頭へ':
                    content += '  ' + text_.get_text() + '\n\n'

            utils.save_as_txt(title, content, save_dir)
    except Exception as e:
        print(e)
        raise RuntimeError('Cannot parse html')


if __name__ == '__main__':
    try:
        raw = utils.read_html(raw_dir)
        parse_html(raw)
    except Exception as e:
        embed(header=str(e))