import functools
import sqlite3
from flask import current_app, g
from flask.cli import with_appcontext


from flask import (
	Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from news_website.db import get_db
from . import news_webscraper
from news_website.db import get_db

bp = Blueprint('news', __name__)
@bp.route('/')
def index():
	
	
	
	news_webscraper.get_nyt_articles()
	news_webscraper.get_zeit_article_links()

	db_connection = get_db()
	db_cursor = db_connection.cursor()

	main_article = db_cursor.execute("""SELECT * FROM Links LIMIT 1""").fetchall()
	news = db_cursor.execute("""SELECT LINK, Source_ID, HEADLINE, TEASER, IMG_LINK, DateandTime FROM Links ORDER BY DateandTime DESC LIMIT 1, 5000;""").fetchall()
	db_cursor.close()
	return render_template('news/index.html', news=news, main_article=main_article)


@bp.route('/politik')
def politik():


	db_connection = get_db()
	db_cursor = db_connection.cursor()

	main_article = db_cursor.execute("""SELECT * FROM Links LIMIT 1""").fetchall()
	news = db_cursor.execute("""SELECT LINK, Source_ID, HEADLINE, TEASER, IMG_LINK, DateandTime FROM Links WHERE Topic_ID=1 ORDER BY DateandTime DESC LIMIT 1, 5000;""").fetchall()
	db_cursor.close()
	return render_template('news/index.html', news=news, main_article=main_article)

@bp.route('/wirtschaft')
def wirtschaft():

	db_connection = get_db()
	db_cursor = db_connection.cursor()

	main_article = db_cursor.execute("""SELECT * FROM Links LIMIT 1""").fetchall()
	news = db_cursor.execute("""SELECT LINK, Source_ID, HEADLINE, TEASER, IMG_LINK, DateandTime FROM Links WHERE Topic_ID=3 ORDER BY DateandTime DESC LIMIT 1, 5000;""").fetchall()
	db_cursor.close()
	return render_template('news/index.html', news=news, main_article=main_article)

@bp.route('/gesellschaft')
def gesellschaft():

	db_connection = get_db()
	db_cursor = db_connection.cursor()

	main_article = db_cursor.execute("""SELECT * FROM Links LIMIT 1""").fetchall()
	news = db_cursor.execute("""SELECT LINK, Source_ID, HEADLINE, TEASER, IMG_LINK, DateandTime FROM Links WHERE Topic_ID=4 ORDER BY DateandTime DESC LIMIT 1, 5000;""").fetchall()
	db_cursor.close()
	return render_template('news/index.html', news=news, main_article=main_article)

@bp.route('/sport')
def sport():

	db_connection = get_db()
	db_cursor = db_connection.cursor()

	main_article = db_cursor.execute("""SELECT * FROM Links LIMIT 1""").fetchall()
	news = db_cursor.execute("""SELECT LINK, Source_ID, HEADLINE, TEASER, IMG_LINK, DateandTime FROM Links WHERE Topic_ID=5 ORDER BY DateandTime DESC LIMIT 1, 5000;""").fetchall()
	db_cursor.close()
	return render_template('news/index.html', news=news, main_article=main_article)


@bp.route('/technik')
def technik():

	db_connection = get_db()
	db_cursor = db_connection.cursor()

	main_article = db_cursor.execute("""SELECT * FROM Links LIMIT 1""").fetchall()
	news = db_cursor.execute("""SELECT LINK, Source_ID, HEADLINE, TEASER, IMG_LINK, DateandTime FROM Links WHERE Topic_ID=5 ORDER BY DateandTime DESC LIMIT 1, 5000;""").fetchall()
	db_cursor.close()
	return render_template('news/index.html', news=news, main_article=main_article)













