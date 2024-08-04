import logging

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OrdinalEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
import pandas as pd

from sam_classifier.logger import setup_logger
from sam_classifier.data.preprocessing.nlp import LemmaTokenizer, Preproccessor
from sam_classifier.data.cleaning.cleaner import Cleaner

def main():
    """ Pipeline stages:
            - clean data
            - preprocess data
            - model
  
      """
    DATASET_PATH = ""
 
    df = pd.read_csv(DATASET_PATH) 

    # preprocess data
    encode_columns = ['Department/Ind.Agency', 'CGAC', 'Sub-Tier',
       'FPDS Code', 'Office', 'AAC Code', 'Type', 'SetASideCode', 'NaicsCode',
       'ClassificationCode', 'OrganizationType', 'State', 'City', 'ZipCode',
       'CountryCode']
 
    vectorizer = TfidfVectorizer(
        preprocessor=Preproccessor(),
        tokenizer=LemmaTokenizer()
    )
 
    ct = ColumnTransformer(
        [("encoder", OrdinalEncoder(), encode_columns),
           ("text_preprocessing", vectorizer, "text")]
    )
    
    pipe = Pipeline(
        [("cleaner", Cleaner()),
         ("column_transformer", ct),
         ()]
    )
    
 
    

if __name__=="__main__":
    setup_logger()
    main()