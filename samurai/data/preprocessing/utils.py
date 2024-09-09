import os
import logging

import pandas as pd

def merge_csv_files(path: str):
    logger = logging.getLogger(__name__)
    
    dfs = []
    
    for file in os.listdir(path):
        
        if not file.endswith(".csv"):
            logger.info(f"Not merging {file} because not csv file")
            
        df = pd.read_csv(path + file, index_col=0)
        logger.info(f"Adding {file} dataframe to list")
        dfs.append(df) 
        
    df = pd.concat(dfs)
    write_path = "../../files/archives/2_complete_unprocessed_unlabeled.csv"
    logger.info(f"Writing {df} to {write_path}")
   
    df.to_csv(write_path)
    

            
            