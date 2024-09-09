import numpy as np

def replace_nan_with_mean(X: np.ndarray):
    col_means = np.nanmedian(X, axis=0)
    
    nan_indices = np.where(np.isnan(X))
    X[nan_indices] = np.take(col_means, nan_indices[1]) 
    
    return X
    