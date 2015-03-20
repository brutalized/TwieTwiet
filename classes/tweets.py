#!/usr/bin/python3

import sys
import json
from collections import namedtuple
from operator import attrgetter

# Todo:
# Refactor

class Tweets():
    ''' Class to read out a specified number of tweets '''

    def __init__(self):
        self.twitterData = self.getTwitterData()

    def getTwitterData(self):
        ''' Gets Twitter JSON data for a specific period '''
        # todo read latest data directly from ssh or other means
        
        data = open('./sampledata/20150311_12.out',mode='r',encoding='utf-8')
        twitterData = []
        for line in data:
            try:
                twitterData.append(json.loads(line))
            except ValueError as errorMessage:
                print('Tweet parse error: "' + str(errorMessage) + '"', file=sys.stderr)
                continue

        return twitterData


    def getTweets(self, start = 0, stop = False, showRawData=False):
        ''' Get a number of tweets from the database '''

        if(stop == False):
            stop = len(self.twitterData)

        self.tweets = []
        if(showRawData): 
            for n in range(start, stop):
                self.tweets.append(self.twitterData[n])
        else:
            # https://dev.twitter.com/overview/api/tweets
            Tweet = namedtuple('Tweet', 'date, message, userName, userImage, userPopularity')
            for n in range(start, stop):
                #if(self.doFilter(self.twitterData[n])):
                #    continue
                
                self.tweets.append(Tweet(self.twitterData[n]['created_at'],
                                    self.twitterData[n]['text'],
                                    self.twitterData[n]['user']['name'],
                                    self.twitterData[n]['user']['profile_image_url'],
                                    int(self.twitterData[n]['user']['followers_count'])))         
            self.tweets = self.doRank(self.tweets)
            
        return self.tweets

    def doRank(self, tweets):
        ''' Do some filtering and ranking '''
        # need to add more filtering
        return sorted(tweets, key=attrgetter('userPopularity'), reverse=True)

    def doFilter(self, tweet):
        ''' Checks if the tweet must be filtered from results. Returns True if it does '''
        pass # moved to seperate class


def tester():
    import os
    os.chdir(os.path.dirname('../'))
    print('Initializing database..')
    tester = Tweets()
    print('Database init finished.')
    print('\nPrinting first raw tweet:\n')
    for tweet in tester.getTweets(0,1,True):
        print(json.dumps(tweet, sort_keys=True, indent=4, separators=(',', ': ')))
    print('\n\nPrinting first default and ranked tweet:\n')
    print(len(tester.getTweets(showRawData=True)))
    print(len(tester.getTweets()))
    tweets = tester.getTweets()
    try:
        print(tweets[0])
    except:
        print('Error: No tweets found!')
    print('\n\nEnd of tester')

if __name__ == "__main__":
    tester()
