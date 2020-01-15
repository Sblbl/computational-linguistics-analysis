"""
python3 prog_2.py texts/alice.txt texts/second.txt
"""

import sys
#	NLTK modules
import nltk
from nltk import sent_tokenize as st
from nltk import word_tokenize as wt
from nltk.probability import FreqDist as fd
#	Statistical module
import LC.tok as LC
#	Statistical module
import LC.ner as NE
#	Data cleaning module
import LC.clean as cl
#	Utility module
import LC.toolbox as tool
#import bs4 to edit the output in html format
from bs4 import BeautifulSoup
import write_output as OUT

st = nltk.data.load('tokenizers/punkt/english.pickle')

def main(f_1, f_2):
	"""
	Extracts NER stats from 2 text files
	"""

	######################################
	#	Text extraction
	######################################

	t_1 = ''
	t_2 = ''

	with open(f_1, 'r') as f:
		t_1 = f.read()
	with open(f_2, 'r') as f:
		t_2 = f.read()

	######################################
	#	Text cleaning
	######################################

	t_1 = cl.clean_text(t_1)
	t_2 = cl.clean_text(t_2)

	
	# Initialize output
	output = OUT.init_html()
	soup = BeautifulSoup(output, 'html.parser')

	col_1 = soup.find('div', {'id': 'text-1-container'})
	col_2 = soup.find('div', {'id': 'text-2-container'})

	title_1 = soup.new_tag('p', attrs={'id' : 'title-1'})
	title_1.insert(1,'Alice in Wonderland')

	title_2 = soup.new_tag('p', attrs={'id' : 'title-2'})
	title_2.insert(1,'Second Variety')

	author_1 = soup.new_tag('p', attrs={'id' : 'author-1'})
	author_1.insert(1,'Lewis Carroll')

	author_2 = soup.new_tag('p', attrs={'id' : 'author-2'})
	author_2.insert(1,'Philip Kindred Dick')

	col_1.append(title_1)
	col_1.append(author_1)

	col_2.append(title_2)
	col_2.append(author_2)


	######################################
	#	Extracting the useful elements
	######################################


	# Sentence tokens
	sents_1 = st.tokenize(t_1)
	sents_2 = st.tokenize(t_2)
	
	# Word tokens (by sentence)
	s_toks_1 = []
	s_toks_2 = []

	for s_1, s_2 in zip(sents_1, sents_2):
		s_toks_1.append(wt(s_1))
		s_toks_2.append(wt(s_2))

	# Word tokens (unique list)
	toks_1 = wt(t_1)
	toks_2 = wt(t_2)

	# NER tagging

	POS_NE_1 = NE.ner_sents(sents_1)
	POS_NE_2 = NE.ner_sents(sents_2)

	PERSON_sents_1 = NE.get_ner_sents(POS_NE_1, ['PERSON'])
	PERSON_sents_2 = NE.get_ner_sents(POS_NE_2, ['PERSON'])

	
	# Get the entities of specific NER_tag
	ENTITIES_1 = NE.get_ner_entities(PERSON_sents_1, ['PERSON'])
	ENTITIES_2 = NE.get_ner_entities(PERSON_sents_2, ['PERSON'])

	PEOPLE_1 = LC.rank(ENTITIES_1['PERSON'])[:10]
	PEOPLE_2 = LC.rank(ENTITIES_2['PERSON'])[:10]

	# Print most frequent characters
	nc_1 = OUT.complex_container('Most frequent characters', PEOPLE_1, soup)
	nc_2 = OUT.complex_container('Most frequent characters', PEOPLE_2, soup)
	col_1.append(nc_1)
	col_2.append(nc_2)
	print('added Most frequent characters to project/index.html')


	# Extract only sentence in which appear the selected PEOPLE
	PEOPLE_1 = tool.tup_2_list(PEOPLE_1)
	PEOPLE_2 = tool.tup_2_list(PEOPLE_2)
	
	useful_sents_1 = NE.meaningful_sents(PERSON_sents_1, ['PERSON'], PEOPLE_1)
	useful_sents_2 = NE.meaningful_sents(PERSON_sents_2, ['PERSON'], PEOPLE_2)


	######################################
	#	Extracting informations
	######################################

	"""
	Now that we have extracted the useful sentences,
	we can begin to mine the information inside them.
	"""

	# NER_tags to look for in the sentence
	NER_tags = ['PERSON', 'LOC', 'GPE', 'DATE', 'TIME']
	POS_tags = ['NN', 'NNP', 'NNPS', 'NNS', 'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']

	# For every sent: find the Person and {PERSON_1 : [link1: freq, link2: freq], PERSON_2: [link1: freq, link2: freq]}
	links_1 = NE.extract_links(useful_sents_1, {'PERSON' : PEOPLE_1}, NER_tags, POS_tags)
	links_2 = NE.extract_links(useful_sents_2, {'PERSON' : PEOPLE_2}, NER_tags, POS_tags)

	# Extract the frequency of each link
	links_freqs_1 = NE.extract_link_freqs(links_1)
	links_freqs_2 = NE.extract_link_freqs(links_2)

	#with open('tests/links_freqs_1.txt', 'w') as output:
		#output.write(str(links_freqs_1))

	# Extract the most frequent items for each field
	most_freq_1 = NE.rank_link_freqs(links_freqs_1, 10)
	most_freq_2 = NE.rank_link_freqs(links_freqs_2, 10)

	# Print infos TEXT_1
	for NER in most_freq_1:
		for leaf in most_freq_1[NER]:
			for link_type in most_freq_1[NER][leaf]:
				nc_1 = OUT.complex_container(leaf + ' + ' + link_type, most_freq_1[NER][leaf][link_type], soup)
				col_1.append(nc_1)
				print('added', leaf, ' + ', link_type,'to project/index.html')

	# Print infos TEXT_2
	for NER in most_freq_2:
		for leaf in most_freq_2[NER]:
			for link_type in most_freq_2[NER][leaf]:
				nc_2 = OUT.complex_container(leaf + ' + ' + link_type, most_freq_2[NER][leaf][link_type], soup)
				col_2.append(nc_2)
				print('added', leaf, ' + ', link_type,'to project/index.html')



	# Get the max-prob sentence of lenght between 8 and 12 token

	# Select sents of lenght between 8 and 12 token containing 
	selected_sents_1 = tool.sents_of_len(NE.trees_2_toks(useful_sents_1), 8, 12)
	selected_sents_2 = tool.sents_of_len(NE.trees_2_toks(useful_sents_2), 8, 12)

	sents_4_person_1 = NE.assign_sent_2_person(selected_sents_1, PEOPLE_1)
	sents_4_person_2 = NE.assign_sent_2_person(selected_sents_2, PEOPLE_2)

	# Compute the probability for each sentence for each important person in the text
	max_markow_1 = {}
	for person in sents_4_person_1:
		max_markow_1[person] = NE.get_max_markow(sents_4_person_1[person], fd(toks_1), len(t_1), False) 

	max_markow_2 = {}
	for person in sents_4_person_2:
		max_markow_2[person] = NE.get_max_markow(sents_4_person_2[person], fd(toks_2), len(t_2), False) 
	
	# Print Markov probabilities
	for person in max_markow_1:
		nc_1 = OUT.tok_sent_container('Probable sentence for ' + person, max_markow_1[person], soup)
		col_1.append(nc_1)
		print('added '+ 'Probable sentence for ' + person + 'to project/index.html')

	for person in max_markow_2:
		nc_2 = OUT.tok_sent_container('Probable sentence for ' + person, max_markow_2[person], soup)
		col_2.append(nc_2)
		print('added '+ 'Probable sentence for ' + person + 'to project/index.html')
	
	# Final prints
	title_1 = soup.new_tag('p', attrs={'id' : 'book-1'})
	title_1.insert(1,'Alice in Wonderland')
	soup.body.append(title_1)

	title_2 = soup.new_tag('p', attrs={'id' : 'book-2'})
	title_2.insert(1,'Second Variety')
	soup.body.append(title_2)

	# Exporting output
	with open('output/index_2.html', 'w') as h:
		h.write(str(soup))



main(sys.argv[1], sys.argv[2])