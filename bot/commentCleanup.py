import praw
import os
import time


userAgent = 'untouchedURL old comment cleanup. heroku 7.14.2014'
user = 'untouchedURL' 
password = os.environ['botPW'] #password

r = praw.Reddit(userAgent) 
r.login(user, password)

comments = r.user.get_comments()

def should_delete(comment):
    if comment.link_author == u'[deleted]':
        return True

    if comment.score < 1:
        if (time.time() - comment.created_utc) > 3600:
            return True
    return False

for comment in comments:
    if should_delete(comment):
            print "deleting comment."
            comment.delete()
