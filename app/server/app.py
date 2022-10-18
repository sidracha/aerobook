from flask import Flask, redirect, render_template, url_for, session, request, Blueprint, jsonify, abort, json
import json
from authlib.integrations.flask_client import OAuth
import os
from datetime import timedelta
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from functools import wraps

app = Flask(__name__,
					template_folder="../frontend/templates",
					static_folder="../frontend/static")
CORS(app)

app.secret_key = os.getenv("APP_SECRET_KEY")
app.config['SESSION_COOKIE_NAME'] = 'google-login-session'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=31)

print(os.getenv("SQLALCHEMY_DATABASE_URI"))
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("SQLALCHEMY_DATABASE_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

from models import db

db.init_app(app)
with app.app_context():
	db.create_all()

# oAuth Setup

def login_required(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if "profile" in session:
			print("Logged In")
			return f(*args, **kwargs)
		else:
			#flash("You need to login first")
			print("you need to login first")
			return redirect("/")

	return wrap


import notebooks
import notes

@app.route("/")
def handle_home():
	return render_template("home.html")

@app.route("/display/notebooks")
@login_required
def handle_display():
	email = session["profile"]["email"]
	return render_template("books.html")


@app.route("/notebook/<name>", methods=["POST"])
@login_required
def handle_notebook_post(name):
	user_id = session["profile"]["user_id"]
	max_notebooks = 1000
	#max_notebooks = int(os.getenv("MAX_NOTEBOOKS"))

	notebook_obj = notebooks.create_new_notebook(user_id, name, max_notebooks)
	if bool(notebook_obj) == False:
		return abort(500, description="Notebook Limit Exceeded")

	return notebook_obj


@app.route("/notebooks", methods=["GET"])
@login_required
def handle_notebooks_get():
	user_id = session["profile"]["user_id"]
	notebooks_arr = notebooks.get_all_notebooks(user_id)

	return jsonify({"notebooks": notebooks_arr})

@app.route("/notebook/<notebook_id>", methods=["DELETE"])
@login_required
def handle_notebook_delete(notebook_id):
	notebooks.delete_notebook(notebook_id)
	return "deleted notebook"


@app.route("/notebook/<notebook_id>/note", methods=["POST"])
@login_required
def handle_note_post(notebook_id):
	user_id = session["profile"]["user_id"]
	body = request.json
	body = body["body"]
	return notes.create_new_note(user_id, notebook_id, body)

@app.route("/notebook/<notebook_id>/notes", methods=["GET"])
@login_required
def handle_notes_get(notebook_id):
	return notes.get_all_notes(notebook_id)

@app.route("/notebook/<notebook_id>/note/<note_id>", methods=["DELETE"])
@login_required
def handle_note_delete(notebook_id, note_id):
	notes.delete_note(note_id, notebook_id)
	return "deleted note"


@app.route("/display/<notebook_id>")
@login_required
<<<<<<< HEAD
def handle_display_nbid(notebook_id):

	#check if notebook exists otherwise redirect
	if notebooks.check_if_notebook_exists(notebook_id) == False:
		return redirect("/display/notfound")
	return render_template("notebook.html")

@app.route("/display/notfound")
def handle_notfound():
	return render_template("notfound.html")

@app.route("/notebook/<notebook_id>/count")
@login_required
def handle_count_notes(notebook_id):
	count = notes.get_note_count(notebook_id)
	return jsonify({"count": count})
=======
def handle_display_nbid():
	return render_template("notebook.html")


>>>>>>> parent of 72a3d1f (notebook page)




@app.route("/session")
@login_required
def handle_session():
	return session["profile"]


@app.route("/test")
@login_required
def handle_test():
	count = notebooks.get_notebooks_count(session["profile"]["user_id"])
	return jsonify({"count": count})


# google login stuff
oauth = OAuth(app)
google = oauth.register(
	name='google',
	client_id=os.getenv("GOOGLE_CLIENT_ID"),
	client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
	access_token_url='https://accounts.google.com/o/oauth2/token',
	access_token_params=None,
	authorize_url='https://accounts.google.com/o/oauth2/auth',
	authorize_params=None,
	api_base_url='https://www.googleapis.com/oauth2/v1/',
	userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',  # This is only needed if using openId to fetch user info
	client_kwargs={'scope': 'openid email profile'},
	jwks_uri='https://www.googleapis.com/oauth2/v3/certs'
)

@app.route('/google-login')
def login_google():
	google = oauth.create_client('google')  # create the google oauth client
	redirect_uri = url_for('authorize', _external=True)
	return google.authorize_redirect(redirect_uri)


@app.route('/logout')
def logout():
	for key in list(session.keys()):
		session.pop(key)
	return redirect('/')


@app.route('/authorize')
def authorize():
	google = oauth.create_client('google')  # create the google oauth client
	token = google.authorize_access_token()  # Access token from google (needed to get user info)
	resp = google.get('userinfo')  # userinfo contains stuff u specificed in the scrope
	user_info = resp.json()
	user = oauth.google.userinfo()  # uses openid endpoint to fetch user info
	# Here you use the profile/user data that you got and query your database find/register the user
	# and set ur own data in the session not the profile from google

	session['profile'] = user_info
	session.permanent = True  # make the session permanant so it keeps existing after broweser gets closed

	import users
	user = users.create_user(user_info["email"])
	session["profile"]["user_id"] = user.user_id

	return redirect('/display/notebooks')


if __name__ == "__main":
	app.run()