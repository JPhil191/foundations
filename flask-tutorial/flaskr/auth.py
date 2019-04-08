import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

#aassociates the URL /register with the register view function. When flask recieves a request to /auth/register,
#it will call the register view and use the return value as the response 
#If the user submitted the form, request.method will be POST. In this case, start validating the input
@bp.route('/register', methods=('GET', 'POST'))
def register():
	if request.method == 'POST':
					#request.form is a special type of dict mapping submitted form keys and values. 
					#The user will input their username and password
		username = request.form['username']
		password = request.form['password']
		db = get_db()
		error = None

		if not username:
			error = 'Username is required.'
		elif not password:
			error = 'Password is required.'
		elif db.execute(
			#checking if username is already taken by making a database query
			'SELECT id FROM user WHERE username = ?', (username,)
			#fetchone() returns one row from the query. If the query returned no results, it returns None. LAter fetchall() is used which returns all resuts.
		).fetchone() is not None:
			error = 'User {} is already registered.'.format(username)

			#User name is fine and will be stored in the database with the password which we will hash first.
		if error is None:
			db.execute(
				'INSERT INTO user (username, password) VALUES (?, ?)',
				(username, generate_password_hash(password))
			)
			#db.commit() is being called to save the changes we have made to database
			db.commit()
			#After we have stored the users information inside the database they are redirected to the log in page. url_for() generates the URL
			#for the log in view based in its name. This is preferable to writing the URL directly as it allows you to change the URL
			#later without changing all the code that links to it. redirect() generates a redirect response to the generated URL
			return redirect(url_for('auth.login'))
		#If validation fails, the error is shown to the user. flash() stores messages that can be retrieved when rendering the template.
		flash(error)
		#When the user initially navigates to auth/register, or there was an validation errir, an HTML page with the registration form should be shown.
		#render_template will render a template containing the HTML.
	return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		db = get_db()
		error = None
		#User is stored inside a variable for later use
		user = db.execute(
			'SELECT * FROM user WHERE username = ?', (username,)
		).fetchone()

		if user is None:
			error = 'Incorrect username.'
				#check password hash hashes the submitted password in the same way as the stored has and securely
				#compares them. If they match the password is valid.
		elif not check_password_hash(user['password'], password):
			error = 'Incorrect password.'

		if error is None:
			#session is a dict that stores data across requests. When validation succeds the users id is stored in a new session.
			#The data is stored in a cookie that is sent to the browser, and the browser then send is back with
			# subsequent requests. Flask securly sugns the data so that it can not be tempered with
			session.clear()
			session['user_id'] = user['id']
			return redirect(url_for('index'))

		flash(error)

	return render_template('auth/login.html')
	#Now that the user's id s stored in the session it will be available on subsequent requests. At the beginning of each request
	#if the user is logged in, their information shoul be loaded and made available to other views.



#@bp.before_app_requests registers a function that runs before the view function, no matter wht URL is requested.
@bp.before_app_request
#load_logged_in_user() checks if a user id is stored in the session and hets that user's data from the database
#storing it on the g.user, which lasts for the length of the request. If there is no user id, or if the user does not exist g.user will be None
def load_logged_in_user():
	user_id = session.get('user_id')

	if user_id is None:
		g.user = None
	else:
		g.user = get_db().execute(
			'SELECT * FROM user WHERE id = ?', (user_id,)
		).fetchone()


#To log out you need to remove the user id from the session. Then load_logged_in_user won't load a user on supsequent requests.
@bp.route('/logout')
def logout():
	session.clear()
	return redirect(url_for('index'))




#This decorator returns a new view function that wraps the original view it's applied to. The name function checks if a user is loaded and redirects to the login page otherwise.
#If a user is loaded the original views are cancelled and continues normally. You'll use this decorator when writing the blog views.
def login_required(view):
	@functools.wraps(view)
	def wrapped_view(**kwargs):
		if g.user is None:
			return redirect(url_for('auth.login'))

		return view(**kwargs)

	return wrapped_view

"""The url_for() function generates the URL to a view based on a name and arguments. The name associated with a view is also called the endpoint,
and by default it’s the same as the name of the view function. For example, the hello() view that was added to the app factory earlier in the tutorial
has the name 'hello' and can be linked to with url_for('hello'). If it took an argument, which you’ll see later, it would be linked to using url_for('hello', who='World').
When using a blueprint, the name of the blueprint is prepended to the name of the function, so the endpoint for the login function you wrote above
is 'auth.login' because you added it to the 'auth' blueprint."""














































