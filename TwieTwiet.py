#!/usr/bin/python3

''' TwieTwiet Application by Arend-Eric, Lesley and Micha '''
import time
import re
import sys
from PyQt4 import QtGui
from classes.tweets import Tweets
from classes.rhyme import Entry, Rhyme
from classes.gui import Gui, ProgressBar

def main():
	app = QtGui.QApplication(sys.argv)
	progress = ProgressBar()
	progress.show() # gotcho reference bro!

	progress.update('Initializing database...', 5)
	db = Tweets(0, 25000) # init db, use max 25.000 tweets

	progress.update('Loading Twitter data...', 30)
	tweets = db.getTweets() # get tweets

	progress.update('Loading rhyme dictionary...', 40)
	rhyme = Rhyme()

	progress.update('Matching tweets...', 70)
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

	progress.close()
	gui = Gui(twieTwiets)
	gui.show()
	app.exec_()

if __name__ == "__main__":
	main()
