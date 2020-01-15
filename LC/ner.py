"""
##########        ########    #####################    #######################
########  ##      ########    #####################    #######################
########    ##    ########    ########                 ########       ########
########	  ##  ########    #################        #######################
########        ##########    #################        #######################
########          ########    ########                 ########    ########
########          ########    #####################    ########      ########
########          ########    #####################    ########        ########.py

This module computes the basic ner stats of a text

"""

import nltk
from nltk import word_tokenize as wt
from nltk import pos_tag as POS
from nltk import ne_chunk as NER
import LC.toolbox as tool
import LC.tok as LC
import math
import numpy as np
import re

def ner_sents(sents):
	"""
	Given a list of word-tokenized sentences, 
	Returns the tree of the sentences.
	"""

	sentences = []

	for sent in sents:
		sentences.append(NER(POS(wt(sent))))

	return sentences


def get_ner_sents(sentences, NER_tag):
	"""
	Returns all the sentences with a specific NER_tag or list of.
	Requires already chunked sentences.
	"""

	sents = []

	for sent in sentences:
		add = False
		# for every node in the tree
		for label in sent:
			# if it is an intermediate node
			if hasattr(label, 'label'):
				if label.label() in NER_tag:
					add = True
		if add:
			sents.append(sent)


	return sents

def get_ner_entities(sentences, NER_tag):
	"""
	Analyses each chunked sentence and returns 
	the list of entities with a specific NER tag or list of.
	It returns a dictionary divided by NER_tag, in which each attr 
	corresponds to a list of entities.
	"""

	entities = {}
	freq_entities = {}

	for sent in sentences:
		# for every node in the tree
		for label in sent:
			NER = ''
			# if it is an intermediate node
			if hasattr(label, 'label'):
				if label.label() in NER_tag:
					# for each leaf in the node
					for part in label.leaves():
						NER = part[0]

					if label.label() not in entities:
						entities[label.label()] = []

					entities[label.label()].append(NER)

	for ner in entities:
		freq_entities[ner] = {}
		freq_entities[ner] = LC.freqs(entities[ner], set(entities[ner]))

	return freq_entities

def meaningful_sents(sentences, NER_tag, leaves):
	"""
	From a set of sents returns only the ones
	containing a NER tag with a specific leaf.
	The sentences must already be chunked, because
	it doesn't look for some tokens, 
	but for some specific leaves in the tree.
	"""

	meaningful_sents = []

	for sent in sentences:
		keep = False
		# for every node in the tree
		for label in sent:
			# if it is an intermediate node
			if hasattr(label, 'label'):
				if label.label() in NER_tag:
					# for each leaf in the node
					for part in label.leaves():
						if part[0] in leaves:
							keep = True
		if keep:
			meaningful_sents.append(sent)

	return meaningful_sents

def tree_2_text(sentence):
	"""
	From a list of chunked sentences
	returns the tokenized sentences
	without any POS or NER tag.
	"""
	
	# transforms in conll and delete the syntactic infos
	conll = nltk.chunk.tree2conllstr(sentence)
	lines = conll.split('\n')
	s = ''
	for line in lines:
		line = line.split(' ')
		s = s + line[0] + ' '
	
	# removes the last white character
	return s[:-1]

def trees_2_toks(sentences):
	"""
	From a list of chunked sentences
	returns the tokenized sentences
	without any POS or NER tag.
	"""
	
	sents = []

	for sent in sentences:
		# transforms in conll and delete the syntactic infos
		conll = nltk.chunk.tree2conllstr(sent)
		lines = conll.split('\n')
		s = ''
		for line in lines:
			line = line.split(' ')
			s = s + line[0] + ' '
		sents.append(wt(s[:-1]))

	# removes the last white character
	return sents

