import sqlite3

#with sqlite3.connect('/home/janphilipp_thiele/foundations/project/instance/news_articles.sqlite') as db_connection:
def empty_db():
	with sqlite3.connect('/Users/jan-philippthiele/FoundationsFolder/foundations/project/instance/news_articles.sqlite') as db_connection:
		db_cursor = db_connection.cursor()
		db_cursor.execute("DELETE FROM Links;")

		db_connection.commit()