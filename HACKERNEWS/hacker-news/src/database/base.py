import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker


engine = create_engine("postgresql+psycopg2://rockship:@localhost:5432/hackernews", echo="debug")
Session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base(bind=engine)
