"""
#####################	########             	#####################	#######################	   ##########         ########
#####################	########             	#####################	#######################	   ########  ##       ########
########			 	########             	########             	########       ########	   ########    ##     ########
########			 	########             	#################    	#######################	   ########	      ##  ########
########			 	########             	#################    	#######################	   ########         ##########
########			 	########             	########             	########       ########	   ########           ########
#####################	#####################	#####################	########       ########	   ########           ########
#####################	#####################	#####################	########       ########	   ########           ########.py

This module cleans the text

"""

import re

def del_specs (text, char):
	"""
	Eliminates the special chars
	"""
	
	text = re.sub(char, ' ', text)
	
	return text

def rm_seps(text):
	"""
	Removes exceeding separators. 
	Best if runned at the end of the cleaning
	"""
	text = re.sub('\s+', ' ', text)
	text = re.sub('\n+', '\n', text)
	text = re.sub('\t', ' ', text)
	text = re.sub('[ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz]\n[ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz]', ' ', text)
	return text

def clean_punct(text):
	"""
	Uniforms the punctuation
	"""

	# Quotation marks
	text = re.sub('\s\’', ' "', text)
	text = re.sub('\’\s', '" ', text)
	# Apostrophe
	text = re.sub('[ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz]\’[ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz]', '\'', text)
	# Suspension points
	text = re.sub('\.\.\.', ' … ', text)
	return text

def sep_punct(text):
	"""
	Adds a space before and after the punctuation marks
	that generally have only a punctuation role
	"""
	text = re.sub('([\".,:!?/\(\)\[\]])', ' \1 ', text)
	text = re.sub('\s\-', ' - ', text)
	text = re.sub('\-\s', ' - ', text)
	return text

def hardcore_sep_punct(text):
	"""
	Adds a space before and after every 
	punctuation mark
	"""
	text = re.sub('([.,;\'\"!?-:/\(\)\[\]])', ' \1 ', text)
	return text

def rm_chaps(text):
	"""
	Removes chapter's heading
	"""

	chaps = ['^CHAPTER.$', '^chapter\s\d+', '^Chapter.+$', 'SECTION\s\d+', 'PART\s\d+', '\n\d+\n', '^\s*(I|V|X|L|C)+\s*$']
	for chap in chaps:
		text = re.sub(chap, '', text)
	return text

def clean_text(text):
	"""
	Performs a complete cleaning
	of the input text and returns 
	clear one.
	"""

	# delete useless special chars found opening the text
	del_specs(text, '\*')
	# clean the punctuation in order to have a uniform redaction of the text
	clean_punct(text)
	# separate some punctuation mark from the tokens
	# in order to have a correct tokenization
	sep_punct(text)
	# Remove chapter titlings
	rm_chaps(text)

	# delete redundant separators
	rm_seps(text)

	return text












