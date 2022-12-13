import os
import json
from typing import List, Optional
from collections.abc import Iterable
from tqdm import tqdm
import random
import pandas as pd
import py_vncorenlp

"""
Note: define current path
"""
current_path = os.path.dirname(os.path.realpath(__file__))
"""
Note: set environment path for java compiler
"""
# os.environ["JAVA_HOME"] = "/data/nlp/dungdx4/java/jdk1.8.0_45"
os.environ["JAVA_HOME"] = "/usr/lib/jvm/java-11-openjdk-amd64"
"""
Note: Set seed
"""
random.seed(69)
"""
Note: create rdrsegmenter
"""
rdrsegmenter = py_vncorenlp.VnCoreNLP(annotators=["wseg"],
                                      save_dir=current_path+'/VnCoreNLP')
os.chdir("..")


def read_data_from_json(filename: str):
    with open(filename, 'r') as f:
        data = json.load(f)
    return data


def write_data_to_json(data: List[dict], filename: str):
    with open(filename, 'w', encoding='utf8') as f:
        json.dump(data, f, ensure_ascii=False)


def reformat_json_file(filename: str,
                       new_filename: Optional[str] = None):
    data = read_data_from_json(filename)
    if new_filename:
        write_data_to_json(data, new_filename)
    else:
        write_data_to_json(data, filename)


def read_new_data():
    """
    Note: 
    """

    text_pos = list()
    text_neg = list()

    for filename in tqdm(os.listdir(current_path+'/data/new_data/data_train/train/neg')):
        with open(os.path.join(current_path+'/data/new_data/data_train/train/neg', filename), 'r') as f:
            text_neg.append(f.read())

    for filename in tqdm(os.listdir(current_path+'/data/new_data/data_train/train/pos')):
        with open(os.path.join(current_path+'/data/new_data/data_train/train/pos', filename), 'r') as f:
            text_pos.append(f.read())

    for filename in tqdm(os.listdir(current_path+'/data/new_data/data_train/test/neg')):
        with open(os.path.join(current_path+'/data/new_data/data_train/test/neg', filename), 'r') as f:
            text_neg.append(f.read())

    for filename in tqdm(os.listdir(current_path+'/data/new_data/data_train/test/pos')):
        with open(os.path.join(current_path+'/data/new_data/data_train/test/pos', filename), 'r') as f:
            text_pos.append(f.read())

    for filename in tqdm(os.listdir(current_path+'/data/new_data/data_test/test/neg')):
        with open(os.path.join(current_path+'/data/new_data/data_test/test/neg', filename), 'r') as f:
            text_neg.append(f.read())

    for filename in tqdm(os.listdir(current_path+'/data/new_data/data_test/test/pos')):
        with open(os.path.join(current_path+'/data/new_data/data_test/test/pos', filename), 'r') as f:
            text_pos.append(f.read())

    # crawled_data = pd.read_csv(current_path+'/data/new_data/crawled_data.csv')
    # crawled_data = crawled_data[crawled_data['rating']<8.5]
    # crawled_neg_text = crawled_data[crawled_data['rating']<6].values.tolist()
    # crawled_pos_text = crawled_data[crawled_data['rating']>=6].values.tolist()
    # text_pos = text_pos + crawled_pos_text
    # text_neg = text_neg + crawled_neg_text

    return text_pos, text_neg


def unsegment_data(list_text: Iterable[str]) -> List[str]:
    return list(map(lambda text: text.replace("_", " "), tqdm(list_text)))


def segment_data(list_text: Iterable[str]) -> List[str]:
    return list(map(lambda text: " ".join(rdrsegmenter.word_segment(text)), tqdm(list_text)))
