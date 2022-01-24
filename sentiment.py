import pandas as pd
import numpy as np
from utils import indexes
from cleantext import clean
import datetime
import flair

sentiment_model = flair.models.TextClassifier.load('en-sentiment')
tickers = pd.read_pickle('utils/tickers.pkl')
testdata = pd.read_pickle('reports/Jan-24-2022-goes-brr.pkl')

def summary():
    text = ['title', 'selftext']
    stats = pd.DataFrame(columns=['title', 'selftext'], index=indexes)
    for t in text:
        summary = testdata[f'{t}'].apply(len).describe()
        stats[f'{t}'] = summary
    return stats

def cleaner():
    cleantitle = [clean(text, lower=False) for text in testdata['title']]
    testdata['title'] = cleantitle

    cleanselftext = [clean(text, lower=False) for text in testdata['selftext']]
    testdata['selftext'] = cleanselftext

    realtime = [datetime.datetime.fromtimestamp(time) for time in testdata['created_utc']]
    testdata['realtime'] = realtime

    score = [int(score) for score in testdata['score']]
    testdata['score'] = score
    return testdata

def tickercount():
    tickerlist = list(tickers['tickers'])
    for ticker in tickerlist:
        t_count = testdata['selftext'].str.contains(f'{ticker}').sum()
        if t_count > 50:
            print(f"There are {t_count} mentions of {ticker} in the posts")

def flair(): #1000개의 본문파싱하는데 대략 8분걸렸다
    probability = []
    sentiment = []
    for text in testdata['selftext'].to_list():
        sentence = flair.data.Sentence(text)
        sentiment_model.predict(sentence)
        probability.append(sentence.labels[0].score)
        sentiment.append(sentence.labels[0].value)
    testdata['probability'] = probability
    testdata['sentiment'] = sentiment