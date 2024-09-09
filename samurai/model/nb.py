import logging

from sklearn.naive_bayes import MultinomialNB, CategoricalNB
from sklearn.preprocessing import LabelEncoder
import pandas as pd
import numpy as np

from samurai.logger import setup_logger

class CustomNB:
    def __init__(self):
        self.categorical_nb = CategoricalNB()
        self.multinomial_nb = MultinomialNB()
        self.label_encoder = LabelEncoder()
        
        self._logger = logging.getLogger(__name__)
    
    def fit(self, X_categorical, X_text, y):
        encoded_y = self.label_encoder.fit_transform(y) 
        
        self.categorical_nb = self.categorical_nb.fit(X_categorical, encoded_y)
        self.multinomial_nb = self.multinomial_nb.fit(X_text, encoded_y)
        
        return self
   
    def predict_log_proba(self, categorical_X, text_X):
        categorical_log_prob = self.categorical_nb.predict_log_proba(categorical_X)
        multinomial_log_prob = self.multinomial_nb.predict_log_proba(text_X)
        
        return categorical_log_prob + multinomial_log_prob
       
    def predict_proba(self, categorical_X, text_X):
        log_proba = self.predict_log_proba(categorical_X, text_X) 
      
        self._logger.debug("Log probabilities: %s", log_proba) 
        numerator = np.exp(log_proba)
        denominator = np.sum(numerator, axis=1, keepdims=True)
        softmax_proba = numerator / denominator 
        
        self._logger.debug("Softmax applied: %s", softmax_proba)
        
        return softmax_proba
 
        
    def predict(self, categorical_X, text_X):
        proba = self.predict_proba(categorical_X, text_X)
        encoded_labels = np.argmax(proba, axis=1, keepdims=True)
        self._logger.debug(encoded_labels)
        labels = self.label_encoder.inverse_transform(encoded_labels)
        
        return labels

    
    