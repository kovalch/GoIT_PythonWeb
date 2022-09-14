from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship

from src.db import Base

class AdressBook(Base):
	__tablename__ = "contacts"
	id = Column(Integer, primary_key=True)
	first_name = Column(String(120), nullable=False)
	last_name = Column(String(120), nullable=False)
	email = Column('email', String(100), nullable=False)
	cell_phone = Column('cell_phone', String(100), nullable=False)
	address = Column('address', String(100), nullable=True)
	creation_date = Column('creation_date', Date, nullable=True)
	notes = relationship('NoteBook', secondary='contacts_to_notes', back_populates='contacts')


class NoteBook(Base):
	__tablename__ = "notes"
	id = Column(Integer, primary_key=True)
	note = Column('note', String(340), nullable=False)
	tag = Column('tag', String(100), nullable=True)
	contacts = relationship('AdressBook', secondary='contacts_to_notes', back_populates='notes')


class ContactNote(Base):
	__tablename__ = 'contacts_to_notes'
	id = Column(Integer, primary_key=True)
	contact_tag = Column('contact_tag', String(100))
	contact_id = Column('contact_id', ForeignKey('contacts.id', ondelete='CASCADE'))
	note_id = Column('note_id', ForeignKey('notes.id', ondelete='CASCADE'))
