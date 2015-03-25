import math
from collections import namedtuple

class Rank():

	def __init__(self, twieTwiets):
		self.ranked = self.rankTweets(twieTwiets)
		
	def getRankedTweets(self):
		return self.ranked
	
	def rankTweets(self, twieTwiets):
		rankedTwieTwiets = []
		
		# Calculate maximum and total scores and individual scores per tweet
		maxLength, maxInvolvement, maxPopularity = 0, 0, 0
		totLength, totInvolvement, totPopularity = 0, 0, 0
		Stats = namedtuple('Stats', 'rhymeLength, involvement, popularity')
		for tweet, rhymingTweet in twieTwiets:
			rhymeLength = (len(tweet.rhymeWord) + len(rhymingTweet.rhymeWord)) / 2
			usersInvolvement = (tweet.userInvolvement + rhymingTweet.userInvolvement) / 2
			usersPopularity = (tweet.userPopularity + rhymingTweet.userPopularity) / 2
			
			if rhymeLength > maxLength:
				maxLength = rhymeLength
			if usersInvolvement > maxInvolvement:
				maxInvolvement = usersInvolvement
			if usersPopularity > maxPopularity:
				maxPopularity = usersPopularity
				
			totLength += rhymeLength
			totInvolvement += usersInvolvement
			totPopularity += usersPopularity
			
			rankedTwieTwiets.append((tweet, rhymingTweet, Stats(rhymeLength, usersInvolvement, usersPopularity)))

		# Calculate the average and start with deviation
		twieTweetCount = len(rankedTwieTwiets)
		gemLength = totLength / twieTweetCount
		gemInvolvement = totInvolvement / twieTweetCount
		gemPopularity = totPopularity / twieTweetCount
		devLength, devInvolvement, devPopularity = 0, 0, 0
		for tweet, rhymingTweet, stats in rankedTwieTwiets:
			devLength += (stats.rhymeLength - gemLength)**2
			devInvolvement += (stats.involvement - gemInvolvement)**2
			devPopularity += (stats.popularity - gemPopularity)**2
		
		# Calculate the standard deviation
		devLength = math.sqrt(devLength / twieTweetCount)
		devInvolvement = math.sqrt(devInvolvement / twieTweetCount)
		devPopularity = math.sqrt(devPopularity / twieTweetCount)
		minRankLength = gemLength - devLength
		maxRankLength = gemLength + devLength
		minRankInvolvement = gemInvolvement - devInvolvement
		maxRankInvolvement= gemInvolvement + devInvolvement
		minRankPopularity = gemPopularity - devPopularity
		maxRankPopularity = gemPopularity + devPopularity
		
		# Make with the calculated variables a new ranked list
		twieTwiets = []
		for t1, t2, score in rankedTwieTwiets:
			# Factor 1: Length of the Tweet's rhymeword
			if score.rhymeLength > maxRankLength:
				w1 = 100
			elif score.rhymeLength < minRankLength:
				w1 = 1
			else:
				w1 = (maxRankLength / score.rhymeLength) / 100
			
			# Factor 2: Involvement of the Tweet's author
			if score.involvement > maxRankInvolvement:
				w2 = 100
			elif score.involvement < minRankInvolvement:
				w2 = 1
			else:
				w2 = (maxRankInvolvement / score.involvement) / 100
				
			# Factor 3: Popularity of the Tweet's author
			if score.popularity > maxRankPopularity:
				w3 = 100
			elif score.popularity < minRankPopularity:
				w3 = 1
			else:
				w3 = (maxRankPopularity / score.popularity) / 100
			
			# Define a final score and set how much a value should weigh
			finalScore = w1 * 0.7 + w2 * 0.1 + w3 * 0.2
			
			twieTwiets.append((t1, t2, finalScore))
		
		return sorted(twieTwiets, key=lambda tweet: tweet[2], reverse=True)