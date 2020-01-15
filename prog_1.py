"""
python3 prog_1.py texts/alice.txt texts/second.txt
"""

import sys
#	NLTK modules
import nltk
from nltk import word_tokenize as wt
from nltk import pos_tag as POS
from nltk import bigrams as bigr
#	Statistical module
import LC.tok as LC
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
	Extracts basic stats from 2 text files
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

	######################################
	#	Extracting informations
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

	# Print number of sentences
	nc_1 = OUT.create_container('Number of sentences', str(len(sents_1)), soup)
	nc_2 = OUT.create_container('Number of sentences', str(len(sents_2)), soup)
	col_1.append(nc_1)
	col_2.append(nc_2)
	print('added Number of sentences to project/index.html')

	# Print number of tokens
	nc_1 = OUT.create_container('Number of tokens', str(len(toks_1)), soup)
	nc_2 = OUT.create_container('Number of tokens', str(len(toks_2)), soup)
	col_1.append(nc_1)
	col_2.append(nc_2)
	print('added Number of tokens to project/index.html')

	# Print mean sentence length
	nc_1 = OUT.create_container('Mean sentence length', str(tool.minify(LC.mean_len(s_toks_1))), soup)
	nc_2 = OUT.create_container('Mean sentence length', str(tool.minify(LC.mean_len(s_toks_2))), soup)
	col_1.append(nc_1)
	col_2.append(nc_2)
	print('added Mean sentence length to project/index.html')

	# Print word length
	nc_1 = OUT.create_container('Mean word length', str(tool.minify(LC.mean_len(toks_1))), soup)
	nc_2 = OUT.create_container('Mean word length', str(tool.minify(LC.mean_len(toks_2))), soup)
	col_1.append(nc_1)
	col_2.append(nc_2)
	print('added Mean word length to project/index.html')



	# Vocab
	voc_1 = LC.create_vocab(toks_1)
	voc_2 = LC.create_vocab(toks_2)

	# Print vocabulary dimension

	nc_1 = OUT.create_container('Vocabulary dimension', str(len(voc_1)), soup)
	nc_2 = OUT.create_container('Vocabulary dimension', str(len(voc_2)), soup)
	col_1.append(nc_1)
	col_2.append(nc_2)
	print('added Vocabulary dimension to project/index.html')


	# Frequencies
	freq_1 = LC.freqs(toks_1, voc_1)
	freq_2 = LC.freqs(toks_2, voc_2)

	# Hapax_list
	hapax_1 = LC.get_hapax(freq_1)
	hapax_2 = LC.get_hapax(freq_2)

	# Print number of hapaxes
	nc_1 = OUT.create_container('Number of hapaxes', str(len(hapax_1)), soup)
	nc_2 = OUT.create_container('Number of hapaxes', str(len(hapax_2)), soup)
	col_1.append(nc_1)
	col_2.append(nc_2)
	print('added Number of hapaxes to project/index.html')

	print('PLOTTING HAPAXES - DISTRIBUTION...')

	# Plotting Hapaxes' distribution 
	LC.hapax_distr(toks_1, 1000, "Alice in Wonderland - Carrol")
	LC.hapax_distr(toks_2, 1000, "Second Variety - Dick")


	# Print plots
	nc_1 = OUT.create_img_container('Hapax distribution', '../plots/Alice in Wonderland - Carrol.svg', soup)
	nc_2 = OUT.create_img_container('Hapax distribution', '../plots/Second Variety - Dick.svg', soup)
	col_1.append(nc_1)
	col_2.append(nc_2)
	print('added Hapax distribution to project/index.html')

	# POS tagging
	POS_1 = POS(toks_1)
	POS_2 = POS(toks_2)

	# POS frequency
	"""
	Getting the frequency of every POS in the two texts
	"""

	POS_freqs_1 = LC.get_POS_freqs(POS_1)
	POS_freqs_2 = LC.get_POS_freqs(POS_2)


	NN_1 = POS_freqs_1['NN'] + POS_freqs_1['NNS'] + POS_freqs_1['NNP'] + POS_freqs_1['NNPS']
	VB_1 = POS_freqs_1['VB'] + POS_freqs_1['VBD'] + POS_freqs_1['VBG'] + POS_freqs_1['VBN'] + POS_freqs_1['VBP'] + POS_freqs_1['VBZ']

	NN_2 = POS_freqs_2['NN'] + POS_freqs_2['NNS'] + POS_freqs_2['NNP'] + POS_freqs_2['NNPS']
	VB_2 = POS_freqs_2['VB'] + POS_freqs_2['VBD'] + POS_freqs_2['VBG'] + POS_freqs_2['VBN'] + POS_freqs_2['VBP'] + POS_freqs_2['VBZ']

	# Print Nouns / Verbs
	nc_1 = OUT.create_container('Nouns / Verbs', str(tool.minify(NN_1 / VB_1)), soup)
	nc_2 = OUT.create_container('Nouns / Verbs', str(tool.minify(NN_2 / VB_2)), soup)
	col_1.append(nc_1)
	col_2.append(nc_2)
	print('added Nouns / Verbs to project/index.html')



	POS_rank_1 = LC.rank(POS_freqs_1)
	POS_rank_2 = LC.rank(POS_freqs_2)

	# Print most frequent POS
	nc_1 = OUT.complex_container('Most frequent POS', list(POS_rank_1)[:10], soup)
	nc_2 = OUT.complex_container('Most frequent POS', list(POS_rank_2)[:10], soup)
	col_1.append(nc_1)
	col_2.append(nc_2)
	print('added Most frequent POS to project/index.html')



	# POS bigrams
	"""
	Getting the frequency of every POS-couple in the two texts
	"""
	POS_bi_1 = LC.tag_bigrams(POS_1)
	POS_bi_2 = LC.tag_bigrams(POS_2)

	POS_bi_set_1 = list(set(POS_bi_1))
	POS_bi_set_2 = list(set(POS_bi_2))


	POS_bi_freq_1 = LC.freqs(POS_bi_1, POS_bi_set_1)		
	POS_bi_freq_2 = LC.freqs(POS_bi_2, POS_bi_set_2)

	# POS Conditioned probabilities
	"""
	Now that we have the frequencies of every POS 
	and every couple of POS, we can compute 
	the conditioned probability for each couple.
	"""

	POS_cond_prob_1 = LC.get_cond_prob(POS_bi_freq_1, POS_freqs_1)
	POS_cond_prob_2 = LC.get_cond_prob(POS_bi_freq_2, POS_freqs_2)


	# Print conditioned-probability
	nc_1 = OUT.more_complex_container('Top conditioned-probable POS', LC.rank(POS_cond_prob_1)[:10], soup, ['', 'bigrams', 'probability'])
	nc_2 = OUT.more_complex_container('Top conditioned-probable POS', LC.rank(POS_cond_prob_2)[:10], soup, ['', 'bigrams', 'probability'])
	col_1.append(nc_1)
	col_2.append(nc_2)
	print('added Top conditioned-probable POS to project/index.html')



	# POS Local Mutual Information

	POS_bi_LMI_1 = LC.get_LMI(POS_bi_freq_1, len(POS_bi_1), POS_freqs_1, len(POS_1), POS_bi_set_1)
	POS_bi_LMI_2 = LC.get_LMI(POS_bi_freq_2, len(POS_bi_2), POS_freqs_2, len(POS_2), POS_bi_set_2)

	ranked_POS_bi_LMI_1 = LC.rank(POS_bi_LMI_1)
	ranked_POS_bi_LMI_2 = LC.rank(POS_bi_LMI_2)

	# Print related bigrams
	nc_1 = OUT.more_complex_container('Top LMI-related bigrams', ranked_POS_bi_LMI_1[:10], soup, ['', 'bigrams', 'LMI'])
	nc_2 = OUT.more_complex_container('Top LMI-related bigrams', ranked_POS_bi_LMI_2[:10], soup, ['', 'bigrams', 'LMI'])
	col_1.append(nc_1)
	col_2.append(nc_2)
	print('added Top LMI-related bigrams to project/index.html')

	# Final prints
	title_1 = soup.new_tag('p', attrs={'id' : 'book-1'})
	title_1.insert(1,'Alice in Wonderland')
	soup.body.append(title_1)

	title_2 = soup.new_tag('p', attrs={'id' : 'book-2'})
	title_2.insert(1,'Second Variety')
	soup.body.append(title_2)

	# Exporting output
	with open('output/index_1.html', 'w') as h:
		h.write(str(soup))



main(sys.argv[1], sys.argv[2])




