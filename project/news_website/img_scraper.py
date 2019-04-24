from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import operator
import sqlite3
import json

def get_article_img():

	article_data = get_article_data()

	for article in article_data:

		article_tags = article[2]

		article_tag_list = article_tags.split(',')

		img_query = article_tag_list[0]

		article_ID = article[1]



		img_link = search_forunsplash_image(img_query)


		update_img_in_db(img_link, article_ID)


def update_img_in_db(img_link, article_ID):

	#with sqlite3.connect('/Users/jan-philippthiele/FoundationsFolder/foundations/project/instance/news_articles.sqlite') as db_connection:
	with sqlite3.connect('/home/janphilipp_thiele/foundations/project/instance/news_articles.sqlite') as db_connection:
		db_cursor = db_connection.cursor()

		db_cursor.execute("""UPDATE Links SET IMG_LINK = (?) WHERE ID = (?);""", (img_link, article_ID))
		db_connection.commit()
		


def search_forunsplash_image(query):

	API_Link = 'https://api.unsplash.com/search/photos?page=1&query={}&per_page=1&orientation=landscape&client_id={}'

	API_Key = '70d7ba9bb2607317ee3d673670a1de33d1d976d4c99d576d346d88775943f54e'

	API_query = API_Link.format(query, API_Key)

	with closing(get(API_query, stream=True)) as resp:

		decoded_response = decode_json(resp.content)

		img_link = decoded_response['results'][0]['urls']['full']

		return img_link

def decode_json(tup):
	
	try:
		tup_json = json.loads(tup)                                                 
		return tup_json
	except ValueError: # includes JSONDecodeError                          
		logger.error(error)                                                           
		return None

def get_article_data():

	#with sqlite3.connect('/Users/jan-philippthiele/FoundationsFolder/foundations/project/instance/news_articles.sqlite') as db_connection:
	with sqlite3.connect('/home/janphilipp_thiele/foundations/project/instance/news_articles.sqlite') as db_connection:
		db_cursor = db_connection.cursor()

		article_data =db_cursor.execute("""SELECT IMG_LINK, ID, TAGS, Source_ID FROM Links WHERE IMG_LINK = 'None';""").fetchall()

	return article_data

