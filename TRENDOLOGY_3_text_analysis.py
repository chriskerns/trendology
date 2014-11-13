
# coding: utf-8

# Hello.<br><br>
# This is the code that was used while writing the book:
# 

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
# - This code assumes you have a database table full of Tweets, as created in the "TRENDOLOGY_1_Grab_Tweets" script also located in this folder
# 
# <br>
# My code isn't perfect, but it works. Have fun with it, make it better. <BR><BR>
# 

# In[16]:

# IMPORT A FEW THINGS
import MySQLdb
import datetime
import time
import nltk
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from nltk import bigrams, text
from nltk.collocations import *
import string
import matplotlib.pyplot as plt

mydb = MySQLdb.connect(host='###ADD YOURS HERE###', user='###ADD YOURS HERE###', passwd='###ADD YOURS HERE###', db='###ADD YOURS HERE###')
cursor = mydb.cursor()


# In[17]:

# SET DATABASE TABLE NAME

varTableName = '##YOUR_DB_TABLE_NAME###'


# In[18]:

# CREATE AN EXCLUDE LIST
# THIS COULD BE FOR SCREENNAMES THAT POP UP A LOT OR JUST WORDS THAT ARE MESSING WITH YOUR ANALYSIS THAT YOU
# DON'T CARE ABOUT. A GOOD THING TO HAVE FOR YOUR 2ND, 3RD RUN THROUGH THIS ANALYSIS AS YOU REFINE.

varExclude = ['#remove me#']


# In[19]:


#SAMPLE SQL TO GET ONLY TEXT FROM ORIGINAL BRAND TWEETS, NO RETWEETS OR @REPLIES
varSQL = "select tweettext from " + varTableName + " where tweettext not like 'RT%' and tweettext not like '@%'"

'''

#OTHER SAMPLE SQL STATEMENTS:

#SAMPLE SQL TO GET ONLY TEXT FROM RETWEETS
varSQL = "select tweettext from " + varTableName + " where tweettext like 'RT%'"

#SAMPLE SQL TO GET ONLY TEXT FROM @REPLIES
varSQL = "select tweettext from " + varTableName + " where tweettext like '@%'"
'''

cursor.execute(varSQL)
varReturn = cursor.fetchall()


# In[20]:

#CREATE ONE BIG STRING FROM ALL TWEETS IN DB

varMegaString = ""

for item in varReturn:
    varMegaString = varMegaString + " " + str(item[0])
    
varMegaString = varMegaString.translate(None, string.punctuation)


# In[21]:

#TOKENIZE - SEPARATE OUT INDIVIDUAL WORDS
#THIS STEP MAY TAKE A BIT OF TIME. GRAB A COFFEE. CALL AN OLD FRIEND.

varMegaTokens = nltk.word_tokenize(varMegaString)

#REMOVE ACTUAL MENTIONS OF 'RT' AND 'MT' - WE DON'T THOSE EVEN WHEN LOOKING AT RETWEETS
#WE ALSO WANT TO GET RID OF URLS AND LINKS, UNLESS YOU CARE ABOUT THOSE

varMegaTokens = [x for x in varMegaTokens if x != "RT"]
varMegaTokens = [x for x in varMegaTokens if x != "MT"]
varMegaTokens = [x for x in varMegaTokens if not x.startswith("http")]
varMegaTokens = [x for x in varMegaTokens if not x.startswith("tco")]

#REMOVE STOP WORDS - SMALL WORDS THAT YOU PROBABLY DON'T CARE ABOUT
varMegaFiltered0 = [item for item in varMegaTokens if not item.lower() in stopwords.words('english')]


# In[24]:

#FUNCTION FOR WORD FREQUENCY ON SINGLE TERMS - MOST FREQUENTLY USED WORDS FUNCTION

def freqSingle(list):
    global nouns
    global adjectives
    
    #fig, axs = plt.subplots(1,2)

    varPOS = [nltk.pos_tag(list)] 
    
    ##################################################
    #ALL LANGUAGE - FREQUENCY
    varAll = FreqDist(list)
    
    ##USE THIS TO PRINT THE TOP WORDS
    print "TOP TERMS"
    varAll_common = varAll.most_common(25)
    print varAll_common
    print ""
    
    #PLOT TOP TERMS
    #varAll.plot(25, cumulative=False, title='All Language')
    #plt.show()
    
    ##################################################
    #NOUNS - FREQUENCY
    nouns = []
    for word,pos in varPOS[0]:
        if pos in ['NN', 'NNP']:
            nouns.append(word)
    varNouns = FreqDist(nouns)

    ##USE THIS TO PRINT THE TOP NOUNS
    print "TOP NOUNS"
    varNouns_common = varNouns.most_common(25)
    print varNouns_common
    print ""
    
    #PLOT TOP NOUNS
    #varNouns.plot(25, cumulative=False, title='Nouns')
    #plt.show()
    
    ##################################################
    #ADJECTIVES - FREQUENCY
    adjectives = []
    for word,pos in varPOS[0]:
        if pos in ['JJ', 'JJR', 'JJS']:
            adjectives.append(word)
    varAdjectives = FreqDist(adjectives)
    
    
    ##USE THIS TO PRINT THE TOP ADJECTIVES
    print "TOP ADJECTIVES"
    varAdjectives_common = varAdjectives.most_common(25)
    print varAdjectives_common
    print ""
    
    #PLOT TOP ADJECTIVES
    #varAdjectives.plot(25, cumulative=False, title='Adjectives')
    #plt.show()
    
    #YOU CAN ADD OTHER PARTS OF SPEECH. VISIT WWW.NLTK.ORG FOR DOCUMENTATION
    
    


# In[25]:

#CALL THE SINGLE TERM FREQUENCY FUNCTION

freqSingle(varMegaFiltered0)


# In[32]:

#BIGRAMS - TERMS FREQUENTLY OCCURRING TOGETHER (COMMON PHRASES) FUNCTION

def freqBigram(list):
    varBigramsFreq = nltk.FreqDist(nltk.bigrams(list))
    
    ##USE THIS TO PRINT THE TOP ADJECTIVES
    print "TOP TWO WORD PHRASES"
    varBigrams_common = varBigramsFreq.most_common(25)
    print varBigrams_common
    print ""
    
    #varBigramsFreq.plot(25, cumulative=False, title="Bigrams")
    


# In[33]:

#CALL THE BIGRAM FUNCTION

freqBigram(varMegaFiltered0)


# In[ ]:

# THAT'S IT. PLAY AROUND WITH DIFFERENT PARTS OF SPEECH, AND DIFFERENT SQL QUERIES
# WHICH WILL GET YOU DIFFERENT SLICES OF TWEET TEXT. 
# EX: PULL ONLY THE TOP PERFORMING TWEETS VIA YOUR SQL QUERY 
# AND SEE HOW THOSE DIFFER FROM LOW PERFORMERS.


# If you're having problems with the code or just want to chat, ping me at chris@chris-kerns.com
# 
# Happy coding! Go make something awesome.
# 
# /chris
