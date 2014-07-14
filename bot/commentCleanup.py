import praw
import os
import time


usrAgnt = 'untouchedURL old comment cleanup. heroku 7.14.2014'
usr = 'untouchedURL' 
pw = '' os.environ['botPW'] #password
maker = os.environ['MAKER'] #reddit account to pass feedback to

r = praw.Reddit(usrAgnt) 
r.login(usr,pw)

comments = r.user.get_comments()

def should_delete(comment):
    if comment.link_author == u'[deleted]':
        return True
    if comment.score<1:
        if (time.time()-comment.created_utc)>3600:
            return True
    else:
        return False

for comment in comments:
    if should_delete(comment):
            comment.delete()
            