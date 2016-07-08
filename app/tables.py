from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import (Table, Column, MetaData, ForeignKey, Index,
                        UniqueConstraint)
from sqlalchemy import Integer, String, Text

from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL

metadata = MetaData()


projects_table = Table(
    'projects', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name',String(256), unique=True),
    Column('email', String(256), unique=True),
    Column('description', String(256), unique=True),
    Column('dependencies', String(256), unique=True),
)