def find_dates(sentence):
	"""
	Searches for some temporal pattern 
	in a plain text sentence
	"""

	dates = []

	# find patterns in the format dd/mm/yy(yy), accepting all the possible year combination ad not admitting bisestiles
	ddmmyy = re.findall('\s(?:(?:[0-2]?[\d]|3[0-1])[-/.·](?:0?(1|3|5|7|8|10|12)|1[0-2])[-/.·](?:\d{4}|\d{2})|(?:[0-2]?[\d]|30)[-/.·](?:0?(4|6|9|11)|1[0-2])[-/.·](?:\d{4}|\d{2})|(?:(?:[0-1]?[\d]|2[0-8]))[-/.·](?:0?2)[-/.·](?:\d{4}|\d{2}))\s', sentence)
	#extend the dates list in order to do not have sublists
	dates.extend(ddmmyy)
	
	# find patterns in the format mm/dd/yy(yy), accepting all the possible year combination ad not admitting bisestiles
	mmddyy = re.findall('\s(?:(?:0?(1|3|5|7|8|10|12)|1[0-2])[-/.·](?:[0-2]?[\d]|3[0-1])[-/.·](?:\d{4}|\d{2})|(?:0?(4|6|9|11)|1[0-2])[-/.·](?:[0-2]?[\d]|30)[-/.·](?:\d{4}|\d{2})|(?:0?2)[-/.·](?:(?:[0-1]?[\d]|2[0-8]))[-/.·](?:\d{4}|\d{2}))\s', sentence)
	dates.extend(mmddyy)

	# find temporal references not in date-format

	# in order to be sure that an indipendent sequence of digit is a year, we only consider 4-digits groups
	# also checks if a b.C or a.C occurs
	years = re.findall('\s\d{4}(?:b\.?C|A\.?D\.?)?\s', sentence)

	months = re.findall('(?:Genuary|Febraury|March|April|May\b|June|July|August|September|October|November|December)', sentence)
	days = re.findall('(?:Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)', sentence)

	s = wt(sentence)
	adverbs = ['this', 'that', 'next', 'last']
	
	# if only days are available we have not to find other 
	if days and not months:
		for day in days:
			idx = s.index(day)

			# look for adverbs pairing the day
			if idx > 0:
				if s[idx-1] in adverbs:
					day = s[idx-1] + ' ' + day
			dates.append(day)
	
	else:
		#month_idx, day_idx, num_idx = []

		if months:
			# while a month occurs, we can look for numbers connected to it
			m_31 = ['January', 'March', 'May', 'July', 'August', 'October', 'December']
			m_30 = ['April', 'June', 'September', 'November']
			m_28 = ['Febraury']

			for month in months:
				month_idx = s.index(month)
				max_day = 0
				if month in m_31:
					max_day = '[1-32]'
				elif month in m_30:
					max_day = '[1-31]'
				else:
					max_day = '[1-29]'

				# find pattern 30 August
				if month_idx > 0:
					if re.match(max_day, s[month_idx-1]):
						dates.append(s[month_idx-1] + ' ' + month)
				# find pattern August 30 or August, 30
				else:
					if re.match(max_day, s[month_idx+1]):
						dates.append(s[month_idx+1] + ' ' + month)
					elif re.match(max_day, s[month_idx+2]):
						dates.append(s[month_idx+2] + ' ' + month)
					else:
						dates.append(month)

	return dates

