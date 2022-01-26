import pandas as pd
from cleantext import clean
import datetime
import flair
from tqdm import tqdm

sentiment_model = flair.models.TextClassifier.load('en-sentiment')
tickers = pd.read_pickle('utils/tickers_big3.pkl')
brr = pd.read_pickle('reports/Jan-24-2022-goes-brr.pkl')
flairtest = pd.read_pickle('utils/flair_test.pkl')



def summary(brr): #파일의 통계치
    text = ['title', 'selftext']
    idx = ['count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max']
    stats = pd.DataFrame(columns=['title', 'selftext'], index=idx)
    print('Summarizing..')
    for t in tqdm(text):
        st = brr[f'{t}'].apply(len).describe()
        stats[f'{t}'] = st

    print(f'There are {stats.title[0]} posts today.')
    print(f'Avg. length of the posts are {stats.selftext[1]}.')

def cleaner(brr): #파일 클리닝
    print('Cleaning Text..')
    cleantitle = [clean(text, lower=False) for text in brr['title']]
    brr['title'] = cleantitle

    cleanselftext = [clean(text, lower=False) for text in brr['selftext']]
    brr['selftext'] = cleanselftext

    realtime = [datetime.datetime.fromtimestamp(time) for time in brr['created_utc']]
    brr['realtime'] = realtime

    score = [int(score) for score in brr['score']]
    brr['score'] = score

    print('Cleaned!')
    return brr


def tickercount(brr):
    sentences = [flair.data.Sentence(post) for post in brr['selftext']] #한 포스트를 센텐스화
    sentences = [sentence.tokens for sentence in sentences] #센텐스를 토큰화
    sentence_tokens = [[str(token) for token in sentence] for sentence in sentences]  # 토큰을 str list 화

    tickers = pd.read_pickle('utils/tickers_big3.pkl')
    tickerlist = list(tickers['tickers'])

    fullcount=[]
    print('Analyzing tickers..')
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
    brr['tickerinfo'] = fullcount
    return brr



def flairme(brr): #1000개의 본문파싱하는데 대략 8분걸렸다
    probability = []
    sentiment = []
    print('Analyzing Sentiment..')
    for text in tqdm(brr['selftext'].to_list()):
        sentence = flair.data.Sentence(text)
        sentiment_model.predict(sentence)
        probability.append(sentence.labels[0].score)
        sentiment.append(sentence.labels[0].value)
    brr['probability'] = probability
    brr['sentiment'] = sentiment
    return brr

if __name__ == '__main__':
    summary()