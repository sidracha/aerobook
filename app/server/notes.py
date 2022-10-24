from uuid import uuid4
from flask import jsonify
from sqlalchemy import desc	

from models import Note
from models import db
import notebooks



def create_new_note(user_id, notebook_id, body):

	#need to check if notebook exists
	if notebooks.check_if_notebook_exists(notebook_id) == False:
		return

	note_id = str(uuid4())
	new_note = Note(note_id=note_id, user_id=user_id, notebook_id=notebook_id, body=body)
	db.session.add(new_note)
	db.session.commit()
	return {"note_id": new_note.note_id, "body": new_note.body}

def delete_note(note_id, notebook_id):
	Note.query.filter_by(note_id=note_id, notebook_id=notebook_id).delete()
	db.session.commit()

def get_notes(notebook_id, limit, offset):
	notes = Note.query.filter_by(notebook_id=notebook_id).order_by(desc(Note.created)).limit(limit).offset(offset)
	notes_arr = []
	for note in notes:
		obj = {"note_id": note.note_id, "body": note.body}
		notes_arr.append(obj)
	
	return notes_arr

def get_note_count(notebook_id):
	count = 0
	notes = Note.query.filter_by(notebook_id=notebook_id).all()
	for note in notes:
		count +=1
	
	return count

def delete_all_notes(notebook_id):
	Note.query.filter_by(notebook_id=notebook_id).delete()
	db.session.commit()