class Filter():
	''' Class with various filtering methods for tweets and rhymewords '''
	
	def filterTweetMessage(self, wordList):
		''' Umbrella method to filter the Tweet message text '''
		
		if self.filterRetweets(wordList) or self.filterShortMessages(wordList) or self.filterLongMessages(wordList):
			return True
		
		return False
		
	def filterRhymeWord(self, rhymeWord):
		''' Umbrella method to filter the Rhymeword '''
		
		if self.filterHTTP(rhymeWord) or self.filterShortWord(rhymeWord) or self.filterHashTag(rhymeWord) or self.filterAtSign(rhymeWord):
			return True
		
		return False
		
	def filterRetweets(self, wordList):
		''' Filters all messages starting with RT '''
		
		if wordList[0] == 'RT':
			return True
		
	def filterShortMessages(self, wordList):
		''' Check if the tweet contains at least 7 words '''
		
		if len(wordList) <= 7:
			return True
		
	def filterLongMessages(self, wordList):
		''' Check if the tweet contains a maximum of 12 words '''
		
		if len(wordList) > 12:
			return True
		
	def filterAtSign(self, rhymeWord):
		''' Check if the tweet's last word is an at sign '''
		
		if rhymeWord.find('@') != -1:
			return True
		
	def filterHashTag(self, rhymeWord):
		''' Check if the tweet's last word is a hashtag '''
		
		if rhymeWord.find('#') != -1:
			return True
		
	def filterHTTP(self, rhymeWord):
		''' Check if the tweet's last word is a URL '''
		
		if rhymeWord.find('http') != -1:
			return True
		
	def filterShortWord(self, rhymeWord):
		''' Check if the last word is very short (< 3 char) '''
		
		if len(rhymeWord) < 3:
			return True
