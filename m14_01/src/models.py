from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey, Table

Base = declarative_base()
quote_m2m_tag = Table(
    "quote_m2m_tag",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("quote", Integer, ForeignKey("quotes.id")),
    Column("tag", Integer, ForeignKey("tags.id")),
)


class Author(Base):
    __tablename__ = "authors"
    id = Column(Integer, primary_key=True)
    name_author = Column(String(80), nullable=False, unique=True)
    href_author = Column(String(150), nullable=False, unique=True)


class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True)
    name_tag = Column(String(50), nullable=False, unique=True)


class Quote(Base):
    __tablename__ = "quotes"
    id = Column(Integer, primary_key=True)
    quote_phrase = Column(String(250), nullable=False, unique=True)
    tags = relationship("Tag", secondary=quote_m2m_tag, backref="quotes")
    author_id = Column(Integer, ForeignKey(Author.id, ondelete="CASCADE"))
