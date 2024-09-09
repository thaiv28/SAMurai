import logging
import os
from collections import defaultdict

import pandas as pd

from samurai.logger import setup_logger

def main():
    setup_logger()
    df = pd.read_csv("../../files/archives/2_complete_unprocessed_unlabeled.csv", index_col = 0)

    df = df.drop_duplicates("Title", keep="last")
    f = open("../../files/labels.txt", "r")
    
    positive_ids = f.readlines()
    map = defaultdict(lambda: False, {id.strip() : True for id in positive_ids})
    df['label'] = False
    
    df['label'] = df["Sol#"].map(map)
    
    df.to_csv("../../files/archives/4_labeled_dataset.csv")
   
if __name__ == "__main__":
    main()