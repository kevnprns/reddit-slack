#!/usr/local/Cellar/python3

import os
import sys
import requests, json
import praw
from datetime import datetime

class RedditCrawler:
    """docstring for RedditCrawler."""

    class Post:
        """Create a value object to hold the contents of the post."""

        def __init__(self, id='', msg='', title='', img_url=''):
            self.id = id
            self.msg = msg
            self.title = title or ''
            self.img_url = img_url

        def format(self):
            # Description: Formats the information for the POST body.
            return '{ "text": "%s", "attachments": [ { "text": "%s", "image_url": "%s" } ] }' % (self.msg, self.title, self.img_url,)

        def send(self, hook):
            # Description: Posts message to the slack using the hook setup at <workspace>.slack.com
            body = self.format()

            r = requests.post(hook, headers={'Content-Type': 'application/json'}, data=body.encode('utf-8'))

    def __init__(self, links, appID=None, appSecret=None, excludedFile='.reddit_slack', slackHook=None):
        self.excluded_dictionary = {}

        self.appID = appID
        self.appSecret = appSecret
        self.excludedFile = excludedFile
        self.links = links
        self.slackHook = slackHook
        self.reddit = self._initReddit()

    def _initReddit(self):
        # Description: Creates a praw instance for the reddit API usage
        return praw.Reddit(user_agent='reddit-slack (by /u/kevnprns)',
                         client_id=self.appID, client_secret=self.appSecret)

    def _readFile(self):
        # Description: Loads the excluded posts into the program
        try:
            with open(self.excludedFile, 'r') as file:
                self.excluded_dictionary = json.loads(file.read())
                file.close()
        except: pass

    def _writeFile(self):
        # Description: Writes the updated dictionary to the file
        with open(self.excludedFile, 'w') as file:
            self.excluded_dictionary['updated'] = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            file.write(json.dumps(self.excluded_dictionary))
            file.close()

    def _excludeSubmission(self, subreddit, id):
        # Description: Returns whether or not the post has already been sent to the slack hook
        self.excluded_dictionary['mostRecentPost'] = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        if self.excluded_dictionary.get(subreddit, None) is None:
            self.excluded_dictionary[subreddit] = []

        self.excluded_dictionary[subreddit].append(id)

    def _isSafeSubmission(self, subreddit, id):
        # Description: Returns whether or not the post has already been sent to the slack hook
        excludedList = self.excluded_dictionary.get(subreddit, None)

        if excludedList is None:
            return True

        return not id in excludedList

    def _getTopPost(self, timespan='day', endpoint=''):
        # Description: Gets the top post in the selected timespan(hour, day, week, month, year, all)
        subreddit = self.reddit.subreddit(endpoint)

        for submission in subreddit.top(timespan, limit=1):
            return submission

    def newPostsLoop(self, endpoint):
        # Description: Loop that keeps searching and uploading every new submission from the subreddit
        subreddit = reddit.subreddit(endpoint)

        for submission in subreddit.stream.submissions():
            # TODO: link slack functionality instead of just printing
            self.printSuccess(endpoint, submission)

    def printSuccess(self, endpoint, submission):
        print("\n*")
        print("Successful Submission from 'r/" + endpoint + "'")
        print("\tID: ", submission.id)
        print("\tTitle: ", submission.title)
        print("\tURL: ", submission.url)
        print("\tDate Created(UTC): ", (datetime.utcfromtimestamp(submission.created_utc).strftime('%Y-%m-%d %H:%M:%S')))
        print()

    def start(self):
        self._readFile()

        for link in self.links:

            topPost = self._getTopPost("day", link)

            if self._isSafeSubmission(link, topPost.id):

                message = "Today's Top Post on r/"+ link +":"
                newPost = self.Post(id=topPost.id, msg=message, title=topPost.title, img_url=topPost.url)
                newPost.send(hook=self.slackHook)
                self._excludeSubmission(link, topPost.id)
                self.printSuccess(endpoint, topPost)
            else:
                print("ERROR: Submission has already been posted: " + topPost.id)

        self._writeFile()

def main(argv):
    if len(argv) < 2:
        print('usage: python main.py [excluded file path] [slack api hook] [subreddit to follow] [subreddit to follow] ...')
        sys.exit(1)

    # Parse command line args
    excludedFile = argv[1]
    slackHook = argv[2]
    links = argv[3:]

    # environment variables for reddit API usage
    appID = os.environ.get('REDDITID')
    appSecret = os.environ.get('REDDITSECRET')

    redditBot = RedditCrawler(appID=appID, appSecret=appSecret, excludedFile=excludedFile, links=links, slackHook=slackHook)

    redditBot.start()

if __name__ == "__main__":
    main(sys.argv)
