import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from IPython import embed
from tqdm import tqdm
import re
import utils


name = 'facebook'
raw_dir = './raw/facebook/'
save_dir = './data/facebook/'


def parse_html(html_list: np.ndarray) -> pd.DataFrame:
    """Parse html contents to get facebook post information.

    Args:
        html_list: a np.ndarray of html contents

    Returns:
        all_post_info: a pd.DataFrame of facebook post information
    """
    try:
        single_post_info_list = []
        for html in tqdm(html_list):
            soup = BeautifulSoup(html, 'lxml')

            # Take the number of likes as the positioning mark of each post
            # to find other information.
            like_list = soup.find_all('span', class_='pcp91wgn')
            for like in range(len(like_list) // 2):

                # like_num
                like_num = like_list[like * 2].string

                # time
                time = (
                    like_list[like * 2]
                    .find_parents()[12]
                    .find_previous_siblings()[1]
                    .find(
                        'a',
                        class_='oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl gmql0nx0 gpro0wi8 b1v8xokw',
                    )
                    .string
                )
                time = pd.to_datetime(time)

                # text
                text = str()
                text_list = (
                    like_list[like * 2]
                    .find_parents()[12]
                    .find_previous_sibling()
                    .find_all('div', attrs={'style': 'text-align: start;'})
                )
                for text_index in range(len(text_list)):
                    if text_list[text_index].string != None:
                        text += text_list[text_index].string

                # comment_num and share_num
                comment_num = 0
                share_num = 0
                comment_share_list = (
                    like_list[like * 2]
                    .find_parents()[5]
                    .find_next_sibling()
                    .find_all(
                        'span',
                        class_='d2edcug0 hpfvmrgz qv66sw1b c1et5uql oi732d6d ik7dh3pa ht8s03o8 a8c37x1j fe6kdd0r mau55g9w c8b282yb keod5gw0 nxhoafnm aigsh9s9 d9wwppkn iv3no6db jq4qci2q a3bd9o3v b1v8xokw m9osqain',
                    )
                )
                for comment_share in range(len(comment_share_list)):
                    if re.search(r'(\d+)\scomment', comment_share_list[comment_share].string) != None :
                        comment_num = int(
                            re.search(
                                r'(\d+)\scomment',
                                comment_share_list[comment_share].string,
                            ).group(1)
                        )
                    if re.search(r'(\d+)\sshare', comment_share_list[comment_share].string) != None:
                        share_num = int(
                            re.search(
                                r'(\d+)\sshare',
                                comment_share_list[comment_share].string,
                            ).group(1)
                        )

                # single_post_info
                single_post_info = pd.Series(
                    [time, text, comment_num, share_num, like_num],
                    index=['time', 'text', 'comment_num', 'share_num', 'like_num'],
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
