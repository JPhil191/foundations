import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    
    db_connection = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
            )
    db_connection.row_factory = sqlite3.Row

    return db_connection

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db_connection.close()

