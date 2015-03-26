#!/usr/bin/python3

''' TwieTwiet Application by Arend-Eric, Lesley and Micha '''
import sys
import twitter.api as api
import twitter.oauth as oauth
import datetime
import time
from PyQt4 import QtGui
from classes.tweets import Tweets
from classes.rhyme import Entry, Rhyme
from classes.gui import Gui, ProgressBar
from classes.rank import Rank

def main(argv):
	"""
	The main function that ties all the different aspects of the application together.
	"""
	if len(argv) == 1:
		app = QtGui.QApplication(argv)
		progress = ProgressBar()
		progress.show()

		progress.update('Initializing database...', 5)
		db = Tweets() # init db

		progress.update('Loading Twitter data...', 30)
		tweets = db.getTweets() # get tweets

		progress.update('Loading rhyme dictionary...', 40)
		rhyme = Rhyme()	# init rhyme db

		progress.update('Matching tweets...', 70)
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
		progress.close()
		gui = Gui([(tweet1, tweet2) for tweet1, tweet2, score in rank.getRankedTweets()])
		gui.show()
		app.exec_()
	elif len(argv) == 2 and argv[1] == '-tweet':
		token = input('Enter Twitter Access Token: ')
		token_key = input('Enter Twitter Access Token Secret: ')
		con_secret = input('Enter Twitter Consumer Key (API Key): ')
		con_secret_key = input('Enter Twitter Consumer Secret (API Secret): ')

		if input('Post an update right now? Type y for yes, any other key for no: ') == 'y':
			postFirstTime = True
		else:
			postFirstTime = False
			print('\nTwitter posting started, will post an update to Twitter every hour from now.')
		
		lastUpdate = datetime.datetime.now()
		while True:
			dt = datetime.datetime.now()
			if dt.hour != lastUpdate.hour or postFirstTime:
				postFirstTime = False
				
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

				# Find TwieTweets
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

				rank = Rank(twieTwiets) # Rank them
				twieTwiets = [(tweet1, tweet2) for tweet1, tweet2, score in rank.getRankedTweets()]
				
				# Post the first TwieTwiet to twitter that doesn't exceed the character limit
				auth = oauth.OAuth(token, token_key, con_secret, con_secret_key)
				twitter = api.Twitter(auth=auth)

				for tweet, tweet2 in twieTwiets:
					status = 'RT @' + tweet.userScreenName + ' ' + tweet.message + "\n" + 'RT @' + tweet2.userScreenName + ' ' + tweet2.message
					if len(status) <= 140:
						response = twitter.statuses.update(status=status)
						if response.headers.get('status') == "200 OK":
							print('TwieTwiet posted.')
						else:
							print('Status wasn\'t OK: {}'.format(response.headers.get('status')), file=sys.stderr)
						break
					else:
						continue
				else:
					print('WARNING: Could not find a good TwieTwiet')
			else:
				time.sleep(60)
	else:
		print('Usage: {0}\n       {0} -tweet - Post a TwieTwiet every hour'.format(argv[0]), file=sys.stderr)
		exit(-1)

if __name__ == "__main__":
	main(sys.argv)
