import pandas as pd
import numpy as np
import pickle
from utils import indexes

tickers = pd.read_pickle('utils/tickers.pkl')
testdata = pd.read_pickle('reports/Jan-24-2022-goes-brr.pkl')

def summary():
    text = ['title', 'selftext']
    df = pd.DataFrame(columns=['title', 'selftext'], index=indexes)
    for t in text:
        summary = testdata[f'{t}'].apply(len).describe()
        df[f'{t}'] = summary
    return df

