import pandas as pd
import numpy as np
import pickle
from utils import indexes
from cleantext import clean
import datetime

tickers = pd.read_pickle('utils/tickers.pkl')
testdata = pd.read_pickle('reports/Jan-24-2022-goes-brr.pkl')

def summary():
    text = ['title', 'selftext']
    df = pd.DataFrame(columns=['title', 'selftext'], index=indexes)
    for t in text:
        summary = testdata[f'{t}'].apply(len).describe()
        df[f'{t}'] = summary
    return df

def cleaner():
    cleantitle = [clean(text, lower=False) for text in testdata['title']]
    testdata['cleantitle'] = cleantitle

    cleanselftext = [clean(text, lower=False) for text in testdata['selftext']]
    testdata['cleanselftext'] = cleanselftext

    realtime = [datetime.datetime.fromtimestamp(time) for time in testdata['created_utc']]
    testdata['realtime'] = realtime

    del testdata['title'], testdata['selftext']
