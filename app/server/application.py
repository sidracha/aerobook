from email.mime import application
from flask import Flask, redirect, render_template, url_for, session, request, Blueprint, jsonify, abort, json
import json
from authlib.integrations.flask_client import OAuth
import os
from datetime import timedelta
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from functools import wraps

SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
APP_SECRET_KEY = os.getenv("APP_SECRET_KEY")
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")

application = Flask(__name__,
					template_folder="../frontend/templates",
					static_folder="../frontend/static")
CORS(application)

application.secret_key = APP_SECRET_KEY
application.config['SESSION_COOKIE_NAME'] = 'google-login-session'
application.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=31)

application.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

from models import db

db.init_app(application)
with application.app_context():
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


@application.route("/")
def handle_home():
	if "profile" in session:
		return redirect("/display/notebooks")
	return render_template("home.html")

@application.route("/display/notebooks")
@login_required
def handle_display():
	email = session["profile"]["email"]
	return render_template("books.html")

@application.route("/user")
@login_required
def handle_user():
	return jsonify({"email": session["profile"]["email"], "profile_pic": session["profile"]["picture"]})


@application.route("/notebook/<name>", methods=["POST"])
@login_required
def handle_notebook_post(name):
	user_id = session["profile"]["user_id"]
	max_notebooks = 10
	
	notebook_obj = notebooks.create_new_notebook(user_id, name, max_notebooks)
	if bool(notebook_obj) == False:
		return abort(500, description="Notebook Limit Exceeded")

	return jsonify(notebook_obj)


@application.route("/notebooks", methods=["GET"])
@login_required
def handle_notebooks_get():
	user_id = session["profile"]["user_id"]
	notebooks_arr = notebooks.get_all_notebooks(user_id)

	return jsonify({"notebooks": notebooks_arr})

@application.route("/notebook/<notebook_id>", methods=["DELETE"])
@login_required
def handle_notebook_delete(notebook_id):
	notebooks.delete_notebook(notebook_id)
	return "deleted notebook"


@application.route("/notebook/<notebook_id>/note", methods=["POST"])
@login_required
def handle_note_post(notebook_id):
	print("here!!!!!!!!")
	user_id = session["profile"]["user_id"]
	body = request.get_json(force=True)
	body = body["body"]
	note_obj = notes.create_new_note(user_id, notebook_id, body)
	count = notes.get_note_count(notebook_id)
	return jsonify({"note": note_obj, "count": count})


@application.route("/notebook/<notebook_id>/notes", methods=["GET"])
@login_required
def handle_notes_get(notebook_id):
	args = request.args
	notes_arr = notes.get_notes(notebook_id, int(args["limit"]), int(args["offset"]))
	return jsonify({"notes": notes_arr})

@application.route("/notebook/<notebook_id>/note/<note_id>", methods=["DELETE"])
@login_required
def handle_note_delete(notebook_id, note_id):
	notes.delete_note(note_id, notebook_id)
	return "deleted note"


@application.route("/display/<notebook_id>")
@login_required
def handle_display_nbid(notebook_id):

	#check if notebook exists otherwise redirect
	if notebooks.check_if_notebook_exists(notebook_id) == False:
		return redirect("/display/notfound")
	return render_template("notebook.html")

@application.route("/display/notfound")
def handle_notfound():
	return render_template("notfound.html")

@application.route("/notebook/<notebook_id>/count")
@login_required
def handle_count_notes(notebook_id):
	count = notes.get_note_count(notebook_id)
	return jsonify({"count": count})

@application.route("/notebook/<notebook_id>/name")
@login_required
def handle_notebook_name(notebook_id):
	name = notebooks.get_name(notebook_id)
	print("name", name)
	return jsonify({"name": name})


@application.route("/session")
@login_required
def handle_session():
	return session["profile"]


@application.route("/test")
@login_required
def handle_test():
	count = notebooks.get_notebooks_count(session["profile"]["user_id"])
	return jsonify({"count": count})


# google login stuff
oauth = OAuth(application)
google = oauth.register(
	name='google',
	client_id=GOOGLE_CLIENT_ID,
	client_secret=GOOGLE_CLIENT_SECRET,
	access_token_url='https://accounts.google.com/o/oauth2/token',
	access_token_params=None,
	authorize_url='https://accounts.google.com/o/oauth2/auth',
	authorize_params=None,
	api_base_url='https://www.googleapis.com/oauth2/v1/',
	userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',  # This is only needed if using openId to fetch user info
	client_kwargs={'scope': 'openid email profile'},
	jwks_uri='https://www.googleapis.com/oauth2/v3/certs'
)

@application.route('/google-login')
def login_google():
	google = oauth.create_client('google')  # create the google oauth client
	redirect_uri = url_for('authorize', _external=True)
	return google.authorize_redirect(redirect_uri)


@application.route('/logout')
def logout():
	for key in list(session.keys()):
		session.pop(key)
	return redirect('/')


@application.route('/authorize')
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

