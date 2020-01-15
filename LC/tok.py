"""
#####################	#######################    ########           ##
#####################	#######################    ########         ##
      ########          ########       ########    ########       ##
      ########          ########       ########    ###############
      ########          ########       ########    ########  #######
      ########          ########       ########    ########    #######
      ########          #######################    ########      #######
      ########          #######################    ########        #######.py

This module computes the basic stats of a text

"""

from LC import toolbox as tool
from nltk import pos_tag as POS
import matplotlib
import matplotlib.pyplot as plt
import math
import numpy as np
import operator
import re

def create_vocab (toks):
	"""
	Creates a list where every word of the text
	appears only 1 time (a vocabulary)
	"""
	return sorted(list(set(toks)))

def freqs(toks, vocab):
	"""
	For every word in the vocabulary, 
	counts its frequency. Returns a dict {word : freq}
	"""
	freqs = {}
	for w in vocab: 
		# {w : frequency}
		freqs[w] = toks.count(w)
	# Sort by freq
	# Source: https://stackoverflow.com/questions/613183/how-do-i-sort-a-dictionary-by-value
	freqs = {k: v for k, v in sorted(freqs.items(), key=lambda item: item[1])}
	return freqs

def mean_len (els):
	"""
	Computes the mean length of a list of items.
	It can be used both for sentences
	and for tokens
	"""
	return sum(len(el) for el in els) / len(els)

def get_hapax (freqs):
	"""
	Gets the freqency == 1 words from 
	the  frequency dict
	"""
	return list(w for w, i in freqs.items() if i == 1)

def hapax_distr (toks, interval, name):
	"""
	Plots the Hapax distribution
	in a text in intervals of interval
	"""

	# Dividing the text in lists of interval

	chunks = list(tool.chunk(toks, interval))

	vocab_stats = []
	hapax_stats = []

	# Computing the dimension of the vocabulary and the number of hapaxes
	chunk = []
	for i in range(len(chunks)):
		chunk += chunks[i]
		ch_vocab = create_vocab(chunk)
		ch_freqs = freqs(chunk, ch_vocab)
		ch_hapax = get_hapax(ch_freqs)

		vocab_stats.append(len(ch_vocab))
		hapax_stats.append(len(ch_hapax))

	# PLOT
	plt.rcParams["figure.figsize"] = (30,20)
	#font = {'family' : 'normal', 'size'   : 30}

	#matplotlib.rc('font', **font)

	plt.plot(vocab_stats, '#000000', linewidth=16)
	plt.plot(hapax_stats, '#b3b1b1', linewidth=16)

	plt.title('Hapax distribution in ' + name)
	plt.ylabel('Hapax vs Vocab')
	plt.xlabel('Text length')
	plt.xticks(np.arange(0, len(chunks)))
	plt.legend(['Vocabulary', 'Hapaxes'])
	plt.savefig('plots/' + name + '.svg')
	plt.close()
	print('······································')
	print('hapax plot for ' + name + ' saved')
	print('······································')
	return

def get_POS_freqs(tup_list):
	"""
	Get the frequency of each POS-tag
	"""

	POS = {}

	for tup in tup_list:
		pos = tup[1]
		if not pos in POS:
			POS[pos] = 0
		POS[pos] += 1

	return POS

def rank(POS_freqs):
	"""
	Transforms a dict in a list sorted by occurrence
	"""

	return sorted(POS_freqs.items(), key = operator.itemgetter(1), reverse = True)

#nltk.bigram + nltk.POS aren't compatible.

def tag_bigrams(bigr_list):
	"""
	Creates a list of bigrams 
	from a list of POS-tagged-tokens
	"""

	POS_bigs = []

	for i in range(len(bigr_list)-2):
		POS_bigs.append((bigr_list[i][1], bigr_list[i+1][1]))

	return POS_bigs


def get_cond_prob(bi_probs, uni_probs):
	"""
	Takes two lists of probabilities, one for the bigrams
	and one for the unigrams and returns
	the conditioned probability of their elements.
	It follows the equation:
		cond_prob([A, B]) = freq([A, B])*1.0 / freq(A)*1.0
	The multiplication *1.0 makes the program return a float type number.
	"""

	probs = {}
	for bigr in bi_probs:
		# Solve issues related to the use of the char "'" in the POS tags
		uni = re.sub('\'', '\'', bigr[0])
		probs[bigr] = bi_probs[bigr] * 1.0 / uni_probs[uni] * 1.0

	return probs

def freqs_2_prob(freq_list, n_toks):
	for key, val in freq_list.items():
		freq_list[key] = val / n_toks

	return freq_list


def get_LMI(bi_freqs, tot_bigrs, uni_freqs, tot_toks, bi_set):
	""""
	Returns the Local Mutual Information of the two elements
	of a bigram, following the formula:
		freq(A, B) * log2 ( P(A, B) / P(A) * P(B) )
	Requires the frequencies of the single POS and of the bigrams,
	and the list of the unique POS. 
	tot_bigrs is the total number of bigrams in the text 
	while tot_toks is the number of words in the text. 
	They are needed to compute the probability from the frequency
	"""
	
	bi_probs = freqs_2_prob(bi_freqs, tot_bigrs)
	uni_probs = freqs_2_prob(uni_freqs, tot_toks)

	LMIs = {}

	for tup in bi_set:
		LMIs[tup] = bi_freqs[tup] * math.log( ( bi_probs[tup] / (uni_probs[tup[0]] * uni_probs[tup[1]]) ), 2)

	return LMIs





