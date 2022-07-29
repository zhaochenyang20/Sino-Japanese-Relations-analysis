import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from IPython import embed
from tqdm import tqdm
import re
import utils


name = 'twitter'
raw_dir = './raw/twitter/'
save_dir = './data/twitter/'


def parse_html(html_list: np.ndarray) -> pd.DataFrame:
    """Parse html contents to get tweet information.

    Args:
        html_list: a np.ndarray of html contents

    Returns:
        all_post_info: a pd.DataFrame of tweet information
    """
    try:
        single_post_info_list = []
        for html in tqdm(html_list):
            soup = BeautifulSoup(html, 'lxml')

            text_list = soup.find_all(attrs={'data-testid': 'tweetText'})
            time_list = soup.find_all('time')
            tweet_info_box = soup.find_all(attrs={'role': 'group'})
            reply_num_list = []
            retweet_num_list = []

            # reply_num and retweet_num
            for tweet_info in tweet_info_box:
                if tweet_info.has_attr('aria-label'):
                    reply_num = 0
                    retweet_num = 0
                    if (
                        re.search(r'(\d+)\srep', tweet_info.attrs['aria-label'])
                        != None
                    ):
                        reply_num = int(
                            re.search(
                                r'(\d+)\srep', tweet_info.attrs['aria-label']
                            ).group(1)
                        )
                    if (
                        re.search(r'(\d+)\sRetweet', tweet_info.attrs['aria-label'])
                        != None
                    ):
                        retweet_num = int(
                            re.search(
                                r'(\d+)\sRetweet', tweet_info.attrs['aria-label']
                            ).group(1)
                        )
                    reply_num_list.append(reply_num)
                    retweet_num_list.append(retweet_num)

            for index in range(len(time_list)):

                # text and time
                text = str()
                for i in range(0, len(text_list[index].find_next().find_next_siblings())):
                    if (
                        text_list[index].find_next().find_next_siblings()[i].string
                        != None
                    ):
                        text += (
                            text_list[index]
                            .find_next()
                            .find_next_siblings()[i]
                            .string
                        )
                time = time_list[index].attrs['datetime']
                reply_num = reply_num_list[index]
                retweet_num = retweet_num_list[index]

                # single_post_info
                single_post_info = pd.Series(
                    [time, text, reply_num, retweet_num],
                    index=['time', 'text', 'reply_num', 'retweet_num'],
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
