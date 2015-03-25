#!/usr/bin/python3

import sys
import json
import gzip
import datetime
import time
import re
import os.path
from collections import namedtuple
from operator import attrgetter
from classes.filter import Filter

class Tweets:
	''' Class to initialize the Tweets set to use for Rhyme making '''

	def __init__(self, start = 0, stop = False):
		self.twitterData = self.__getTwitterData(start, stop)

	def __getTwitterData(self, start, stop):
		''' Gets all the Twitter data from two hours ago (or is not available use fallback data) and make it a JSON set '''

		dt = datetime.datetime.now()
		filename = '/net/corpora/twitter2/Tweets/{0}/{1:02d}/{0}{1:02d}{2:02d}:{3:02d}.out.gz'.format(dt.year, dt.month, dt.day, dt.hour-2)
		
		if not os.path.isfile(filename):
			# Use fallback demodata, user is outside LWP')
			filename = 'demodata.gz'
		
		if not os.path.isfile(filename):
			print('Error:\nCould not find any Twitter data. Please put demodata.out.gz in the root map, or use the program on the LWP', file=sys.stderr)
			exit(-1)			

		data = gzip.open(filename)
		
		twitterData = []
		lineNumber = 0
		for line in data:
			if stop != False:
				if(lineNumber == stop):
					break
				lineNumber += 1
			
			try:
				twitterData.append(json.loads(line.decode('utf-8')))
			except ValueError as errorMessage:
				# print('Tweet parse error: "' + str(errorMessage) + '"', file=sys.stderr)
				continue

		return twitterData


	def getTweets(self):
		''' Returns a list containing tweets as namedtuples '''

		# Twitter JSON legend from https://dev.twitter.com/overview/api/tweets	
		Tweet = namedtuple('Tweet', 'date, message, userName, userScreenName, userImage, userPopularity, rhymeWord')
		self.tweets = []
		filter = Filter()
		for n in range(len(self.twitterData)):
			wordList = self.twitterData[n]['text'].split()
			if filter.filterTweetMessage(wordList):
				continue
			
			rhymeWord = re.sub(r'\W+', '', wordList[len(wordList)-1])
			if filter.filterRhymeWord(rhymeWord):
				continue
				
	
			# Wed Mar 25 09:00:02 +0000 2015
			t = time.strftime('%d-%m-%Y\n%H:%M:%S', time.strptime(self.twitterData[n]['created_at'],'%a %b %d %H:%M:%S +0000 %Y'))
			self.tweets.append(Tweet(t,
								self.twitterData[n]['text'],
								self.twitterData[n]['user']['name'],
								self.twitterData[n]['user']['screen_name'],
								self.twitterData[n]['user']['profile_image_url'],
								int(self.twitterData[n]['user']['followers_count']),
								rhymeWord))

		return sorted(self.tweets, key=attrgetter('userPopularity'), reverse=True)
	
def tester():
	import os
	os.chdir(os.path.dirname('../'))
	print('Initializing database..')
	tester = Tweets()
	print('Database init finished.')
	print('\nPrinting tweet:\n')
	for tweet in tester.getTweets():
		print(tweet)
		break;
	print('\n\nEnd of tester')

if __name__ == "__main__":
	tester()
