#!/usr/bin/python3

''' TwieTwie Application by Arend-Eric, Lesley and Micha '''

import re
import sys
from PyQt4 import QtGui
from classes.tweets import Tweets
from classes.rhyme import Entry, Rhyme
from classes.gui import Gui

def main():
	db = Tweets() # init db
	tweets = db.getTweets() # get all tweets
	rhyme = Rhyme()
	
	twietwiets = []
	usedTweet = tweets[0].message.split()
	wantedRhymeWord = re.sub(r'\W+', '', usedTweet[len(usedTweet)-1])
	
	for tweet in tweets:
		parts = tweet.message.split()
		lw = re.sub(r'\W+', '', parts[len(parts)-1])
		
		try:
			if rhyme.compare(wantedRhymeWord, lw):
				twietwiets.append((tweets[0], tweet))
		except:
			continue
	
	print('Enjoy the GUI!')
	
	app = QtGui.QApplication(sys.argv)
	gui = Gui(None)
	gui.updateUI(twietwiets[0][0], twietwiets[0][1])
	gui.show()
	app.exec_()

if __name__ == "__main__":
	main()
