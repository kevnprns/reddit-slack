# reddit-slack

## Description

This project is meant to be used as a slack app integration. It pulls the Top Daily post from the specified subreddit and submits the post to the slack hook that is specified by the user.

## Pre-execution

Firstly you will want to install the python libraries using:
'pipenv install'

For use of this app you will need to get reddit Client ID and Client Secret. Here is a tutorial on how to get those:
https://github.com/reddit-archive/reddit/wiki/OAuth2

You will also require to get a Slack API hook for your slack. Here are the steps to do that:
https://slack.com/intl/en-ca/help/articles/115005265063-incoming-webhooks-for-slack

## Execution

python3 main.py [excluded file path] [slack api hook] [subreddit to follow] [subreddit to follow]...

The excluded file path is used to blacklist any submission that has already been posted on your slack to ensure doubles aren't posted.

## Future Upscaling

* Make the timespan dynamic so that the user can select the viewing window for the top post. (hour, week, month, year, all)
* Finish new post loop to always keep pulling the latest submission from the subreddit as soon as its posted.
