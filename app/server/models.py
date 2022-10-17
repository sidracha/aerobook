from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from datetime import date, datetime

db = SQLAlchemy()

class User(db.Model):

	__tablename__ = "Users"

	user_id = db.Column(db.String, primary_key=True)
	email = db.Column(db.String, unique=True, nullable=False)
	#password = db.Column(db.String, nullable=False)
	created = db.Column(db.DateTime(timezone=True), server_default=func.now())

class Notebook(db.Model):

	__tablename__ = "Notebooks"

	notebook_id = db.Column(db.String, primary_key=True)
	user_id = db.Column(db.String, nullable=False)
	name = db.Column(db.String, nullable=False)
	created = db.Column(db.DateTime(timezone=True), server_default=func.now())

class Note(db.Model):

	__tablename__ = "Notes"

	note_id = db.Column(db.String, primary_key=True)
	user_id = db.Column(db.String, nullable=False)
	notebook_id = db.Column(db.String, nullable=False)
	body = db.Column(db.String, nullable=False)
	created = db.Column(db.DateTime(timezone=True), server_default=func.now())


