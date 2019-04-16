from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import operator
import sqlite3
import json

def decode_json(tup):
	
	try:                                                                           
		tup_json = json.loads(tup)                                                 
		print('json decoded')
		return tup_json                                                            
	except ValueError: # includes JSONDecodeError                          
		logger.error(error)                                                           
		return None


def search_forunsplash_image():

	query = 'chicago'

	API_Link = 'https://api.unsplash.com/search/photos?page=1&query={}&per_page=1&orientation=landscape&client_id={}'

	API_Key = '70d7ba9bb2607317ee3d673670a1de33d1d976d4c99d576d346d88775943f54e'

	API_query = API_Link.format(query, API_Key)

	with closing(get(API_query, stream=True)) as resp:

		decoded_response = decode_json(resp.content)

		img_link = decoded_response['results'][0]['urls']['full']
		print(img_link)

search_forunsplash_image()