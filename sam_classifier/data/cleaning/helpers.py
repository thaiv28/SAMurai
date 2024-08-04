import logging

import pandas as pd

from sam_classifier.logger import setup_logger

def remove_columns(df: pd.DataFrame):
    logger = logging.getLogger(__name__)
    columns = []
   
    # remove columns that aren't available at inference
    columns += ["ArchiveType", "ArchiveDate", "Active"]
    # remove columns that give irrelevant info
    columns += ["Sol#", "Awardee","PrimaryContactTitle","PrimaryContactFullname",
                "PrimaryContactEmail","PrimaryContactPhone","PrimaryContactFax",
                "SecondaryContactTitle","SecondaryContactFullname",
                "SecondaryContactEmail","SecondaryContactPhone","SecondaryContactFax",
                "AdditionalInfoLink","Link", "AwardNumber"]
    # remove columns that are redundant
    columns += ["SetASide", 'PopStreetAddress', 'PopCity', 'PopState', 'PopZip', 
                'PopCountry', "BaseType"]
    # remove columns difficult to work with
    columns += ["AwardDate", "ResponseDeadLine", "Award$"]
   
    logger.info(f"Remove columns from df: {columns}")
    df = df.drop(columns=columns)
    return df

def remove_duplicate_rows(df: pd.DataFrame):
    logger = logging.getLogger(__name__)
   
    new_df = df.drop_duplicates("Title", keep="last")
    logger.info(f"Removed duplicate rows. Dataset size {len(df)} to {len(new_df)}")
    
    return new_df


def rearrange_columns(df: pd.DataFrame):
    logger = logging.getLogger(__name__)
    date_col = df.pop("PostedDate")
  
    df.insert(1, "PostedDate", date_col)
    
    logger.info("Combining description and attachments into text column")
    df['text'] = df.Title.str.cat([df.Description, df.Attachments], na_rep="")
    df = df.drop(columns=["Title", "Description", "Attachments"])
    
    return df
    
def clean_data(df: pd.DataFrame):
    logger = logging.getLogger(__name__)
    logger.info(f"Beginning clean data")
    df = remove_columns(df)
    df = rearrange_columns(df)
    df = remove_duplicate_rows(df)
    logger.info(f"Finished cleaning data")
    
    return df

def main():
    setup_logger()
    
    df = pd.read_csv("../../files/archives/2_complete_unprocessed_unlabeled.csv")
    df = clean_data(df)
    df.to_csv("../../files/archives/3_cleaned_unprocessed_unlabeled.csv")
    print(df.columns)
    
if __name__ == "__main__":
    main()