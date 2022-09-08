from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database, drop_database

import os

# load the .env file into the environment
from dotenv import load_dotenv

load_dotenv()

# loads the password from the environment variable
DB_PASSWORD = os.environ['POSTGRES_PASSWORD']
DB_USER = os.environ['POSTGRES_USER']
engine = create_engine(f'postgresql://{DB_USER}:{DB_PASSWORD}@localhost:5432/stonks')

if not database_exists(engine.url):
    create_database(engine.url)

Session = sessionmaker(bind=engine)
Base = declarative_base()
