from uuid import uuid4
from flask import jsonify
from sqlalchemy import desc

from models import Notebook
from models import db

def get_notebooks_count(user_id):
	count = 0
	notebooks = Notebook.query.filter_by(user_id=user_id).all()
	for notebook in notebooks:
		print("here")
		count += 1
	
	return count


def create_new_notebook(user_id, name, max_notebooks):

	if get_notebooks_count(user_id) > max_notebooks:
		return False

	notebook_id = str(uuid4())

	new_notebook = Notebook(notebook_id=notebook_id, user_id=user_id, name=name)
	db.session.add(new_notebook)
	db.session.commit()
	return jsonify({"notebook_id": new_notebook.notebook_id, "name": new_notebook.name})

def get_all_notebooks(user_id):

	notebooks = Notebook.query.filter_by(user_id=user_id).order_by(Notebook.created).all()
	notebooks_arr = []
	for notebook in notebooks:
		obj = {"notebook_id": notebook.notebook_id, "name": notebook.name}
		notebooks_arr.append(obj)

	print(notebooks_arr)
	return notebooks_arr

def delete_notebook(notebook_id):

	Notebook.query.filter_by(notebook_id=notebook_id).delete()
	db.session.commit()