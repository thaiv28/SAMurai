from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
import nltk
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from unidecode import unidecode
import logging

from sam_classifier.logger import setup_logger

import pandas as pd

nltk.download('wordnet')

DATASET_PATH = "../../files/"

class LemmaTokenizer:
    def __init__(self):
        self.wnl = WordNetLemmatizer()
        
    def __call__(self, doc):
        return [self.wnl.lemmatize(token) for token in word_tokenize(doc)]

class Preproccessor:
    def __init__(self):
        self.stopwords = set(stopwords.words('english'))
    
    def __call__(self, doc: str):
        doc = doc.lower()
        doc = doc.replace("\n", "").replace("\t", "")
        # convert to ascii representation
        doc = unidecode(doc)
        
        tokens = word_tokenize(doc)
        # remove stopwords
        filtered = [token for token in tokens if token not in self.stopwords]

        return " ".join(filtered)

def preprocess_vectorize(df):
    logger = logging.getLogger(__name__)
    
    logger.info("Combining description and attachments into text column")
    df['text'] = df.Description.str.cat(df.Attachments, na_rep="")
   
    logger.debug(df['Description']) 
    logger.debug(df['Attachments'])
    logger.debug(df['text'])
    
    vectorizer = TfidfVectorizer(preprocessor=Preproccessor(), tokenizer=LemmaTokenizer())
    logger.info("Fitting vectorizer and transforming text")
    logger.info(len(df.text))
    list = vectorizer.fit_transform(df['text'])

    print(type(list[0]))

    # TODO: save vectorizer as pickle file to be used during inference

    return (df, vectorizer)

def main():
    df = pd.read_csv(DATASET_PATH + "/raw_dataset.csv", index_col=0)
    
    df, vectorizer = preprocess_vectorize(df)
     
    df.to_csv(DATASET_PATH + "/preprocessed_dataset.csv")
    
def test():
    setup_logger()
    logger = logging.getLogger(__name__)
   
    logger.info("Reading CSV into DF") 
    df = pd.read_csv("../../files/archives/split_by_date/06-21-2024.csv")
    
    preprocess_vectorize(df)
    
    
    
 
if __name__=="__main__":
    test()



