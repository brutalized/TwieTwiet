#!/usr/bin/python3

import json
import re
import os.path
import sys

class Entry:
	"""
	This class represents an entry for a real life dictionary.
	"""
	pattern = re.compile('[^\[\]]+')
	def __init__(self, orthography, stress, phonology, cvpattern):
		"""
		Determines which syllable is stressed and how the syllables are divided into pronunciation and CV pattern.
		"""
		self.orthography = orthography
		self.stress = stress.count('-', 0, stress.index('\'')) # index of syllable that is stressed.
		self.phonology = self.pattern.findall(phonology)
		self.cvpattern = self.pattern.findall(cvpattern)


class Rhyme:
	"""
	This class loads a dictionary from a file, converts it, and offers an interface to determine whether or not two words rhyme with each other by combining the stress, pronunciation and CV pattern from the loaded dictionary.
	"""
	def __init__(self):
		""" Load dictionary from file and initialize the rhyme dictionary """
		filename = '/net/corpora/CELEX/dutch/dpw/dpw.cd'
		
		if not os.path.isfile(filename):
			# Try using local fallback celex data, user is outside LWP')
			filename = 'dpw.cd'
		
		if not os.path.isfile(filename):
			print('Error:\nCould not find Celex DPW. Please put dpw.cd in the root map, or use the program on the LWP', file=sys.stderr)
			exit(-1)
		
		self.dictionary = {}

		for line in open(filename, encoding='utf-8'):
			line = line.rstrip().split('\\')
			if line[3] != '':
				entry = Entry(line[1], line[3], line[4], line[5])
				self.dictionary[entry.orthography.lower()] = entry
		
	def compare(self, word1, word2):
		""" Checks if two words rhyme with each other. """
		if self.lookup(word1) and self.lookup(word2):
			word1 = self.dictionary[word1]
			word2 = self.dictionary[word2]
			
			return self.getRhyme(word1) == self.getRhyme(word2)
		else:
			raise ValueError('word1 or word2 was not found in the dictionary.')
	
	def getRhyme(self, word):
		""" Returns the part of the word that has to rhyme (as a list) """
		phonemes = word.phonology[word.stress:]
		cv = word.cvpattern[word.stress:]
		consonants = cv[0].count('C', 0, cv[0].index('V')) # count consonants at the start of the first syllable until you find a V
		phonemes[0] = phonemes[0][consonants:]
		return phonemes
	
	def lookup(self, word):
		""" Checks whether or not the word was found in the rhyme dictionary """
		return word in self.dictionary


def testRhyme():
	import os
	os.chdir(os.path.dirname('../'))
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

if __name__ == '__main__':
	testRhyme()

# 15078\afschuwelijk\3321\Af-'sxy-w@-l@k\[Af][sxy:][w@][l@k]\[VC][CCVV][CV][CVC]
# 131563\huwelijk\42572\'hy-w@-l@k\[hy:][w@][l@k]\[CVV][CV][CVC]

# 121110\haren\37408\'ha-r@\[ha:][r@]\[CVV][CV]
# 28008\bedaren\8520\b@-'da-r@\[b@][da:][r@]\[CV][CVV][CV]

# 27937\bedaarde\8520\b@-'dar-d@\[b@][da:r][d@]\[CV][CVVC][CV]
# 5671\aarde\1055\'ar-d@\[a:r][d@]\[VVC][CV]
