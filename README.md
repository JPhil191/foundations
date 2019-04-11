# foundations

The foundations project

###Description
Included is a webscraper, scraping and saving articles from the New York Times and zeit.de. The articles are saved in an sqlite database. The articles are then being presented on the website.

### Installing

You will need to install the following

- Python
- Virtualenv
- waitress
- BeautifulSoup4
- requests
- flask

Start by creating the virtual environment:
```
/foundations/
python3 -m venv venv
Activate the virtual environment
```
```
/foundations/
source venv/bin/activate
Install waitress (Use pip not pip3)
```
```
/foundations/
pip install waitress requests BeautifulSoup4 flask
```

## Starting locally

Go to the directory where you installed the project

Go to the /project directory

```
export FLASK_APP=news_website
export FLASK_ENV=development
flask run
```

### Starting website on a server

Activate the Virtualenv 

```
source venv/bin/activate
```

Go to the /foundations/project directory and start the server.py with sudo
```
sudo python3 server.py
```

