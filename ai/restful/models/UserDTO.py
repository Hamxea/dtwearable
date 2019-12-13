from db import db

class UserDTO(db.Model):
    """
    User tablosu için veritabı eşleştirmelerinin yapıldığı model sınıfı
    """

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))
    role = db.Column(db.Integer)

    def __init__(self, username:str, password:str, role:int):
        self.username = username
        self.password = password
        self.role = role

    def json(self):
        """ Nesneyi json'a çeviren metod """

        return {
            'id': self.id,
            'username': self.username,
            'role': self.role
        }