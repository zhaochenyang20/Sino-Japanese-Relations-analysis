import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from IPython import embed
from tqdm import tqdm
import re
import utils


name = 'youtube'
raw_dir = './raw/youtube/'
save_dir = './data/youtube/'


def parse_html(html_list: np.ndarray) -> pd.DataFrame:
    """Parse html contents to get video information.

    Args:
        html_list: a np.ndarray of html contents

    Returns:
        all_post_info: a pd.DataFrame of video information
    """
    try:
        single_post_info_list = []
        for html in tqdm(html_list):
            soup = BeautifulSoup(html, 'lxml')

            # time
            time = (
                soup.find('yt-formatted-string', id='formatted-snippet-text')
                .contents[2]
                .string
            )
            if time.find('Scheduled for') != -1:
                continue
            if time.find('live') != -1:
                time = time[17:]
            if time.find('Premiered') != -1:
                time = time[10:]
            time = pd.to_datetime(time)

            # title
            title = soup.find_all('h1')[1].find_next().string
            if title == None:
                title = soup.find_all('h1')[1].find_next().find_next().string

            # view_num
            view_num = int(
                re.search(
                    r'(.*?)\sview',
                    soup.find('yt-formatted-string', id='formatted-snippet-text')
                    .contents[0]
                    .string,
                )
                .group(1)
                .replace(',', '')
            )

            # like_num
            like_num = soup.find_all(
                'yt-formatted-string',
                class_='style-scope ytd-toggle-button-renderer style-text',
            )[0].string
            if like_num == 'Like':
                like_num = '0'

            # comment_num
            comment_num = '0'
            possible_comment_num = soup.find(
                                            'div',
                                            id='count',
                                            class_='style-scope ytd-comments-entry-point-header-renderer',
                                        )
            if possible_comment_num != None and possible_comment_num.string != None:
                comment_num = possible_comment_num.string

            # single_post_info    
            single_post_info = pd.Series(
                [time, title, view_num, like_num, comment_num],
                index=['time', 'title', 'view_num', 'like_num', 'comment_num'],
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
