from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import operator
import sqlite3
import json



def get_html(url):
	try:
		#using the closing function is good practice to ensure that any network resources
    	#are freed when they go out of scope in that with block
		with closing(get(url, stream=True)) as resp:

			if is_good_response(resp):

				#resp.coontent means that we are getting the response in bites
				return resp.content
			else:
				return None

	except RequestException as e:
		log_error("Error during requests to {0} : {1}".format(url, str(e)))
		return None


def is_good_response(resp):
	#metod returns true when response is html
	#as a response you get a dictonary containing the Contentype
	content_type = resp.headers["Content-Type"].lower()
								#means OK
	return (resp.status_code == 200
			and content_type is not None
			and content_type.find("html") > -1)


def log_error(e):
	# It is always a good idea to log errors. 
    #This function just prints them, but you can
    #make it do anything.
	print("Error")


def get_zeit_article_links():
	url = "https://www.zeit.de/index"
	response = get_html(url)

	zeit_article_list = []

	if response is not None:

		html = BeautifulSoup(response, "html.parser")

		counter = 0
		for h3 in html.find_all('h3'):
			for a in h3.find_all('a'):
				link = a.get('href')

				if counter == 8:
					break
				else:
				
					
					if "teaser-small__heading" in str(h3) or "teaser-classic__headin" in str(h3):
						counter +=1
						print('found')
						zeit_article_list.append(link)	

					else:
						print("kein artikel")

	process_zeit_article_links(zeit_article_list)

	

def process_zeit_article_links(link_list):
	
	for link in link_list:

		try:
			#using the closing function is good practice to ensure that any network resources
	    	#are freed when they go out of scope in that with block
			with closing(get(link+"/komplettansicht", stream=True)) as resp:
			#checking for a multi-page article	
				if is_good_response(resp) == True:
					html = BeautifulSoup(resp.content, 'html.parser')
					link = (link + "/komplettansicht")
					paragraphs = get_paragraphs(html)
					if len(paragraphs)>1:
						teaser = paragraphs[0]
					else:
						teaser = "Readcarticle."
					full_article = "\n\n".join(paragraphs)
					headline = get_article_headline(html)
					img_link_small = get_img_link(html)
					img_link_small = str(img_link_small)
					img_link = img_link_small.replace('822x462', '1920x1080')
					zeit_article_tags = get_zeit_article_tags(html)

					#resp.coontent means that we are getting the response in bites with the cintent of the page
					

				
				else:
					with closing(get(link, stream=True)) as resp:
						html = BeautifulSoup(resp.content, 'html.parser')
						link = (link)
						paragraphs = get_paragraphs(html)
						if len(paragraphs)>1:
							teaser = paragraphs[0]
						else:
							teaser = "Readcarticle."
						full_article = "\n\n".join(paragraphs)
						headline = get_article_headline(html)
						img_link_small = get_img_link(html)
						img_link_small = str(img_link_small)
						img_link = img_link_small.replace('822x462', '1920x1080')
						zeit_article_tags = get_zeit_article_tags(html)


						#tags = translate_tags(need to get tags)

		except RequestException as e:
			print(link)
			log_error("Error during requests to {0} : {1}".format(link, str(e)))

		if len(full_article) > 1200:
			#with sqlite3.connect('/Users/jan-philippthiele/FoundationsFolder/foundations/project/instance/news_articles.sqlite') as db_connection:
			with sqlite3.connect('/home/janphilipp_thiele/foundations/project/instance/news_articles.sqlite') as db_connection:
				db_cursor = db_connection.cursor()
				if db_cursor.execute('SELECT IMG_LINK FROM Links WHERE LINK = ?', (link,)).fetchone() is None:
					write_to_database(link, headline, full_article, img_link, teaser, zeit_article_tags)

def get_paragraphs(html):
	
	
	paragraphs = []
	for p in html.find_all("p"):
		
		if  "paragraph article__item" in str(p):
			#calling a function that cleans the article to pure text without \n etc.
			text = clean_text(p.text)
			paragraphs.append(text)

		elif 'css-1ygdjhk evys1bk0' in str(p):
			text = clean_text(p.text)
			paragraphs.append(text)

		else:
			continue		

		
	return paragraphs

	

def clean_text(text):
	cleaned_text = text.replace('\n', ' ').replace('\xa0', ' ').replace('    ','')
	return cleaned_text

def get_article_headline(html):
	
	headline = ""
	for h1 in html.find_all("h1"):
		headline = h1.text
	
	

	return headline

def get_img_link(html):

	for img in html.find_all("img"):
		if "article__media-item" in str(img) or "css-11cwn6f" in str(img):
			img_link = img.get("src")	
			return img_link

def get_zeit_article_tags(html):

	tags = []

	for a in html.find_all('a'):

		if len(tags) == 3:
			break
		elif "article-tags__link" in str(a):
			tags.append(a.text)
		else:
			continue

	return ", ".join(tags)

