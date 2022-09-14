from sqlalchemy.orm import joinedload
from sqlalchemy import and_
from datetime import datetime
from src.db import session
from src.model import AdressBook, NoteBook
from faker import Faker
fake = Faker()


def get_contacts():
        contacts = session.query(AdressBook).options(joinedload('notes')).all()
        for c in contacts:
            print(vars(c))
            print(f"{[f'id: {n.id} note: {n.note}' for n in c.notes]} \n ")


if __name__ == '__main__':
    get_contacts()