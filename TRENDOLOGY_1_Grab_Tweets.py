
# coding: utf-8

# Hello.<br><br>
# This is the code that was used while writing the book:

## Trendology

#### Building an Advantage through Data-Driven Real-Time Marketing 

# by Chris Kerns<br><br>
# You can find the book here: http://www.amazon.com/Trendology-Advantage-Data-Driven-Real-Time-Marketing/dp/1137479558
# <br>
# You can learn more about me and my latest data analysis here:
# http://chris-kerns.com
# <br>
# and you can find more code from the book here:
# http://github.com/chriskerns
# <br><br>
# Prereqs:<br>
# - This code assumes you have Python and a local MySQL database installed on your machine<br>
# - You'll also need to install Python-Twitter (https://code.google.com/p/python-twitter/)<br>
# - And sign up for a Twitter developer account (it's eay, free, and takes 2 minutes - https://dev.twitter.com/)<br>
# 
# <br>
# My code isn't perfect, but it works. Have fun with it, make it better. <BR><BR>

# In[1]:


# THIS CODE WORKS WITH THE FOLLOWING MYSQL TABLE STRUCTURE:

'''
CREATE TABLE `###YOUR_TABLE_NAME_HERE###` (
  `tweettext` varchar(500) DEFAULT NULL,
  `screenname` varchar(100) DEFAULT NULL,
  `retweet_count` int(11) DEFAULT NULL,
  `favorites_count` int(11) DEFAULT NULL,
  `tweet_created` datetime DEFAULT NULL,
  `tweet_id` bigint(20) DEFAULT NULL,
  `followers` int(11) DEFAULT NULL,
  `rtsperfollower` decimal(12,10) DEFAULT NULL,
  `favsperfollower` decimal(12,10) DEFAULT NULL
)
'''


# In[2]:

# IMPORT A FEW THINGS
import twitter
import MySQLdb
import datetime
import time

# CONNECT TO THE TWITTER API
CONSUMER_KEY = '#YOUR_TWITTER_API_CONSUMER_KEY#'
CONSUMER_SECRET = '#YOUR_TWITTER_API_CONSUMER_SECRET#'
ACCESS_TOKEN = '#YOUR_TWITTER_API_ACCESS_TOKEN#'
ACCESS_TOKEN_SECRET = '#YOUR_TWITTER_API_ACCESS_TOKEN_SECRET#'

api = twitter.Api(consumer_key=CONSUMER_KEY,
    consumer_secret=CONSUMER_SECRET,
    access_token_key=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET)


# In[3]:

# CONNECT TO YOUR DATABASE

mydb = MySQLdb.connect(host='#YOURHOST$', user='#USER#', passwd='#PASSWORD#', db='#DB#')
cursor = mydb.cursor()


# In[ ]:

# SET COUNTERS. THESE MAKE SURE WE STAY WITHIN THE TWITTER API REQUEST LIMITS

varAPICounter = 0
varAPILimit = 15

# SET DATABASE TABLE NAME AND YOUR LIST OF TWITTER SCREENNAMES YOU WANT TO PULL DATA FOR.
# YOU CAN ADD AS MANY SCREENNAMES AS YOU LIKE

varTextTable = "#YOUR_DATABASE_TABLE"

varList = ['#TWITTER_SCREENNAME_1#','#TWITTER_SCREENNAME_2#','#TWITTER_SCREENNAME_3#','#ETC#']


# In[ ]:

#GRAB THE LAST 3200 TWEETS FROM EACH SCREENNAME IN varList

# varCounter TELLS THE CODE IF THIS IS THE FIRST CALL FOR A GIVEN SCREENNAME. THE LOGIC IS A BIT DIFFERENT
# FOR THE FIRST CALL VS. SUBSEQUENT CALLS

varCounter = 0
varMaxID = 0

for varBrand in varList:
    
    while varCounter < 16:
        
        if varAPICounter == varAPILimit:
            now = datetime.datetime.now()
            infifteen = now + datetime.timedelta(seconds=910)
            print "Hit the rate limit. API pinging will resume in 15 minutes, at: " + str(infifteen)
            time.sleep(910)
            varAPICounter = 0
            
        if varCounter == 0:
            varCounter = varCounter + 1
            varAPICounter = varAPICounter + 1
            print "varAPICounter:" + str(varAPICounter) + ", varCounter:" + str(varCounter) + " varMaxID:" + str(varMaxID)                 + ", screenname:" + varBrand
            try:
                user_timeline=api.GetUserTimeline(screen_name=varBrand, count=200)
                print "API call successful"
            except:
                print "API call error"
                continue
        else:
            varCounter = varCounter + 1
            varAPICounter = varAPICounter + 1
            print "varAPICounter:" + str(varAPICounter) + ", varCounter:" + str(varCounter) + " varMaxID:" + str(varMaxID)                 + ", screenname:" + varBrand
            try:
                user_timeline=api.GetUserTimeline(screen_name=varBrand, count=200, max_id=varMaxID)
                print "API call successful"
            except:
                print "API call error"
                continue
                
        for tweet in user_timeline:
            varSQL = "SELECT * FROM " + varTextTable + " WHERE tweet_id = %s" % tweet.id   
            cursor.execute(varSQL)
            varReturn = cursor.fetchall()
            
            if varReturn:
                #print "ID exists"
                tweetID = long(tweet.id)
            else:
                tweetID = long(tweet.id)
                tweetText = tweet.text
                tweetText = tweetText.encode('ascii','ignore').replace("'","").replace("\\","")
                created_at = tweet.created_at
                time_struct = time.strptime(created_at, "%a %b %d %H:%M:%S +0000 %Y")#Tue Apr 26 08:57:55 +0000 2011
                created_at_new = datetime.datetime.fromtimestamp(time.mktime(time_struct))
                retweetCount = tweet.retweet_count
                favoritesCount = tweet.favorite_count
                followersCount = tweet.user.followers_count
                varRTsper = (retweetCount/float(followersCount))
                varFavsper = (favoritesCount/float(followersCount))
                varSQLInsert = "INSERT INTO " + varTextTable + "(tweettext, screenname, retweet_count,                    favorites_count, tweet_created, tweet_id, followers, rtsperfollower, favsperfollower)                    VALUES('%s','%s',%s, %s, '%s', %s, %s, %s, %s) " %                     (tweetText, varBrand, retweetCount, favoritesCount, created_at_new, tweetID, followersCount, varRTsper, varFavsper)
                cursor.execute(varSQLInsert)
            varMaxID = tweetID
        mydb.commit()
        
    varCounter = 0
    varMaxID = 0
    


# In[ ]:

#THAT'S IT - YOU SHOULD NOW HAVE A DATABASE FULL OF TWEETS TO ANALYZE


# If you're having problems with the code or just want to chat, ping me at chris@chris-kerns.com
# 
# Happy coding! Go make something awesome.
# 
# /chris

# In[ ]:



