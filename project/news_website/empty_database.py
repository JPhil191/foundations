import sqlite3

db_connection = sqlite3.connect('/home/janphilipp_thiele/foundations/project/instance/news_articles.sqlite')
db_cursor = db_connection.cursor()
db_cursor.execute("DELETE FROM Links;")

db_connection.commit()