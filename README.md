# foundations

the foundations project

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

What things you need to install the software and how to install them

```
Give examples
```

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
/IRT/
python3 -m venv venv
Activate the virtual environment
```
```
/IRT/
source venv/bin/activate
Install waitress (Use pip not pip3)
```
```
/IRT/
pip install waitress
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

