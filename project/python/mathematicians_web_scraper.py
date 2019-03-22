from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import json
import operator

def simple_get(url):
	
    #Attempts to get the content at `url` by making an HTTP GET request.
    #If the content-type of response is some kind of HTML/XML, return the
    #text content, otherwise return None.
    
    try:
    	#the with ensures that our file is being closed again and saves us some coding
    	#using the closing function is good practice to ensure that any network resources
    	#are freed when they go out of scope in that with block
    				#here we are making the GET request at the url we passed into the function
    	with closing(get(url, stream=True)) as resp:
    		#calling the is_good_response function to know whether we have an html file
    		#if is_good_response(resp):
    		return resp.content
    		#if something goes wrong like we are having a bad url we return None
    		#else:
    		#	return None

    except RequestExceptions as e:
    	#Calls the log error function to report the issue
    	log_error("Error during requests to {0} : {1}".format(url, str(e)))
    	return None


def is_good_response(resp):
	#returns True if the response seems to be HTML, False otherwise
	content_type = resp.headers["Content-Type"].lower()
	return (resp.status_code == 200
			and content_type is not None
			and content_type.find("html") > -1)


def log_error(e):
	# It is always a good idea to log errors. 
    #This function just prints them, but you can
    #make it do anything.
	print(e)


def get_names():
    #Downloads the page where the list of mathematicians is found
    #and returns a list of strings, one per mathematician
    url = "http://www.fabpedigree.com/james/mathmen.htm"
        #calling simple_get to download the page
    response = simple_get(url)

    #checking if we actually got back some html
    if response is not None:
        #passing the raw html as an html.parser to BeautifulSoup so we
        #do not get an warning print
        html = BeautifulSoup(response, "html.parser")
        #not clear what set() does
        names = set()
                        #select mehtod lets us locate all the html li elemnts
                        # now we can loop through them
        for li in html.select("li"):
                       #splitting at every new line where also the new name starts
            for name in li.text.split("\n"):
                #checking if the is actually something we can add to a list
                if len(name) > 0:
                                    #strip returns a copy of a string
                    names.add(name.strip())
                else:
                    continue    
                #returning names in a list
        return list(names)
    # Raise an Exception if we failed to get any data from the url
    raise Exception("Error retrieving content at {}".format(url))


def convert(tup):                                                               
    """                                                                            
    Convert to python dict.                                                        
    """                                                                            
    try:                                                                           
        tup_json = json.loads(tup)                                                 
        return tup_json                                                            
    except ValueError: # includes JSONDecodeError                          
        logger.error(error)                                                           
        return None 



def get_hits_on_name(name):
    #Accepts a `name` of a mathematician and returns the number
    #of hits that mathematician's Wikipedia page received in the 
    #last 60 days, as an `int`
    name2 = name.split()
    name2 = "_".join(name2)
    #url_root is a template string that is used to build a URL.
    url_root = "https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia.org/all-access/user/{}/daily/20180101/20180102"
    response = simple_get(url_root.format(name2))
    
    data = convert(response)


    if data is not None:

        index = 0
        total_views = 0
        
        for views in data:
            try:
                views = data["items"][index]["views"]
                index += 1
                total_views += views
            
                average_views = total_views / (index+1)
                print("{} checked".format(name))
                return int(average_views)
            except KeyError:
                return None


    else:            
        log_error("No pageviews found for {}".format(name))
        return None







mathematicians_list = get_names()
popularity = {}

for mathematician in mathematicians_list:

    average_views = get_hits_on_name(mathematician)

    if average_views == None:
        continue
    else:
        popularity.update( {mathematician: average_views} )

ranking = sorted(popularity.items(), key = lambda x: x[1], reverse=True)

index = 0
for mathematician in ranking:
    index+=1
    print("{}: {} with {} views per day in 2018.".format(index, mathematician[0], mathematician[1]))










































