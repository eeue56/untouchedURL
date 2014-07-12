This is a reddit bot that scans for new posts in reddit.com/r/new and checks for mobile URLs. If it finds them, it adds a comment with a non-mobile URL.

Alternate approach: user get_new() on reddit instance, use subreddit subscriptions to control what it scans.

Todo: create an automated way for moderators to blacklist their subreddit.

resources used: 

https://github.com/praw-dev/praw
https://github.com/acini/praw-antiabuse-functions/blob/master/anti-abuse.py
