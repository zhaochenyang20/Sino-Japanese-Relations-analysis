import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from IPython import embed
from tqdm import tqdm
import re
import utils


name = 'tianya'
raw_dir = './raw/tianya/'
save_dir = './data/tianya/'


def parse_html(html_list: np.ndarray) -> pd.DataFrame:
    """Parse html contents to get tianya post information.

    Args:
        html_list: a np.ndarray of html contents

    Returns:
        all_post_info: a pd.DataFrame of tianya post information
    """
    try:
        single_post_info_list = []
        for html in tqdm(html_list):
            soup = BeautifulSoup(html, 'lxml')

            if (
                soup.find('div', class_='errorCon') == None
                and soup.find('div', class_='wd-question') == None
            ):

                # title
                title = str(soup.find('span', class_='s_title').find_next().string)

                atl_info = soup.find_all('div', class_='atl-info')[0].contents

                # time
                time = atl_info[3].string[3:]

                # click_num
                click_num = int(re.search(r'\d+', atl_info[5].string)[0])

                # reply_num
                reply_num = int(re.search(r'\d+', atl_info[7].attrs['title'])[0])

                # single_post_info
                single_post_info = pd.Series(
                    [time, title, click_num, reply_num],
                    index=['time', 'title', 'click_num', 'reply_num'],
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
