from ipproject.core.database import db


class MasterModel(db.Model):
    __tablename__ = 'masters'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    phone = db.Column(db.String(11), nullable=False)

    def jsonify(self):
        return {
            'id': self.id,
            'name': self.name,
            'phone': self.phone
        }
