from models import User
from uuid import uuid4
from models import db

def create_user(email):

	user = User.query.filter_by(email=email).first()

	if bool(user) == True:
		return user


	user_id = str(uuid4())
	new_user = User(user_id=user_id, email=email)
	db.session.add(new_user)
	db.session.commit()
	return new_user

def delete_user(email):
	user = User.query.filter_by(email=email).delete()
	db.session.commit()