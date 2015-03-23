#!/usr/bin/python3

''' TwieTwie Application by Arend-Eric, Lesley and Micha '''
import time
import re
from classes.tweets import Tweets
from classes.rhyme import Entry, Rhyme
from classes import *

def main():
	db = Tweets(0,10000) # init db
	tweets = db.getTweets() # get tweets
	rhyme = Rhyme()	
	usedTweets = set()
	twieTweets = {}
	
	for tweet in tweets:
		for rhymingTweet in tweets:
			try:
				if rhyme.compare(tweet.rhymeWord, rhymingTweet.rhymeWord) and tweet.rhymeWord != rhymingTweet.rhymeWord:
					if (tweet.message not in usedTweets) and (rhymingTweet.message not in usedTweets):
						twieTweets[tweet] = rhymingTweet
						usedTweets.add(tweet.message)
						usedTweets.add(rhymingTweet.message)
					break
			except:
				continue
				
	
	for tweet1, tweet2 in twieTweets.items():
		print(tweet1.message.encode('utf-8'))
		print(tweet2.message.encode('utf-8'))
		print('-----------')

if __name__ == "__main__":
	main()
