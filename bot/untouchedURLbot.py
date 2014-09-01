import praw
import time
import datetime
import warnings
import requests
import os
#setup


usrAgnt = 'untouchedURL bot deployed 9.1.2014 checks new posts for mobile links | running on Heroku'
usr = 'untouchedURL' 
pw = os.environ['botPW'] #password
maker = os.environ['MAKER'] #reddit account to pass feedback to


logged_in = 0

while logged_in == 0:
    try:
        r = praw.Reddit(usrAgnt) 
        r.login(usr,pw)
        logged_in = 1
    except Exception as e: ##if exception not other, find out what kind
        print '!!!!!!LOG IN EXCEPTION!!!!!!'
        print(type(e))
        sleep(30)
        


#sets request user agent to desktop sasfari, turns of cache-ing.
request_headers = {'User-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.78.2 (KHTML, like Gecko) Version/7.0.6 Safari/537.78.2','Cache-Control': 'no-cache'}
session = requests.Session()
session.headers = request_headers

touchHint = {'.m.':'.','//m.':'//','/.compact':'/','//mobile.':'//','//touch.':'//'} #search terms and translations

ignoreDomains = {'mlb.com','m.memegen.com','m.braves.mlb.com','m.imgur.com','m.espn.go.com', 'm.mlb.com', 'm.youtube.com', 'm.politico.com', 'm.wpbf.com','m.huffpost.com','m.bleacherreport.com','m.btownthings.com','m.bbc.com', 'mobile.gungho.jp','m.vice.com','m.eet.com', 'm.tigerdirect.com'} #these take care of themselves/are broken
processDomains = {'en.m.wikipedia.org'} #domain whitelist
ignoreSubreddits = set([u'latterdaysaints', u'politics',u'WTF',u'gats',u'NBA'])
processedPosts = set()

feedbackURL = "^[Feedback?](http://www.reddit.com/message/compose/?to=untouchedURL&amp;subject=untouchedURL%20feedback)" 
feedbackSubject = u'untouchedURL feedback' 
sourcecodeURL = "^[Sourcecode](https://github.com/Kharms/untouchedURL)"



        
def get_last_redirect(url_head): #follows redirects, returns last requests.response object
    redirects = session.resolve_redirects(url_head,url_head.request)
    last_redirect = url_head
    for last_redirect in redirects:
        pass
    return last_redirect
    

def get_mobile_url(mobile_url):
    mobile_url_head = session.head(mobile_url)
    last_redirect = get_last_redirect(mobile_url_head)
    return last_redirect.url

#extracomment
#posts comment.
def post_comment(post, commentTxt, ignoreSubreddits):
    try:
        a = post.add_comment(commentTxt)
        return True
    except Exception as e:
        warnings.warn("Comment Failed: %s @ %s in subreddit %s"%(commentTxt,post.permalink,post.subreddit))
        if str(e) == '403 Client Error: Forbidden':
            print '/r/',post.subreddit,' has banned me.'
            ignoreSubreddits.add(post.subreddit.display_name)
        return False



#checks to see if we can skip post

def check_post(post, ignoreDomains, ignoreSubreddits, processedPosts):
    if post.over_18:
        return False
    if post.is_self:
        return False
    if post.subreddit.display_name in ignoreSubreddits:
        return False
    if post.domain in ignoreDomains:
        return False
    if post.id in processedPosts:
        return False
    else:
        return True
        
#requests module found at: http://stackoverflow.com/questions/1140661/python-get-http-response-code-from-a-url   



     
#Checks domain to see if it is in processDomains, if not, checks to see if fix returns 404. If it does, adds to ignoreDomains, else adds to processDomains.
def check_domain(newlink,domain,ignoreDomains,processDomains):
    if domain in processDomains:
        return True
    else:
        try:
            url_head = session.head(newlink)
            status = url_head.status_code
            if status == 404:
                ignoreDomains.add(domain)
                return False
            if status == 400:
                ignoreDomains.add(domain)
                return False
            if (status > 299) and (status<400):
                last_redirect = get_last_redirect(url_head)
                #if last_redirect.status_code = 404:
                    #ignoreDomains.add(domain)
                    #return false
                if last_redirect.status_code == 200:
                    processDomains.add(domain)
                    return True
                else:
                    ignoreDomains.add(domain)
                    return False
            if status == 200:
                processDomains.add(domain)
                return True
            else:
                return False    
        except requests.ConnectionError:
            print "failed to connect"
            return False



####TODO: check_domain to check the mobile URL for redirect to non-mobile site. Pass "post" instead of "post.domain"


running = True
runCount = 0
comments_posted = 0



#bot:
while running:
#newPosts = r.get_new(limit=100)
    print "getting posts..."
    newPosts = r.get_subreddit('all').get_new(limit = 100)
    print "Scanning posts..."
#newPosts = r.get_subreddit('todayilearned').get_new(limit=1000)
    try:
        for post in newPosts:
            if check_post(post,ignoreDomains,ignoreSubreddits,processedPosts):
                url = post.url.lower()
                processedPosts.add(post.id)
                if any(hint in url for hint in touchHint): #checks if mobile URL
                    url = get_mobile_url(url) #checks for auto-redirect from mobile URL
                    if any(hint in url for hint in touchHint): #replaces hints, checks new url, posts comment.
                        for hint, replacement in touchHint.items():
                            if hint in url:
                                newlink = post.url.replace(hint,replacement)
                        if check_domain(newlink,post.domain,ignoreDomains,processDomains):
                            comments_posted +=1
                            post_comment(post,("Here is a non-mobile link: " + newlink + "\n \n" + sourcecodeURL + " ^| "+feedbackURL),ignoreSubreddits)
    # except socket.timeout as sock_time:
    #     print '!!!!TIME.OUT'
    #     print sock_time
    # except Other as other:
    #     print '!!!!Timed out.???'
    #     print other
    except Exception as e: ##if exception not other, find out what kind
        print '!!!!!!EXCEPTION!!!!!!'
        print(type(e))
    time.sleep(15)
    runCount += 1
    if runCount == 1440: 
        sleep(90) #sleep: to avoid repeats at the expense of missing some.
        runCount = 0
        processedPosts = set()
        mail = r.get_unread()
        print "processDomains: ", processDomains
        print "ignoreDomains: ", ignoreDomains
        print "ignoreSubreddits: ", ignoreSubreddits
        print "comments posted: ",comments_posted
        comments_posted = 0
        for m in mail:
            if m.subreddit == None:
                if m.subject == feedbackSubject:
                    m.mark_as_read()
                    r.send_message(maker,m.subject,m.body)      
                    
                    
                    #r.send_message(maker,"test","Here is a non-mobile link: " + newlink + "\n \n" + feedbackURL)
                    #post.add_comment("Here is a non-mobile link: " + newlink + "\n \n" + feedbackURL)