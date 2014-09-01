import praw
import os
import time


usrAgnt = 'old comment cleanup. deployed to heroku 9.1.2014'
usr = os.environ['MAKER'] #username
pw = os.environ['MAKERpw'] #password

r = praw.Reddit(usrAgnt) 
r.login(usr,pw)

comments = r.user.get_comments()

#deletes comments in deleted posts, or <1 valued over 24 hours old. 
def should_delete(comment): 
    if comment.link_author == u'[deleted]':
        return True
    if comment.score<1:
        if (time.time()-comment.created_utc)>86400:
            return True
    else:
        return False

for comment in comments:
    if should_delete(comment):
            print "deleting comment."
            comment.delete()