def get_nyt_tags(html):

	tags = []

	for tag in html.find_all('meta'):
		if len(tags) == 3:
			break
		elif 'article:tag' in str(tag):
			tag_sent = tag.get('content')

			tag_final = str(tag_sent)
			if len(tag_final) < 20:
				tags.append(tag_final)
		else:
			continue
	return ', '.join(tags)

def get_nyt_articles():

	nyt_sections_urls = ["https://www.nytimes.com/section/technology", "https://www.nytimes.com/section/politics", "https://www.nytimes.com/section/business"]
	link_list = []
	for url in nyt_sections_urls:
		response = get_html(url)

		if response	is not None:

			html = BeautifulSoup(response, "html.parser")
			
			for a in html.find_all('a'):
				if "data-rref" in str(a):
					link = a.get('href')
					full_link = "https://www.nytimes.com" + link
					if full_link not in link_list:
						link_list.append(full_link)
	
	make_nyt_ready_for_database(link_list)



def make_nyt_ready_for_database(link_list):
#paragraphs
#headline
	for link in link_list:
		response = get_html(link)
		html = BeautifulSoup(response, "html.parser")
		
		paragraphs = get_paragraphs(html)
		if len(paragraphs)>1:
			teaser = paragraphs[0]
		else:
			teaser = "Readcarticle."
		full_article = "\n\n".join(paragraphs)
		headline = get_article_headline(html)
		img_link_small = get_img_link(html)
		img_link_small = str(img_link_small)
		img_link = img_link_small.replace('articleLarge', 'superJumbo')
		tags = get_nyt_tags(html)

		if len(full_article) > 1200:
			#with sqlite3.connect('/Users/jan-philippthiele/FoundationsFolder/foundations/project/instance/news_articles.sqlite') as db_connection:
			with sqlite3.connect('/home/janphilipp_thiele/foundations/project/instance/news_articles.sqlite') as db_connection:
				db_cursor = db_connection.cursor()
				if db_cursor.execute('SELECT IMG_LINK FROM Links WHERE LINK = ?', (link,)).fetchone() is None:
					
					write_to_database(link, headline, full_article, img_link, teaser, tags)


def decode_json(tup):
	
	try:                                                                           
		tup_json = json.loads(tup)                                                 
		return tup_json                                                            
	except ValueError: # includes JSONDecodeError                          
		logger.error(error)                                                           
		return None


def translate_tags(tags):

	API_URL = "https://translate.googleapis.com/translate_a/single?client=gtx&sl=de&tl=en&dt=t&q={}"

	translated_tags = []

	for tag in tags:

		API_query = API_URL.format(tag) 

		with closing(get(API_query, stream=True)) as resp:

			decoded_response = decode_json(resp.content)

			translated_tags.append(decoded_response)

	
	return (translated_tags)

def write_to_database(link, headline, content, img_link, teaser, tags):
	#with sqlite3.connect('/Users/jan-philippthiele/FoundationsFolder/foundations/project/instance/news_articles.sqlite') as db_connection:
	with sqlite3.connect('/home/janphilipp_thiele/foundations/project/instance/news_articles.sqlite') as db_connection:
		db_cursor = db_connection.cursor()





		Topic_ID = 1

		if 'nytimes.com' in link:
			if '/politics/' in link:
				Topic_ID = 1
			elif '/technology/' in link:
				Topic_ID = 2
			elif '/business/' in link:
				Topic_ID = 3
			else:
				Topic_ID = 4
				

			db_cursor.execute("INSERT INTO Links (LINK, Source_ID, Topic_ID, HEADLINE, CONTENT, IMG_LINK, TEASER, DateandTime, TAGS) VALUES (?, 2, ?, ?, ?, ?, ?, strftime('%d.%m.%Y %H:%M', 'now'), ?);", (link, Topic_ID, headline, content, img_link, teaser, tags))
		elif 'zeit.de' in link:
				
			if '/politik/' in link:
				Topic_ID = 1
			elif '/gesellschaft/' in link:
				Topic_ID = 4
			elif '/sport/' in link:
				Topic_ID = 5
			elif '/wirtschaft/' in link:
				Topic_ID = 3
			elif '/wissen/' in link:
				Topic_ID = 2
			else:
				Topic_ID = 4
			db_cursor.execute("INSERT INTO Links (LINK, Source_ID, Topic_ID, HEADLINE, CONTENT, IMG_LINK, TEASER, DateandTime, TAGS) VALUES (?, 1, ?, ?, ?, ?, ?, strftime('%d.%m.%Y %H:%M', 'now'), ?);", (link, Topic_ID, headline, content, img_link, teaser, tags))
		db_connection.commit()





#db_connection = sqlite3.connect('/Users/jan-philippthiele/FoundationsFolder/foundations/project/instance/news_articles.sqlite')

#db_cursor = db_connection.cursor()


#get_nyt_articles()
#get_zeit_article_links()
#printing()


	 























