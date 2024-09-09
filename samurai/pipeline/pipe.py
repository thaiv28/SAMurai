import logging

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OrdinalEncoder
from sklearn.impute import SimpleImputer
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics import confusion_matrix
import pandas as pd
import numpy as np

from samurai.logger import setup_logger
from samurai.data.preprocessing.nlp import LemmaTokenizer, Preproccessor
from samurai.data.cleaning.cleaner import Cleaner
from samurai.model.nb import CustomNB
from samurai.pipeline import pipe_helpers

class CustomPipeline:
    def __init__(self):
        self.cleaner = Cleaner()
        self.imputer = SimpleImputer(strategy="constant")
        self.categorical_ct, self.text_ct = self._init_ct()
        self.model = CustomNB()
        self._logger = logging.getLogger(__name__)

      
    def _init_ct(self):
        vectorizer = TfidfVectorizer(
            preprocessor=Preproccessor(),
            tokenizer=LemmaTokenizer()
        )
        
        encode_columns = ['Department/Ind.Agency', 'CGAC', 'Sub-Tier',
       'FPDS Code', 'Office', 'AAC Code', 'Type', 'SetASideCode', 'NaicsCode',
       'ClassificationCode', 'OrganizationType', 'State', 'City', 'ZipCode',
       'CountryCode']
        
        categorical_ct = ColumnTransformer(
            [("input_encoder", OrdinalEncoder(handle_unknown="use_encoded_value",
                                            unknown_value=np.nan), encode_columns)]
        )
        
        text_ct = ColumnTransformer(
            [("text_preprocessing", vectorizer, "text")]
        )
        
        return categorical_ct, text_ct
    
    def clean(self, df):
        return self.cleaner.transform(df) 
     
    def fit(self, X_train, y_train):
        imputed_X = pd.DataFrame(self.imputer.fit_transform(X_train), columns = X_train.columns)
        self._logger.debug(type(imputed_X))
        
        categorical_X = self.categorical_ct.fit_transform(imputed_X)
        self._logger.debug("Fitted categorical df: %s", categorical_X)
        
        text_X = self.text_ct.fit_transform(imputed_X)
        self._logger.debug("Fitted text df: %s", text_X)
        self.model = self.model.fit(categorical_X, text_X, y_train)
        
    def predict(self, X):
        imputed_X = pd.DataFrame(self.imputer.transform(X), columns=X.columns)
        
        categorical_X = self.categorical_ct.transform(imputed_X)
        categorical_X = pipe_helpers.replace_nan_with_mean(categorical_X)
        
        text_X = self.text_ct.transform(imputed_X)
        
        return self.model.predict(categorical_X, text_X)
    
    def score(self, X, y):
        y_pred = self.predict(X)
        return np.sum(y_pred == y) / y_pred.size
   
    def analyze(self, X, y) -> str:
        predicted_y = self.predict(X)
        score = np.sum(predicted_y == y) / predicted_y.size
        
        string = f"Score: {score}"
        string += f"\n{self.print_confusion_matrix(y, predicted_y)}"  
        
        return string
    
    def print_confusion_matrix(self, expected_y, predicted_y):
        tn, fp, fn, tp = confusion_matrix(expected_y, predicted_y).ravel()
        
        string = f"True Negative: {tn} | False Positive: {fp}\nFalse Negative: {fn} | True Positive: {tp}"
        
        return string 
    
           
    
        
        
     
        
        
    
        
        