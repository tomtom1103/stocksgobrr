import pandas as pd
import numpy as np
from utils import indexes
from cleantext import clean
import datetime
import flair
import timeit
from tqdm import tqdm
import time

sentiment_model = flair.models.TextClassifier.load('en-sentiment')
tickers = pd.read_pickle('utils/tickers.pkl')
testdata = pd.read_pickle('reports/Jan-24-2022-goes-brr.pkl')
flairtest = pd.read_pickle('utils/flair_test.pkl')

def summary():
    text = ['title', 'selftext']
    stats = pd.DataFrame(columns=['title', 'selftext'], index=indexes)
    for t in text:
        st = testdata[f'{t}'].apply(len).describe()
        stats[f'{t}'] = st
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

def tickercount_1():
    starttime = timeit.default_timer()
    tickers = pd.read_pickle('utils/tickers.pkl')
    tickerlist = list(tickers['tickers'])
    fullcounts=[]
    for ticker in tqdm(tickerlist):
        tickercount = []
        sentences = [flair.data.Sentence(post) for post in testdata['selftext']] #한 포스트를 센텐스화
        sentences = [sentence.tokens for sentence in sentences] #센텐스를 토큰화
        sentence_tokens = [[str(token) for token in sentence] for sentence in sentences]  # 토큰을 str list 화
        count = int(len([ticker for sentence in sentence_tokens for token in sentence if ticker in token]))
        #각 포스트 안 해당 티커가 존재하면 티커의 수 카운트
        tickercount.append(f'{ticker} was mentioned {count} times in this post.')
        fullcounts.append(str(tickercount))

    testdata['ticker_info'] = fullcounts
    print(timeit.default_timer() - starttime)


def tickercount():
    starttime = timeit.default_timer()
    tickers = pd.read_pickle('utils/tickers.pkl')
    tickerlist = list(tickers['tickers'])
    fullcounts=[]
    sentences = [flair.data.Sentence(post) for post in testdata['selftext']] #한 포스트를 센텐스화
    sentences = [sentence.tokens for sentence in sentences] #센텐스를 토큰화
    sentence_tokens = [[str(token) for token in sentence] for sentence in sentences]  # 토큰을 str list 화

    for ticker in tqdm(tickerlist):
        tickercount = []
        count = int(len([ticker for sentence in sentence_tokens for token in sentence if ticker in token]))
        #각 포스트 안 해당 티커가 존재하면 티커의 수 카운트
        tickercount.append(f'{ticker} was mentioned {count} times in this post.')
        for i in range(len(testdata)):
            fullcounts.append(str(tickercount))

    testdata['ticker_info'] = fullcounts
    print(timeit.default_timer() - starttime)



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