#!/usr/bin/python3

''' TwieTwiet Application by Arend-Eric, Lesley and Micha '''
import time
import re
import sys
from PyQt4 import QtGui
from classes.tweets import Tweets
from classes.rhyme import Entry, Rhyme
from classes.gui import Gui

def main():
	db = Tweets(0,10000) # init db
	tweets = db.getTweets() # get tweets
	rhyme = Rhyme()	
	usedTweets = set()
	twieTwiets = []
	
	for tweet in tweets:
		for rhymingTweet in tweets:
			try:
				if rhyme.compare(tweet.rhymeWord, rhymingTweet.rhymeWord) and tweet.rhymeWord != rhymingTweet.rhymeWord:
					if (tweet.message not in usedTweets) and (rhymingTweet.message not in usedTweets):
						twieTwiets.append((tweet, rhymingTweet))
						usedTweets.add(tweet.message)
						usedTweets.add(rhymingTweet.message)
					break
			except:
				continue
	
	app = QtGui.QApplication(sys.argv)
	gui = Gui(twieTwiets)
	gui.show()
	app.exec_()

if __name__ == "__main__":
	main()
