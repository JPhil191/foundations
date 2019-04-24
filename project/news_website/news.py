import functools
import sqlite3
from flask import current_app, g
from flask.cli import with_appcontext


from flask import (
	Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from news_website.db import get_db
from . import news_webscraper
from . import img_scraper
from . import empty_database

bp = Blueprint('news', __name__)
@bp.route('/')
def index():
	
	
	

	db_connection = get_db()
	db_cursor = db_connection.cursor()
	db_length = db_cursor.execute("""SELECT COUNT(*) FROM Links ;""").fetchall()
	print(db_length)
	#if db_length > 22 :
	#	empty_database.empty_db()
	#news_webscraper.get_zeit_article_links()
	#news_webscraper.get_nyt_articles()
	
	#img_scraper.get_article_img()


	news = db_cursor.execute("""SELECT * FROM Links ORDER BY DateandTime DESC LIMIT 1, 5000;""").fetchall()
	db_cursor.close()
	return render_template('news/landingpage.html', news=news)


@bp.route('/politik')
def politik():


	db_connection = get_db()
	db_cursor = db_connection.cursor()

	news = db_cursor.execute("""SELECT * FROM Links WHERE Topic_ID=1 ORDER BY DateandTime DESC LIMIT 1, 5000;""").fetchall()
	db_cursor.close()
	return render_template('news/landingpage.html', news=news)

@bp.route('/wirtschaft')
def wirtschaft():

	db_connection = get_db()
	db_cursor = db_connection.cursor()

	news = db_cursor.execute("""SELECT * FROM Links WHERE Topic_ID=3 ORDER BY DateandTime DESC LIMIT 1, 5000;""").fetchall()
	db_cursor.close()
	return render_template('news/landingpage.html', news=news)

@bp.route('/gesellschaft')
def gesellschaft():

	db_connection = get_db()
	db_cursor = db_connection.cursor()

	news = db_cursor.execute("""SELECT * FROM Links WHERE Topic_ID=4 ORDER BY DateandTime DESC LIMIT 1, 5000;""").fetchall()
	db_cursor.close()
	return render_template('news/landingpage.html', news=news)

@bp.route('/sport')
def sport():

	db_connection = get_db()
	db_cursor = db_connection.cursor()

	news = db_cursor.execute("""SELECT * FROM Links WHERE Topic_ID=5 ORDER BY DateandTime DESC LIMIT 1, 5000;""").fetchall()
	db_cursor.close()
	return render_template('news/landingpage.html', news=news)


@bp.route('/technik')
def technik():

	db_connection = get_db()
	db_cursor = db_connection.cursor()

	news = db_cursor.execute("""SELECT * FROM Links WHERE Topic_ID=2 ORDER BY DateandTime DESC LIMIT 1, 5000;""").fetchall()
	db_cursor.close()
	return render_template('news/landingpage.html', news=news)

@bp.route('/zeit')
def zeit():

	db_connection = get_db()
	db_cursor = db_connection.cursor()

	news = db_cursor.execute("""SELECT * FROM Links WHERE Source_ID = 1 ORDER BY DateandTime DESC LIMIT 1, 5000;""").fetchall()
	db_cursor.close()
	return render_template('news/landingpage.html', news=news)

@bp.route('/nyt')
def nyt():

	db_connection = get_db()
	db_cursor = db_connection.cursor()

	news = db_cursor.execute("""SELECT * FROM Links WHERE Source_ID = 2 ORDER BY DateandTime DESC LIMIT 1, 5000;""").fetchall()
	db_cursor.close()
	return render_template('news/landingpage.html', news=news)


@bp.route('/<int:article_id>/reader')
def reader(article_id):

	article = get_article_from_db(article_id)

	return render_template('news/reader.html', article=article)

def get_article_from_db(article_id):

	db_connection = get_db()
	db_cursor = db_connection.cursor()

	article = db_cursor.execute("""SELECT * FROM Links WHERE ID = (?) ;""", (article_id,)).fetchall()

	return article










