import pandas as pd
import numpy as np
from cleantext import clean
import datetime
import flair
import timeit
from tqdm import tqdm
import time

sentiment_model = flair.models.TextClassifier.load('en-sentiment')
tickers = pd.read_pickle('utils/tickers_big3.pkl')
testdata = pd.read_pickle('reports/Jan-24-2022-goes-brr.pkl')
flairtest = pd.read_pickle('utils/flair_test.pkl')



def summary(): #파일의 통계치
    text = ['title', 'selftext']
    idx = ['count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max']
    stats = pd.DataFrame(columns=['title', 'selftext'], index=idx)
    for t in text:
        st = testdata[f'{t}'].apply(len).describe()
        stats[f'{t}'] = st
    return stats

def cleaner(): #파일 클리닝
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
    sentences = [flair.data.Sentence(post) for post in testdata['selftext']] #한 포스트를 센텐스화
    sentences = [sentence.tokens for sentence in sentences] #센텐스를 토큰화
    sentence_tokens = [[str(token) for token in sentence] for sentence in sentences]  # 토큰을 str list 화

    tickers = pd.read_pickle('utils/tickers_big3.pkl')
    tickerlist = list(tickers['tickers'])

    fullcount=[]
    for sentence in tqdm(sentence_tokens):
        sentence = str(sentence)
        sentence = clean(sentence, lower=False)
        tickercount = []

        for ticker in tickerlist:
            count = 0
            nocount = 0
            secondcount=[]
            if ticker in sentence:
                count +=1
            else:
                nocount +=1
            if count > 0:
                tickercount.append(f'{ticker} was mentioned {count} times in this post.')

            secondcount.append(tickercount)
        fullcount.append(str(tickercount))
    testdata['tickerinfo'] = fullcount



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