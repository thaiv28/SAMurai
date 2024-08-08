import logging

from sam_classifier.data.cleaning import helpers

class Cleaner:
    def __init__(self):
        pass
    
    def fit(self, X, Y):
        return self
    
    def transform(self, X):
        return helpers.clean_data(X)