from requests import get
from contextlib import closing
import json

def decode_json(tup):
	
	try:                                                                           
		tup_json = json.loads(tup)                                                 
		return tup_json                                                            
	except ValueError: # includes JSONDecodeError                          
		logger.error(error)                                                           
		return None



def translate_tags(tags):

	API_URL = "https://translate.googleapis.com/translate_a/single?client=gtx&sl=de&tl=en&dt=t&q={}"

	for tag in tags:

		API_query = API_URL.format(tag) 

		with closing(get(API_query, stream=True)) as resp:

			decoded_response = decode_json(resp.content)

			print (decoded_response[0][0][0])


tag_list = ['Politik', 'Gesellschaft', 'Wirtschaft']

translate_tags(tag_list)