from datetime import datetime
from unicodedata import name

from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.sql.schema import ForeignKey, Table
from sqlalchemy.orm import relationship

Base = declarative_base()


quote_tag = Table(
    "quote_tag",
    Base.metadata,
    # Column("id", Integer, primary_key=True),
    Column("quote", Integer, ForeignKey("quotes.id")),
    Column("tag", Integer, ForeignKey("tags.id")),
)

class Author(Base):
    __tablename__ = "authors"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    quotes = relationship("Quote", cascade="all, delete", backref="author")


class Quote(Base):
    __tablename__ = "quotes"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(10000), nullable=False)
    author_id = Column(Integer, ForeignKey(Author.id, ondelete="CASCADE"))
    tags = relationship("Tag", secondary=quote_tag, backref="quotes")


class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(25), nullable=False)

