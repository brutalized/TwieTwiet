#!/usr/bin/python3

import sys
import json
from collections import namedtuple
from operator import attrgetter

class Tweets():
    ''' Class to read out a specified number of tweets '''

    def __init__(self):
        self.twitterData = self.getTwitterData()


    def getTwitterData(self):
        ''' Gets Twitter JSON data for a specific period '''
        # todo read latest data directly from ssh or other means
        
        data = open('./sampledata/20150311_12.out')
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

        tweets = []
        if(showRawData): 
            for n in range(start, stop):
                tweets.append(self.twitterData[n])
        else:
            tweet = namedtuple('tweet', 'date, message, userName, userImage, userPopularity')
            for n in range(start, stop):
                tweets.append(tweet(self.twitterData[n]['created_at'],
                                    self.twitterData[n]['text'],
                                    self.twitterData[n]['user']['name'],
                                    self.twitterData[n]['user']['profile_image_url'],
                                    int(self.twitterData[n]['user']['followers_count'])))         
            tweets = self.doRank(tweets)
            
        return tweets

    def doRank(self, tweets):
        ''' Do some filtering and ranking '''
        # need to add more filtering
        return sorted(tweets, key=attrgetter('userPopularity'), reverse=True)

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
    tweets = tester.getTweets()
    print(tweets[0])
    print('\n\nEnd of tester')

if __name__ == "__main__":
    tester()



    
    
