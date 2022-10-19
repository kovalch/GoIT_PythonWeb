from src.models import Contact, Note, db
import datetime
from bson.objectid import ObjectId
from bson.errors import InvalidId
from mongoengine import *
# jo = Contact(email='ex@example.com', first_name='Jo', last_name='Lawley', age=20).save()
# note1 = Note(title='Fun with MongoEngine', author=jo)
# note1.note = 'Took a look at MongoEngine today, looks pretty cool.'
# note1.tags = ['mongodb', 'mongoengine']
# note1.save()


def create(*args):
    result = Contact(
	    first_name = input('First name:  '),
	    last_name = input('Last name:  '),
	    age = input('Your age:  '),
	    email=input('Email: '),
	    date= datetime.datetime.now()
    ).save()

    return result

def find_by_id(*args):
	id = input('id of the record:  ')
	collection = db.personal_helper.contact
	try:
		result = collection.find({"_id": ObjectId(id)})
		for doc in result:
			print(doc)
	except InvalidId:
		print(f"No record were found with id: {id}")

def remove_by_id(*args):
	id = input('id of the record:  ')
	collection = db.personal_helper.contact
	try:
		r = collection.delete_one({"_id": ObjectId(id)})
		print(f"The record with id: {id} was deleted")
		return r
	except InvalidId:
		print(f"There is no record with id: {id}")


"""Methods for NoteBook"""
def create_note(*args):
    result = Note(
	    title = input('Note title:  '),
	    note = input('Your note:  '),
	    tags = input('Tags:  '),
	    date= datetime.datetime.now()
    ).save()

    return result

def find_note_by_id(*args):
	id = input('id of the record:  ')
	collection = db.personal_helper.note
	try:
		result = collection.find({"_id": ObjectId(id)})
		for doc in result:
			print(doc)
	except InvalidId:
		print(f"No record were found with id: {id}")

def remove_note_by_id(*args):
	id = input('id of the record:  ')
	collection = db.personal_helper.note
	try:
		r = collection.delete_one({"_id": ObjectId(id)})
		print(f"The record with id: {id} was deleted")
		return r
	except InvalidId:
		print(f"There is no record with id: {id}")


