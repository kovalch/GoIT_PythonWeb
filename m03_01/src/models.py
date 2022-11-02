from mongoengine import *
from pymongo import MongoClient, errors

db=connect(host='mongodb://localhost:27017/personal_helper')
# client = MongoClient('mongodb://localhost:27017/personal_helper')
# dbname = client["personal_helper"]
# print(connect(host='mongodb://localhost:27017/personal_helper'))
class Contact(Document):
    first_name = StringField(max_length=120, min_length=1, required=True)
    last_name = StringField(max_length=120, min_length=1, required=False)
    age = IntField(min_value=18, max_value=75, required=True)
    email = EmailField(required=True)
    date = DateField(default=False)

class Note(Document):
    title = StringField(max_length=50, required=True)
    author = ReferenceField(Contact, reverse_delete_rule=CASCADE)
    note = StringField(required=False)
    # tags = ListField(StringField(max_length=30))
    tags = StringField(max_length=30)
    date = DateField(default=False)
    meta = {'allow_inheritance': True}