import pandas as pd
import numpy as np
from tqdm import tqdm
import os


def read_html(raw_dir: str) -> np.ndarray:
    """Read raw data from html files.

    Args:
        raw_dir: directory of raw data

    Returns:
        html_list: a np.ndarray of html contents
    """
    try:
        file_name_list = os.listdir(raw_dir)
        html_list = []
        for file_name in tqdm(file_name_list):
            if file_name.endswith('.html'):
                file_path = os.path.join(raw_dir, file_name)
                with open(file_path, 'r') as f:
                    html = f.read()
                    html_list.append(html)
        html_list = np.asarray(html_list)
        return html_list
    except Exception as e:
        print(e)
        raise IOError('Cannot read html files')


def save_data(data: pd.DataFrame, save_dir: str, name: str) -> None:
    """Save processed data into different formats.

    Args:
        data: processed data
        save_dir: directory to save data
        name: name of the data

    Returns:
        None
    """
    try:
        data.to_csv(save_dir + name + '.csv', index=False)
        data.to_excel(save_dir + name + '.xlsx', index=False)
        data.to_json(
            save_dir + name + '.json',
            orient='split',
            force_ascii=False,
            indent=4,
            index=False,
        )
        data.to_csv(save_dir + name + '.txt', sep='\t', index=False)
    except Exception as e:
        print(e)
        raise IOError('Cannot save data')


def save_as_txt(title: str, content: str, save_dir: str) -> None:
    """Save post information into txt file.

    Args:
        title: title of the post
        content: content of the post
        save_dir: directory to save data

    Returns:
        None
    """
    try:
        with open(save_dir + title + '.txt', 'w') as f:
            f.write(content)
    except Exception as e:
        print(e)
        raise IOError('Cannot save as txt')
    