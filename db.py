from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine

"""
SqlAlchemy örneğini oluşturan ve tüm DAO sınıflarının kullandığı sınıf
"""
db = SQLAlchemy()
engine = create_engine('postgresql://arge05:arge05@10.0.0.59:5432/keymind')

