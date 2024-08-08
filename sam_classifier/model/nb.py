import logging

from sklearn.naive_bayes import MultinomialNB
import pandas as pd

from sam_classifier.logger import setup_logger

class CustomNB:
    def __init__(self):
        self.multinomial_nb = MultinomialNB()
        self._logger = logging.getLogger(__name__)
    
    def fit(self, X, y):
        self._logger.debug("\n" + str(pd.DataFrame(X.toarray())))
        fit = self.multinomial_nb.fit(X["text"], y)
        return fit
    
    def predict(self, X):
        return self.multinomial_nb.predict(X)
    
    def score(self, X, y):
        return self.multinomial_nb.score(X, y)