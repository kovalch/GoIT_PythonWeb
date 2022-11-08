from datetime import datetime

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey, Table, MetaData
from sqlalchemy.sql.sqltypes import DateTime

from src.db import Base, engine, db_session

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False)
    phone = Column(String(150), nullable=False, unique=True)
    created = Column(DateTime, default=datetime.now())
    infos = relationship("Info", backref="users")


class Info(Base):
    __tablename__ = "infos"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=True)
    surname = Column(String(50), nullable=True)
    email = Column(String(125), nullable=True, unique=True)
    birthday = Column(String(25), nullable=True)
    address = Column(String(25), nullable=True)
    info_id = Column("info_id", ForeignKey("users.id", ondelete="CASCADE"))

    def __repr_(self):
        return f'Info: {self.id}, {self.name}, {self.surname}, {self.email}, ' \
               f'{self.birthday}, {self.address}'


if __name__ == "__main__":
    Base.metadata.create_all(engine)