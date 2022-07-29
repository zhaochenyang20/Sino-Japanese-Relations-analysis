import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from IPython import embed
from tqdm import tqdm
import re
import utils


name = 'jiia'
raw_dir = './raw/jiia/'
save_dir = './data/jiia/'


def parse_html(html_list: np.ndarray) -> None:
    """Parse html contents to get jiia post information.

    Args:
        html_list: a np.ndarray of html contents

    Returns:
        None
    """
    try:
        for html in tqdm(html_list):
            soup = BeautifulSoup(html, 'lxml')

            # title
            title = soup.find_all('h1')[-1].get_text()

            # content
            content = '  '
            text_list = soup.find_all('p', class_='MsoNormal indent')
            if text_list == []:
                for br in soup.find_all('br'):
                    br.decompose()
                text_list = soup.find('div', class_='post-contents').find_all('p')
            else:
                content += soup.find_all('p', class_='indent')[0].get_text()
            for text_ in text_list:
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