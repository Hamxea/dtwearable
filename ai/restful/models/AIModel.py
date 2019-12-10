from db import db


class AIModel(db.Model):
    """
    AIModel tablosu için veritabı eşleştirmelerinin yapıldığı model sınıfı
    """

    __tablename__ = 'ai_model'

    id = db.Column(db.Integer, primary_key=True)
    class_name = db.Column(db.String(80), nullable=False)
    version = db.Column(db.Integer, nullable=False)
    model_url = db.Column(db.String(512), nullable=False)
    parameters = db.Column(db.String(4096), nullable=True)
    performance_metrics = db.Column(db.String(4096), nullable=True)
    enabled = db.Column(db.Boolean, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False)

    def __init__(self, id, class_name, version, model_url, parameters, performance_metrics, enabled, date_created):
        self.id = id
        self.class_name = class_name
        self.version = version
        self.model_url = model_url
        self.parameters = parameters
        self.performance_metrics = performance_metrics
        self.enabled = enabled
        self.date_created = date_created

    @property
    def serialize(self):
        """ Nesneyi json'a çeviren metod """

        return {
            'id': self.id,
            'class_name': self.class_name,
            'version': self.version,
            'model_url': self.model_url,
            'parameters': self.parameters,
            'performance_metrics': self.performance_metrics,
            'enabled = enabled': self.enabled,
            'date_created = date': self.date_created.strftime('%d.%m.%Y %H:%M:%S')
        }