def extract_links(sentences, NER_tag_and_leaves, NER_linked, POS_linked):
	"""
	From a list of sentences, searches 
	the elements linked to a given leave with a specific NER.
	The sentences must be chunked, while NER_tag_and_leaves is a dict 
	in the form : {'PERSON' : ['Alice', 'Rabbit', 'Obama'], 'ORGANISATION' : ['ONU', 'NASA']}
	The output will be: {'PERSON' : {'Alice' : [rel_1, rel_2], 'Rabbit' : [rel_1, rel_2] }}
	"""
	#NE.extract_links(useful_sents_1, {'PERSON' : PEOPLE_1}, NER_tags, POS_tags)
	relations = {}

	# Analyse one NER per time (in our program will be only PERSON)
	for NER_tag in NER_tag_and_leaves:
		# Add in the relation dict a field for the NER
		relations[NER_tag] = {}

		# Find informations for each character (NER leave)
		for leave in NER_tag_and_leaves[NER_tag]: 

			relations[NER_tag][leave] = {}
			# Archive only the sentences that contain a specific NER leave
			sents = []
			for sent in sentences:
				keep = False
				# for every node in the tree
				for label in sent:
					# if it is an intermediate node
					if hasattr(label, 'label'):
						if label.label() == NER_tag:
							# for each leaf in the node
							for part in label.leaves():
								if part[0] == leave:
									keep = True
				if keep: 
					sents.append(sent)

			# Now we have the sents that contain a certain character (NER leave)
			leave_rels = {}
			for sent in sents:

				# First, find NER informations
				# for every node in the tree
				for label in sent:
					# if it is an intermediate node
					if hasattr(label, 'label'):
						if label.label() in NER_linked:
							if not label.label() in leave_rels:
								leave_rels[label.label()] = []
							# for each leaf in the node
							for part in label.leaves():
								# Exclude the character of which we are searching links
								if part[0] != leave:
									leave_rels[label.label()].append(part[0])

				# Then, delete the NER information and find the patterns with Regexes
				s = tree_2_text(sent)
				
				leave_rels['dates'] = find_dates(s)

				# Finally,extract the important POS

				# analyze the POS of the sentence
				s_pos = POS(wt(s))

				for word, pos_tag in s_pos:
					if pos_tag in POS_linked:
						if word != leave:
							# Exclude the character of which we are searching links
							if not pos_tag in leave_rels:
								leave_rels[pos_tag] = []
							leave_rels[pos_tag].append(word)

			relations[NER_tag][leave] = leave_rels

	return relations

def extract_link_freqs(link_dict):
	"""
	Given the dict of the links, return a more clean version
	with the frequency of each link.
	"""

	for NER in link_dict:
		for leaf in link_dict[NER]:
			for link_type in link_dict[NER][leaf]:
				l = link_dict[NER][leaf][link_type]
				freqs = LC.freqs(l, set(l))
				link_dict[NER][leaf][link_type] = freqs

	return link_dict

def rank_link_freqs(link_freqs, max_els):
	"""
	Given the link-frequencies, extracts the (max) 
	most frequent ones
	"""

	for NER in link_freqs:
		for leaf in link_freqs[NER]:
			for link_type in link_freqs[NER][leaf]:
				# Order by freq and select the desired number of items
				n = max_els
				if n > len(link_freqs[NER][leaf][link_type]):
					n = len(link_freqs[NER][leaf][link_type])
				link_freqs[NER][leaf][link_type] = LC.rank(link_freqs[NER][leaf][link_type])[:n]

	return link_freqs

def assign_sent_2_person(sentences, people):
	"""
	From a list of sentences and a list of people
	comparing in them, returns a dict that links the person
	to the sentences in which it appears.
	"""

	d = {}

	for sent in sentences:
		for person in people:
			if person in sent:
				if person not in d:
					d[person] = []
				d[person].append(sent)

	return d


def markov_0(sentence, tok_freqs, text_len, smooth):
	"""
	Computes the Markov probability of level 0
	of a sentence. Needs the list of token frequencies and the length 
	of the corpus. The function applies a smoothing parameter 
	if smooth == True
	"""

	prob = 1.0
	vocab_len = len(tok_freqs)

	if smooth:
		for tok in sentence:
			tok_prob = (tok_freqs[tok] + 1) * 1.0 / (text_len + vocab_len)* 1.0
			prob *= tok_prob
	else:
		for tok in sentence:
			tok_prob = tok_freqs[tok] * 1.0 / text_len * 1.0
			prob *= tok_prob

	return prob

def get_max_markow(sentences, tok_freqs, text_len, smooth):
	"""
	Selects in a list of sentences the one 
	with the max probability, using Markow 0
	"""

	max_prob = 0
	sentence = ''

	for sent in sentences:
		p = markov_0(sent, tok_freqs, text_len, smooth)
		if p > max_prob:
			max_prob = p
			sentence = sent

	return(sentence, max_prob)


