import logging

from samurai.data.cleaning import helpers

class Cleaner:
    def __init__(self):
        pass
    
    def fit(self, X):
        return self
    
    def transform(self, X):
        return helpers.clean_data(X)