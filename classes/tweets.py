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
        
        data = open('./sampledata/20150311_12.out',mode='r',encoding='utf-8')
        twitterData = []
        for line in data:
            try:
                twitterData.append(json.loads(line))
            except ValueError as errorMessage:
                print('Tweet parse error: "' + str(errorMessage) + '"', file=sys.stderr)
                continue

        return twitterData


    def getTweets(self, start = 0, stop = False):
        ''' Get a number of tweets from the database '''

        if(stop == False):
            stop = len(self.twitterData)

        # Field specification from Twitter JSON:
        # https://dev.twitter.com/overview/api/tweets
        Tweet = namedtuple('Tweet', 'date, message, userName, userImage, userPopularity')
        self.tweets = []
        for n in range(start, stop):
            self.tweets.append(Tweet(self.twitterData[n]['created_at'],
                                self.twitterData[n]['text'],
                                self.twitterData[n]['user']['name'],
                                self.twitterData[n]['user']['profile_image_url'],
                                int(self.twitterData[n]['user']['followers_count'])))

        return sorted(self.tweets, key=attrgetter('userPopularity'), reverse=True)
    

def tester():
    import os
    os.chdir(os.path.dirname('../'))
    print('Initializing database..')
    tester = Tweets()
    print('Database init finished.')
    print('\nPrinting tweet:\n')
    for tweet in tester.getTweets(0,1):
        print(tweet)
    print('\n\nEnd of tester')

if __name__ == "__main__":
    tester()
