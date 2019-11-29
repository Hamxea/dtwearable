from db import db


class AbstractDAO:

    def save_to_db(self, model):
        db.session.add(model)
        db.session.commit()

    def delete_from_db(self, model):
        db.session.delete(model)
        db.session.commit()