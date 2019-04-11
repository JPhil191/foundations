from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import operator
import sqlite3



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
						print("found article")
						print(link)
						process_zeit_article_link(link)
						counter +=1
							

					else:
						print("kein artikel")

	

def process_zeit_article_link(link):
	
	

	try:
		#using the closing function is good practice to ensure that any network resources
    	#are freed when they go out of scope in that with block
		with closing(get(link+"/komplettansicht", stream=True)) as resp:
		#checking for a multi-page article	
			if is_good_response(resp) == True:
				print('found multi page')
				html = BeautifulSoup(resp.content, 'html.parser')
				link = (link + "/komplettansicht")
				paragraphs = get_paragraphs(html)
				if len(paragraphs)>1:
					teaser = paragraphs[0]
				else:
					teaser = "Readcarticle."
				full_article = "<br>".join(paragraphs)
				headline = get_article_headline(html)
				img_link = get_img_link(html)
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
					full_article = "<br>".join(paragraphs)
					headline = get_article_headline(html)
					img_link = get_img_link(html)

	except RequestException as e:
		print(link)
		log_error("Error during requests to {0} : {1}".format(link, str(e)))

	if len(full_article) > 1200:
		write_to_database(link, headline, full_article, img_link, teaser)

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
		full_article = "\n<br>\n<br>".join(paragraphs)
		headline = get_article_headline(html)
		img_link = get_img_link(html)

		if len(full_article) > 1200:
			#if db_cursor.execute('SELECT IMG_LINK FROM Links WHERE LINK = ?', (link,)).fetchone() is None:
				
			write_to_database(link, headline, full_article, img_link, teaser)

	

def write_to_database(link, headline, content, img_link, teaser):
	
	if img_link == None and 'Brexit' in content:
			img_link = 'https://images.unsplash.com/photo-1483972117325-ce4920ff780b?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=2100&q=80'

	if img_link == None and 'Trump' in content:
		img_link = 'https://images.unsplash.com/photo-1550531996-ff3dcede9477?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=2104&q=80'

	elif img_link == None and '/politics/' or img_link == None and '/politik/' in link:
		img_link = 'https://images.unsplash.com/photo-1529107386315-e1a2ed48a620?ixlib=rb-1.2.1&auto=format&fit=crop&w=2100&q=80'
	
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
			

		db_cursor.execute("INSERT INTO Links (LINK, Source_ID, Topic_ID, HEADLINE, CONTENT, IMG_LINK, TEASER) VALUES (?, 2, ?, ?, ?, ?, ?);", (link, Topic_ID, headline, content, img_link, teaser))
		print("nyt written to database")
	elif 'zeit.de' in link:
			
		if '/politik/' in link:
			Topic_ID = 1
		elif '/gesellschaft/' in link:
			Topic_ID = 4
		elif '/sport/' in link:
			Topic_ID = 5
		elif '/wirtschaft/' in link:
			Topic_ID = 3
		else:
			Topic_ID = 4
		db_cursor.execute("INSERT INTO Links (LINK, Source_ID, Topic_ID, HEADLINE, CONTENT, IMG_LINK, TEASER) VALUES (?, 1, ?, ?, ?, ?, ?);", (link, Topic_ID, headline, content, img_link, teaser))
		print("zeit article written to database")



def printing():
	db_cursor.execute("SELECT * from Links")
	list_links = db_cursor.fetchall()
	db_connection.commit()


zeit_article_dict = {}

nyt_article_dict = {}

#db_connection = sqlite3.connect('/Users/jan-philippthiele/FoundationsFolder/foundations/project/instance/news_articles.sqlite')
db_connection = sqlite3.connect('/home/janphilipp_thiele/foundations/project/instance/news_articles.sqlite')
db_cursor = db_connection.cursor()


#get_nyt_articles()
#get_zeit_article_links()
#printing()


	 























