from sam_classifier.logger import setup_logger
import sam_classifier.data.preprocessing.utils as utils
import sam_classifier.data.preprocessing.nlp as nlp
import sam_classifier.data.preprocessing.categorical as categorical

import pandas as pd

def main():
    df = pd.read_csv("../../files/archives/complete_unprocessed_unlabeled.csv")
    
    df, vectorizer = nlp.preprocess_vectorize(df)
    # df, encoder = categorical.encode(df)
    # save vectorizer and encoder

if __name__ == "__main__":
    setup_logger()
    utils.merge_csv_files("../../files/archives/split_by_date/attachments_scraped/")
    