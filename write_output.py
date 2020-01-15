from bs4 import BeautifulSoup, NavigableString

def init_html(): 
	"""
	Prepares the layout of the output
	"""
	return """
	<!DOCTYPE html>
	<html lang="en">
	<head>

		<meta charset="utf-8">

		<title>CL- project</title>

		<meta name="description" content="Exam project for Computational Linguistics - Università di Pisa">
		<meta name="author" content="Marta Fioravanti - 603574">

		<link href="https://fonts.googleapis.com/css?family=Titillium+Web:400,700&display=swap" rel="stylesheet">
		<link href="https://fonts.googleapis.com/css?family=Space+Mono:400,700&display=swap" rel="stylesheet">
		
		<link rel="stylesheet" type="text/css" href="style.css">

	</head>
	<body>

		<header>
			<h1>Comparison between two texts</h1>
		</header>

		<div id="main">

			<div id="text-1-container" class="info-container">

			</div>

			<div id="text-2-container" class="info-container">
				
			</div>
			
		</div>

		<footer>
			<p>Marta Fioravanti - 603574</p>
			<p>Exam project for Computational Linguistics - Università di Pisa</p>
		</footer>

	</body>
	</html>
	"""

def create_container(title, text, soup):
	"""
	Creates an html object containing a title and a p
	"""

	content = soup.new_tag('div', attrs={'class' : 'info-content'})
	title_content = soup.new_tag('h3', attrs={'class' : 'content-title'})
	content_content = soup.new_tag('p', attrs={'class' : 'content-content'})

	title_content.string = title
	content_content.string = text

	content.append(title_content)
	content.append(content_content)

	return content

def create_img_container(title, img, soup):
	"""
	Creates an html object containing a title and an image
	"""

	content = soup.new_tag('div', attrs={'class' : 'info-content'})
	title_content = soup.new_tag('h3', attrs={'class' : 'content-title'})
	content_content = soup.new_tag('p', attrs={'class' : 'content-content'})
	image = soup.new_tag('img', src=img, attrs={'class' : 'content-img'})

	title_content.string = title
	content_content.append(image)

	content.append(title_content)
	content.append(content_content)

	return content

def complex_container(title, p_list, soup, th=['', 'element', 'frequency']):
	"""
	Creates an html object containing a title and a set of p
	from a list of tuples
	"""

	content = soup.new_tag('div', attrs={'class' : 'info-content'})
	title_content = soup.new_tag('h3', attrs={'class' : 'content-title'})
	title_content.string = title

	content.append(title_content)

	counter = 0

	table_content = soup.new_tag('table', attrs={'class' : 'content-table'})

	table_tr = soup.new_tag('tr')

	table_th_0 = soup.new_tag('th')
	table_th_0.string = th[0]
	table_tr.append(table_th_0)
	table_th_1 = soup.new_tag('th')
	table_th_1.string = th[1]
	table_tr.append(table_th_1)
	table_th_2 = soup.new_tag('th')
	table_th_2.string = th[2]
	table_tr.append(table_th_2)

	table_content.append(table_tr)


	for k, v in p_list:
		counter += 1
		
		table_row = soup.new_tag('tr')

		id_cell = soup.new_tag('td', attrs={'class' : 'id-cell'})
		text_cell = soup.new_tag('td')
		stats_cell = soup.new_tag('td')

		id_cell.string = str(counter) + '.'
		text_cell.string = '"' + str(k) + '"'
		stats_cell.string = str(v)

		table_row.append(id_cell)
		table_row.append(text_cell)
		table_row.append(stats_cell)

		table_content.append(table_row)

	content.append(table_content)

	return content

def more_complex_container(title, p_list, soup, th=['', 'elements', 'probability']):
	"""
	Creates an html object containing a title and a set of p
	from a list of tuples containing a tuple
	"""

	content = soup.new_tag('div', attrs={'class' : 'info-content'})
	title_content = soup.new_tag('h3', attrs={'class' : 'content-title'})
	title_content.string = title

	content.append(title_content)

	counter = 0

	table_content = soup.new_tag('table', attrs={'class' : 'content-table'})

	table_tr = soup.new_tag('tr')

	table_th_0 = soup.new_tag('th')
	table_th_0.string = th[0]
	table_tr.append(table_th_0)
	table_th_1 = soup.new_tag('th')
	table_th_1.string = th[1]
	table_tr.append(table_th_1)
	table_th_2 = soup.new_tag('th')
	table_th_2.string = th[2]
	table_tr.append(table_th_2)

	table_content.append(table_tr)

	for k, v in p_list:
		counter += 1
		
		table_row = soup.new_tag('tr')

		id_cell = soup.new_tag('td', attrs={'class' : 'id-cell'})
		text_cell = soup.new_tag('td')
		stats_cell = soup.new_tag('td')

		id_cell.string = str(counter) + '.'
		text_cell.string = '"' + str(k[0]) + '"' + ' + ' + '"' + str(k[1]) + '"'
		stats_cell.string = str(minify(v))

		table_row.append(id_cell)
		table_row.append(text_cell)
		table_row.append(stats_cell)

		table_content.append(table_row)

	content.append(table_content)

	return content

def tok_sent_container(title, p_list, soup):
	"""
	Creates an html object containing a title,
	a sentence from a token list and a value associated
	"""

	content = soup.new_tag('div', attrs={'class' : 'info-content'})
	title_content = soup.new_tag('h3', attrs={'class' : 'content-title'})
	title_content.string = title

	content.append(title_content)

	s = ''

	for tok in p_list[0]:
		content_content_0 = soup.new_tag("p", attrs={'class' : 'content-content'})
		s += tok + ' '
	
	s = s[:-1]

	content_content_0.string = s
	content_content_1 = soup.new_tag('p', attrs={'class' : 'content-content'})
	content_content_1.string = 'Markov 0:\t' + str(p_list[1])[:5]

	content.append(content_content_0)
	content.append(content_content_1)

	return content



def minify (n):
	"""
	Returns an approximated float
	"""
	return "%.4f" % n












