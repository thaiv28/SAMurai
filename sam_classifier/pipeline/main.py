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
    
    X = df.drop(columns=["label"])
    y = df["label"]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.8, random_state=0)

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
        [("input_encoder", OrdinalEncoder(), encode_columns),
           ("text_preprocessing", vectorizer, "text")],
        verbose=True
    )
    
    pipe = Pipeline(
        [("cleaner", Cleaner()),
         ("column_transformer", ct),
         ("multinomial_nb", CustomNB())
        ]
    )
  
    pipe = pipe.fit(X_train, y_train) 
    print(pipe.score(X_test, y_test))
    
 
    

if __name__=="__main__":
    setup_logger()
    main()