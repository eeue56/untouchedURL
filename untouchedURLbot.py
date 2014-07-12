import praw
import time
import datetime

#setup

usrAgnt = 'untouchedURL bot 7.12.2014 checks new posts for mobile links | GITHUB'
usr = 'untouchedURL' 
pw = '' #password
maker = '' #account to pass feedback to

r = praw.Reddit(usrAgnt) 
r.login(usr,pw)

touchHint = {'.m.':'.','//m.':'//','/.compact':'/','//mobile.':'//','//touch.':'//'} #search terms and translations
ignoreDomains = ['mlb.com','m.memegen.com','m.braves.mlb.com','m.imgur.com','m.espn.go.com', 'm.mlb.com', 'm.youtube.com'] #these take care of themselves
ignoreSubreddits = []
processedPosts = []

feedbackURL = "[How am I doing?](http://www.reddit.com/message/compose/?to=untouchedURL&amp;subject=untouchedURL%20feedback)" 
feedbackSubject = u'untouchedURL feedback' 
sourcecodeURL = "[Sourcecode](https://github.com/Kharms/untouchedURL)"


def post_comment(post, commentTxt):
    global ignoreSubreddits
    try:
        a = post.add_comment(commentTxt)
        return True
    except Exception as e:
        warn("Comment Failed: %s @ %s in subreddit %s"%(commentTxt,post.permalink,post.subreddit))
        if str(e) == '403 Client Error: Forbidden':
            print '/r/'+post.subreddit+' has banned me.'
            ignoreSubreddits.append(post.subreddit)
        return False


running = True
runCount = 0


#bot:
while running:
#newPosts = r.get_new(limit=100)
    newPosts = r.get_subreddit('all').get_new(limit = 100)
    print "Scanning..."
#newPosts = r.get_subreddit('todayilearned').get_new(limit=1000)
    for post in newPosts:
        url = post.url.lower()
        if ((post.subreddit not in ignoreSubreddits) and (post.domain not in ignoreDomains)):
            if any(hint in url for hint in touchHint):
                if ((post.id not in processedPosts) and (post.over_18 == False)):
                    print '--------'
                    print datetime.datetime.utcnow()
                    print post.permalink
                    for hint, replacement in touchHint.items():
                        if hint in url:
                            newlink = post.url.replace(hint,replacement)
                            print post_comment(post,("Here is a non-mobile link: " + newlink + "\n \n" + feedbackURL + " | "+sourcecodeURL))
#r.send_message(maker,"test","Here is a non-mobile link: " + newlink + "\n \n" + feedbackURL)
#post.add_comment("Here is a non-mobile link: " + newlink + "\n \n" + feedbackURL)
                            processedPosts.append(post.id)
    time.sleep(20)
    runCount += 1
    if runCount == 90: 
        runCount = 0
        processedPosts = []
        mail = r.get_unread()
        for m in mail:
            if m.subreddit == None:
                if m.subject == feedbackSubject:
                    r.send_message(maker,m.subject,m.body)