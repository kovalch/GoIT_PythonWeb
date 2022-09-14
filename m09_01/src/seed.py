"""Adding data"""
import random
from faker import Faker
from db import session
from model import AdressBook, NoteBook, ContactNote

fake = Faker()


def create_contacts():
    for _ in range(1, 6):
        contact = AdressBook(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            email=fake.ascii_free_email(),
            cell_phone=fake.phone_number(),
            address=fake.address(),
            creation_date=fake.date_between(start_date='-10y')
        )
        session.add(contact)
    session.commit()


def create_notes():
    for _ in range(10):
        note = NoteBook(
            note=fake.text(),
            tag=fake.words(1)
        )
        session.add(note)
    session.commit()


def create_relationship():
    notes = session.query(NoteBook).all()
    contacts = session.query(AdressBook).all()

    for note in notes:
        contact = random.choice(contacts)
        rel = ContactNote(contact_id=contact.id, note_id=note.id, contact_tag='connector')
        session.add(rel)
    session.commit()


if __name__ == '__main__':
    #create_contacts()
    #create_notes()
    create_relationship()
