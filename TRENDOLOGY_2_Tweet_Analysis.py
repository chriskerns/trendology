
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
# - This code assumes you have Pandas installed<br>
# 
# <br>
# My isn't perfect, but it works. Have fun with it, make it better. <BR><BR>
# 

# In[1]:

# IMPORT A FEW THINGS
import MySQLdb
from datetime import datetime as dt
import time
import pandas as pd
import numpy as np
from pandas import DataFrame, Series, date_range
import pandas.io.sql as psql
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import pylab as pylab


# In[2]:

# CONNECT TO YOUR DATABASE

mydb = MySQLdb.connect(host='#', user='#', passwd='#', db='#')
cursor = mydb.cursor()

varTableName = "#YOUR_TABLE_NAME#"


# In[3]:

#GET TWEETS FROM DB
varSQLAll = "SELECT * FROM " + varTableName
DFall = psql.frame_query(varSQLAll, con=mydb)
DFall['screenname'] = DFall['screenname'].str.lower()
print 'loaded dataframe from MySQL. records:', len(DFall)


# In[4]:


#GET ORGANIC TWEETS FROM DB
varSQLOrganic = "SELECT * FROM " + varTableName + " where tweettext not like '@%' and tweettext not like 'RT%'"
DForganic = psql.frame_query(varSQLOrganic, con=mydb)
DForganic['screenname'] = DForganic['screenname'].str.lower()
print 'loaded dataframe from MySQL. records:', len(DForganic)


# In[5]:

#GET @REPLIES FROM DB
varSQLAT = "SELECT * FROM " + varTableName + " WHERE TWEETTEXT LIKE '@%'"
DFAT = psql.frame_query(varSQLAT, con=mydb)
DFAT['screenname'] = DFAT['screenname'].str.lower()
print 'loaded dataframe from MySQL. records:', len(DFAT)


# In[6]:

#GET RTS FROM DB
varSQLRT = "SELECT * FROM " + varTableName + " WHERE TWEETTEXT LIKE 'RT%'"
DFRT = psql.frame_query(varSQLRT, con=mydb)
DFRT['screenname'] = DFRT['screenname'].str.lower()
print 'loaded dataframe from MySQL. records:', len(DFRT)


# In[7]:

#STATS FUNCTION

def mainstats(varDataframe):
    varMeanRT = varDataframe['retweet_count'].mean()
    varMedianRT = varDataframe['retweet_count'].median()
    varSTDRT = varDataframe['retweet_count'].std()
    varRTsPer = varDataframe['rtsperfollower'].mean()
    varSTDRTsPer = varDataframe['rtsperfollower'].std()
    
    varMeanFav = varDataframe['favorites_count'].mean()
    varMedianFav = varDataframe['favorites_count'].median()
    varSTDFavs = varDataframe['favorites_count'].std()
    varFavsPer = varDataframe['favsperfollower'].mean()
    varSTDFavsPer = varDataframe['favsperfollower'].std()
    
    print "Tweet count: " + str(len(varDataframe))
    print ""
    print "RETWEET STATS:"
    print "--------------"
    print "Average RTs: " + str(varMeanRT)
    print "Median RTs: " + str(varMedianRT)
    print "Average RTs/Follower: " + '%f' % varRTsPer
    print ""
    print "FAVORITES STATS:"
    print "--------------"
    print "Average Favs: " + str(varMeanFav)
    print "Median Favs: " + str(varMedianRT)
    print "Average Favs/Follower: " + '%f' % varFavsPer
    print ""
    
    return varMeanRT, varMedianRT, varRTsPer, varMeanFav, varMedianFav, varFavsPer


# In[8]:

#GRAB STATS FOR ALL TWEETS
mainstats(DFall)


# In[9]:

#GRAB STATS FOR ORGANIC TWEETS (NON-RT, NON-@REPLIES)
varOrganic = mainstats(DForganic)


# In[10]:

#GRAB STATS FOR RETWEETS
mainstats(DFall.loc[DFall['tweettext'].str.startswith("RT")])


# In[11]:

#GRAB STATS FOR @REPLIES
mainstats(DFall.loc[DFall['tweettext'].str.startswith("@")])


# In[12]:

#TOP 10 AND BOTTOM 10 RETWEETING SCREENNAMES FROM YOUR DATASET (AS A PERCENT OF LAST 3,200 TWEETS)

varTopRTs = DFall.loc[DFall['tweettext'].str.startswith("RT")].groupby('screenname').tweettext.nunique()
varAll = DFall.groupby('screenname').tweettext.nunique()
varRatio = (varTopRTs/varAll).order(ascending=False)

print varRatio[:10]
print ""
print varRatio[-10:]


# In[13]:

#TOP10 AND BOTTOM 10 @REPLY SCREENNAMES FROM YOUR DATASET (AS A PERCENT OF LAST 3,200 TWEETS)

varTopReplies = DFall.loc[DFall['tweettext'].str.startswith("@")].groupby('screenname').tweettext.nunique()
varAll = DFall.groupby('screenname').tweettext.nunique()
varRatio = (varTopReplies/varAll.astype(float)).order(ascending=False)

print varRatio[:10]
print ""
print varRatio[-10:]


# In[16]:

#RTs and FAVS CORRELATION
DForganic['retweet_count'].corr(DForganic['favorites_count'])


# That's it, just some basic analysis functionality.
# 
# If you're having problems with the code or just want to chat, ping me at chris@chris-kerns.com
# 
# Happy coding! Go make something awesome.
# 
