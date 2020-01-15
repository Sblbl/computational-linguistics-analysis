"""
#####################	#######################    #######################    ########             
#####################	#######################    #######################    ########             
      ########          ########       ########    ########       ########    ########             
      ########          ########       ########    ########       ########    ########             
      ########          ########       ########    ########       ########    ########             
      ########          ########       ########    ########       ########    ########             
      ########          #######################    #######################    #####################
      ########          #######################    #######################    #####################.py

This module contains useful code snippets

"""

def chunk (l, n):
	"""
	Divides a list l in chunks of length n
	"""
	for i in range(0, len(l), n):
		yield l[i:i+n]

def tup_2_dic (tup):
	"""
	Transforms a tuple into a dictionary {KEY, VALUE	}
	"""

	dic = {}
	for k, v in tup:
		dic.setdefault(k, v)
	return dic

def tup_2_list (tup):
	"""
	Extracts the first value of a tuple
	in a tuple list. Returns a list.
	"""

	l = []
	for t in tup:
		l.append(t[0])

	return l

def sents_of_len(sents, min_l, max_l):
	"""
	From a list of tokenized sentences, 
	returns the ones of length between
	min_l and max_l.
	"""

	l = [sent for sent in sents if len(sent) >= min_l and len(sent) <= max_l]
	
	return l

def minify (n):
	"""
	Returns an approximated float
	"""
	return "%.4f" % n




