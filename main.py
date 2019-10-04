#!/usr/local/Cellar/python3

import sys
import requests, json
from bs4 import BeautifulSoup
import praw
from datetime import datetime


def initBot():

    return praw.Reddit(user_agent='reddit-slack (by /u/kevnprns)',
                     client_id='CLIENT_ID', client_secret="CLIENT SECRET")

def getTopPost(reddit, endpoint):
    subreddit = reddit.subreddit(endpoint)

    for submission in subreddit.top('day',limit=1):
        return submission


def main(argv):
    if len(argv) < 2:
        print('usage: python main.py [subreddit to follow] [subreddit to follow] ...')
        sys.exit(1)

    # Parse command line args
    links = argv[1:]

    reddit = initBot()

    for link in links:
        topPost = getTopPost(reddit, link)

        print("\n*")
        print("Today's top post on 'r/" + link + "'")
        print("\tID: ", topPost.id)
        print("\tTitle: ", topPost.title)
        print("\tURL: ", topPost.url)
        print("\tDate Created(UTC): ", (datetime.utcfromtimestamp(topPost.created_utc).strftime('%Y-%m-%d %H:%M:%S')))

    print()

if __name__ == "__main__":
    main(sys.argv)
