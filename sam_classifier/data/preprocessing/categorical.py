from sklearn.preprocessing import OrdinalEncoder

def encode(df):
    enc = OrdinalEncoder()
    enc.fit(df)
    
    df = enc.transform(df)
    
    return (df, enc)