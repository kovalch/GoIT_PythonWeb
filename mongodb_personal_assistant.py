import argparse
import datetime
import sys
from functools import wraps

from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient("mongodb://localhost:27017")
db = client.test

parser = argparse.ArgumentParser(description='Personal Assistant APP')
parser.add_argument('--action', help='Command: create, update, find, remove')
parser.add_argument('--id')
parser.add_argument('--name')
parser.add_argument('--email')
parser.add_argument('--note')
parser.add_argument('--tags', nargs='+')
parser.add_argument('--date')

arguments = parser.parse_args()
my_arg = vars(arguments)

action = my_arg.get('action')
name = my_arg.get('name')
email = my_arg.get('email')
_id = my_arg.get('id')
note = my_arg.get('note')
date = my_arg.get('date')
tags = my_arg.get('tags')


class ExceptionValidation(Exception):
    pass


def validate(func):
    @wraps(func)
    def wrapper(*args):
        for el in args:
            if el is None:
                raise ExceptionValidation(f'Incoming data is not valid : {func.__name__}{args}')
        result = func(*args)
        return result

    return wrapper


def find_by_id(_id):
    result = db.address_book.find_one({"_id": ObjectId(_id)})
    return result


@validate
def create(name, email, note, tags):
    result = db.address_book.insert_one({
        "name": name,
        "email": email,
        "note": note,
        "tags": tags,
        "date": datetime.datetime.now()
    })
    return find_by_id(result.inserted_id)


@validate
def find():
    return db.address_book.find()


@validate
def update(_id, name, email, note, tags):
    r = db.address_book.update_one({"_id": ObjectId(_id)}, {
        "$set": {
            "name": name,
            "email": email,
            "note": note,
            "tags": tags
        }
    })
    print(r)
    return find_by_id(_id)


@validate
def remove(_id):
    r = db.address_book.delete_one({"_id": ObjectId(_id)})
    return r


def main():
    try:
        match action:
            case 'create':
                r = create(name, email, note, tags)
                print(r)
            case 'find':
                r = find()
                [print(el) for el in r]
            case 'update':
                r = update(_id, name, email, note, tags)
                print(r)
            case 'remove':
                r = remove(_id)
                print(r)
            case _:
                print('Unknowns command')
    except ExceptionValidation as err:
        print(err)


if __name__ == '__main__':
    main()
