import pandas as pd
import praw
from config import *
from datetime import date
import os

reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    user_agent=user_agent,
    username=username,
    password=password
)

today = date.today().strftime('%b-%d-%Y')
dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, 'reports')

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
    for submission in subreddit.new(limit=None):
        brr = brr.append(parse_submission(submission), ignore_index=True)
    brr.to_pickle(f'{filename}/{today}-goes-brr.pkl')


if __name__ == '__main__':
    if str(reddit.user.me()) == username:
        try:
            main()
            print('money printer go brr🤑')
        except ValueError:
            print('money printer stuck📉')