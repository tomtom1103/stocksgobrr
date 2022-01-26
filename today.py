import pandas as pd
import praw
from config import *
from datetime import date
import os
import flair
from tqdm import tqdm
from sentiment import cleaner, summary, flairme, tickercount

sentiment_model = flair.models.TextClassifier.load('en-sentiment')


reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    user_agent=user_agent,
    username=username,
    password=password
)

today = date.today().strftime('%b-%d-%Y')
dirname = os.path.dirname(__file__)
reportpath = os.path.join(dirname, 'reports')

def parse_submission(submission):
    return {
        'title': submission.title,
        'created_utc': submission.created_utc,
        'selftext': submission.selftext,
        'score': submission.score,
        'id': submission.id
    }


def main():
    subreddit = reddit.subreddit('Stocks')
    brr = pd.DataFrame()
    print('Parsing Reddit..')
    for submission in tqdm(subreddit.new(limit=None)):
        brr = brr.append(parse_submission(submission), ignore_index=True)
    brr.to_pickle(f'{reportpath}/{today}-goes-brr.pkl')

    #brr = pd.read_pickle('reports/Jan-24-2022-goes-brr.pkl')#tester

    summary(brr)
    cleaner(brr)
    flairme(brr)
    tickercount(brr)
    print('done!')
    print(brr)
    brr.to_excel(f'{reportpath}/{today}-goes-brr.xlsx')
    brr.to_pickle(f'{reportpath}/{today}-goes-brr.pkl')

    return brr


if __name__ == '__main__':
    if str(reddit.user.me()) == username:
        try:
            main()
            print('money printer go brr🤑')
        except ValueError:
            print('money printer stuck📉')