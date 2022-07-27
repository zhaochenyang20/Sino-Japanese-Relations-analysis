import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from IPython import embed
from tqdm import tqdm
import re
import utils


name = 'tieba'
raw_dir = './raw/tieba/'
save_dir = './data/tieba/'


def parse_html(html_list: np.ndarray) -> pd.DataFrame:
    """Parse html contents to get tieba post information.

    Args:
        html_list: a np.ndarray of html contents

    Returns:
        all_post_info: a pd.DataFrame of tieba post information
    """
    try:
        single_post_info_list = []
        for html in tqdm(html_list):
            soup = BeautifulSoup(html, 'lxml')

            # title and time
            if soup.find('h3') != None:
                title = str(soup.find('h3').get_text(strip=True))
                if soup.find_all('span', class_='tail-info')[1].get_text() == '1楼':
                    time = soup.find_all('span', class_='tail-info')[2].get_text()
                else:
                    time = soup.find_all('span', class_='tail-info')[1].get_text()
            else:
                title = str(soup.find('h1').get_text(strip=True))
                time = json.loads(
                    soup.find('div', class_='p_postlist')
                    .find_next()
                    .attrs['data-field']
                )['content']['date']

            # reply_num
            reply_num = int(
                soup
                .find_all('li', class_='l_reply_num')[0]
                .find_next()
                .string
            )

            # single_post_info
            single_post_info = pd.Series(
                [time, title, reply_num],
                index=['time', 'title', 'reply_num']
            )
            single_post_info_list.append(single_post_info)

        # all_post_info
        all_post_info = (
            pd.DataFrame(single_post_info_list)
            .sort_values(['time'])
            .drop_duplicates()
        )
        return all_post_info
    except Exception as e:
        print(e)
        raise RuntimeError('Cannot parse html')


if __name__ == '__main__':
    try:
        raw = utils.read_html(raw_dir)
        data = parse_html(raw)
        utils.save_data(data, save_dir, name)
    except Exception as e:
        embed(header=str(e))
