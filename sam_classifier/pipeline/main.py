import logging

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OrdinalEncoder
from sklearn.preprocessing import OneHotEncoder
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import MultinomialNB
import pandas as pd

from sam_classifier.logger import setup_logger
from sam_classifier.data.preprocessing.nlp import LemmaTokenizer, Preproccessor
from sam_classifier.data.cleaning.cleaner import Cleaner
from sam_classifier.model.nb import CustomNB
from sam_classifier.pipeline.pipe import CustomPipeline

def main():
   
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG) 
    
    """ Pipeline stages:
            - clean data
            - preprocess data
            - model
  
      """
    DATASET_PATH = "../files/archives/4_labeled_dataset.csv"
 
    df = pd.read_csv(DATASET_PATH)
    pipe = CustomPipeline()
   
    df = pipe.clean(df)
    
    X = df.drop(columns=["label"])
    y = df["label"]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.8, random_state=0)
    logger.info("Sizes: X_train - %d, X_test - %d", len(X_train), len(X_test))
    
    pipe.fit(X_train, y_train)
    print(pipe.score(X_test, y_test))
    

if __name__=="__main__":
    setup_logger()
    main()