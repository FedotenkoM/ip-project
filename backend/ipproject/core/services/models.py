from ..database import db


class ServiceModel(db.Model):
    __tablename__ = 'services'

    id = db.Column(db.Integer, primary_key=True)
    service_name = db.Column(db.String(50), unique=True, nullable=False)
    price = db.Column(db.Integer, nullable=False)

    def jsonify(self):
        return {
            'id': self.id,
            'service_name': self.username,
            'price': self.price
        }
