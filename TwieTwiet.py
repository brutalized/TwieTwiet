#!/usr/bin/python3

''' TwieTwiet Application by Arend-Eric, Lesley and Micha '''
import sys
from PyQt4 import QtGui
from classes.tweets import Tweets
from classes.rhyme import Entry, Rhyme
from classes.gui import Gui
from classes.rank import Rank

def main():
	db = Tweets() # init db
	tweets = db.getTweets() # get tweets
	rhyme = Rhyme()	# init rhyme db
	usedTweets = set()
	twieTwiets = []
	
	# Find TwieTweets
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
	
	rank = Rank(twieTwiets) # Rank them
	
	# Show the GUI
	app = QtGui.QApplication(sys.argv)
	gui = Gui([(tweet1, tweet2) for tweet1, tweet2, score in rank.getRankedTweets()])
	gui.show()
	app.exec_()

if __name__ == "__main__":
	main()
