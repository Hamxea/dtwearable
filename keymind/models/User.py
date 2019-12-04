from db import db

"""
User tablosu için veritabı eşleştirmelerinin yapıldığı model sınıfı
"""
class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))
    role = db.Column(db.String(80))

    def __init__(self, username:str, password:str, role:int):
        self.username = username
        self.password = password
        self.role = role

    # Nesneyi json'a çeviren metod
    def json(self):
        return {
            'id': self.id,
            'username': self.username,
            'role': self.role
        }