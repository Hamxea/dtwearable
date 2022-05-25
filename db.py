from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine

"""
The class that instantiates SqlAlchemy and is used by all DAO classes
"""
db = SQLAlchemy()
engine = create_engine('postgresql://postgres:postgres@localhost:5432/dt')

