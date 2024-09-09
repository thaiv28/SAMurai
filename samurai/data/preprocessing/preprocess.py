from samurai.logger import setup_logger
import samurai.data.preprocessing.utils as utils
import samurai.data.preprocessing.nlp as nlp
import samurai.data.preprocessing.categorical as categorical

import pandas as pd

def main():
    df = pd.read_csv("../../files/archives/complete_unprocessed_unlabeled.csv")
    
    df, vectorizer = nlp.preprocess_vectorize(df)
    # df, encoder = categorical.encode(df)
    # save vectorizer and encoder

if __name__ == "__main__":
    main()