from sqlalchemy import (Table, Column, MetaData)
from sqlalchemy import Integer, String

metadata = MetaData()

projects_table = Table(
    'projects', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(256), unique=True),
    Column('email', String(256), unique=True),
    Column('description', String(256), unique=True),
    Column('dependencies', String(256), unique=True)
)
