import os

from flask import Flask

def create_app(test_config = None):
    #create and configure app
    #creates the Flask instance, __name__ is the name of the current python module. The app needs to know where it's located to set up
    #some paths, and __name__ is a convinient way to tell it that.
    #                   tells the app that cconfiguration files are relative to the instance folder.
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'news_articles.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)app = create_app()
    except OSError:
        pass

    app.add_url_rule('/', endpoint='index')


    from . import news
    app.register_blueprint(news.bp)

    return app

