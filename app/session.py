from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from os import environ

engine = create_engine(environ['DATABASE_URI'])
Base = declarative_base()
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
Session.configure(bind=engine)
session = Session()
