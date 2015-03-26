#!/usr/bin/python3

''' TwieTwiet Application by Arend-Eric, Lesley and Micha '''
import time
import re
import sys
import twitter.api as api
import twitter.oauth as oauth
from PyQt4 import QtGui
from classes.tweets import Tweets
from classes.rhyme import Entry, Rhyme
from classes.gui import Gui, ProgressBar

def main(argv):
	"""
	The main function that ties all the different aspects of the application together.
	"""
	if len(argv) == 1:
		app = QtGui.QApplication(argv)
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
	elif len(argv) == 2 and argv[1] == '-tweet':
		lastUpdate = None
		while True:
			dt = datetime.datetime.now()
			if dt.hour != lastUpdate.hour:
				lastUpdate = datetime.datetime.now()
				print('Initializing database... (this may take a while)')
				db = Tweets()

				print('Loading Twitter data...')
				tweets = db.getTweets() # get tweets

				print('Loading rhyme dictionary...')
				rhyme = Rhyme()

				print('Matching tweets... (this may take a longer while)')
				usedTweets = set()
				twieTwiets = []

				for i, tweet in enumerate(tweets):
					if tweet.message in usedTweets:
						continue
					for rhymingTweet in tweets[:-i+1]:
						if rhymingTweet.message in usedTweets:
							continue
						try:
							if rhyme.compare(tweet.rhymeWord, rhymingTweet.rhymeWord) and tweet.rhymeWord != rhymingTweet.rhymeWord:
								twieTwiets.append((tweet, rhymingTweet))
								usedTweets.add(tweet.message)
								usedTweets.add(rhymingTweet.message)
								break
						except:
							continue

				# Post the first TwieTwiet to twitter that doesn't exceed the character limit
				token = '3098953431-Z6nnIGjNBq1drfDFq0D1j0Wc1qzTpttoJvOML0E'
				token_key = 'uiPmdVyB73wzqr6cyDiZ4NzFQ9eDYmthm44Q4voaqzwFA'
				con_secret = 'ByfuGTFGSp7FBAy0MuLAUOKxn'
				con_secret_key = 'TC90HCgTFxg4Cu1J0jCCTr1SfCEkOKXnE4MSAriOrMeLcCbX8m'

				auth = oauth.OAuth(token, token_key, con_secret, con_secret_key)
				twitter = api.Twitter(auth=auth)

				for tweet, tweet2 in twieTwiets:
					status = '@' + tweet.userScreenName + ' ' + tweet.message + "\n" + '@' + tweet2.userScreenName + ' ' + tweet2.message
					if len(status) <= 140:
						response = twitter.statuses.update(status=status)
						if response.headers.get('status') == 200:
							print('TwieTwiet posted.')
						else:
							print('Status wasn\'t OK: {}'.format(response.headers.get('status')), file=sys.stderr)
							exit(-1)
						break
				else:
					print('WARNING: Could not find a good TwieTwiet')
			else:
				time.sleep(60)
	else:
		print('Usage: {0}\n       {0} -tweet - Post a TwieTwiet every hour'.format(argv[0]), file=sys.stderr)
		exit(-1)

if __name__ == "__main__":
	main(sys.argv)
