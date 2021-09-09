from sqlalchemy import (
  Column,
  Integer,
  MetaData,
  String,
  Table,
  create_engine
)
import databases

DATABASE_URL = 'mysql://huidadao:$Billga2te$@localhost/fastapi'

engine = create_engine(DATABASE_URL)
metadata = MetaData()

Article = Table(
  'article',
  metadata,
  Column('id', Integer, primary_key = True),
  Column('title', String(100)),
  Column('description', String(100))
)

User = Table(
  'user',
  metadata,
  Column('id', Integer, primary_key = True),
  Column('username', String(20)),
  Column('password', String(128))
)

database = databases.Database(DATABASE_URL)