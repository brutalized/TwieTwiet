import json
import re

class Entry:
	"""
	This class represents an entry for a real life dictionary.
	"""
	pattern = re.compile('[^\[\]]+') # still need to make this proper with lookbehind [ and lookahead ]
	def __init__(self, orthography, stress, phonology, cvpattern):
		"""
		phonology and cvpattern are expected to have the following format: [syl1][syl2][syl3]
		"""
		self.orthography = orthography
		self.stress = stress.count('-', 0, stress.index('\'')) # index of syllable that is stressed.
		self.phonology = self.pattern.findall(phonology)
		self.cvpattern = self.pattern.findall(cvpattern)

class Rhyme:
	def __init__(self, filename='../celex/dpw.cd'):
		self.filename = filename
		self.dictionary = {}
		
		# load dictionary
		with open(filename, encoding='utf-8') as f:
			for line in f:
				line = line.rstrip().split('\\')
				if line[3] != '':
					entry = Entry(line[1], line[3], line[4], line[5])
				self.dictionary[entry.orthography.lower()] = entry
	
	def compare(self, word1, word2):
		"""
		Checks if two words rhyme with each other.
		1: word1 and word2 rhyme with each other.
		0: word1 and word2 don't rhyme with each other.
		-1: word1 or word2 was not found in the dictionary.
		"""
		if self.lookup(word1) and self.lookup(word2):
			word1 = self.dictionary[word1]
			word2 = self.dictionary[word2]
			
			phonemes1 = word1.phonology[word1.stress:]
			cv1 = word1.cvpattern[word1.stress:]
			consonants = cv1[0].count('C', 0, cv1[0].index('V')) # count consonants at the start of the first syllable until you find a V
			phonemes1[0] = phonemes1[0][consonants:]
			
			phonemes2 = word2.phonology[word2.stress:]
			cv2 = word2.cvpattern[word2.stress:]
			consonants = cv2[0].count('C', 0, cv2[0].index('V')) # count consonants at the start of the first syllable until you find a V
			phonemes2[0] = phonemes2[0][consonants:]
			
			return phonemes1 == phonemes2
		else:
			raise ValueError('word1 or word2 was not found in the dictionary.')
	
	def lookup(self, word):
		return word in self.dictionary


def test_rhyme():
	print('Initializing rhyme dictionary...')
	rhyme = Rhyme()
	print('Initialization complete.\n')
	
	print('Rhyme checker.')
	while True:
		word1 = input('Eerste word: ').lower()
		word2 = input('Tweede word: ').lower()
		if word1 in ['', 'quit', 'exit'] or word2 in ['', 'quit', 'exit']:
			break
		elif rhyme.compare(word1, word2):
			print('{} rijmt op {}!\n'.format(word1, word2))
		else:
			print('{} en {} rijmen niet!\n'.format(word1, word2))

def test_full():
	import tweets
	samplesize = 1000
	print('Initializing tweets...')
	tweets_handler = tweets.Tweets()
	tweets = tweets_handler.getTweets(0, samplesize)
	print('Initializing rhyme dictionary...')
	rhyme = Rhyme()
	print('Initialization complete.\n')
	
#	message1 = [word for word in tweets[0].message.lower().split() if rhyme.lookup(word)]
#	message2 = [word for word in tweets[1].message.lower().split() if rhyme.lookup(word)]
	
	sweets = [tweet for tweet in tweets if rhyme.lookup(tweet.message.lower().split()[-1])]
	
	twietwiets = []
	for i, sweet in enumerate(sweets):
		message = sweet.message.lower().split()
		for j, sweet2 in enumerate(sweets):
			message2 = sweet2.message.lower().split()
			if i != j and message[-1] != message2[-1] and rhyme.compare(message[-1], message2[-1]):
				twietwiets.append((sweet, sweet2))
				print('found two corresponding sweets! Sweets spotted at: position {} and {}'.format(i, j))
	else:
		print('No corresponding sweets found at samplesize', samplesize, 'and sweet size', len(sweets))
	
	for twietwiet in twietwiets:
		tweet, tweet2 = twietwiet
		print('Tweet 1:', tweet.message)
		print('Tweet 2:', tweet2.message)
		print()

if __name__ == '__main__':
	test_rhyme()

# 15078\afschuwelijk\3321\Af-'sxy-w@-l@k\[Af][sxy:][w@][l@k]\[VC][CCVV][CV][CVC]
# 131563\huwelijk\42572\'hy-w@-l@k\[hy:][w@][l@k]\[CVV][CV][CVC]

# 121110\haren\37408\'ha-r@\[ha:][r@]\[CVV][CV]
# 28008\bedaren\8520\b@-'da-r@\[b@][da:][r@]\[CV][CVV][CV]

# 27937\bedaarde\8520\b@-'dar-d@\[b@][da:r][d@]\[CV][CVVC][CV]
# 5671\aarde\1055\'ar-d@\[a:r][d@]\[VVC][CV]