from ..database import db
from enum import Enum


class PurchaseStatus(Enum):
    NEW = 'NEW'
    IN_PROGRESS = 'IN_PROGRESS'
    CANCELLED = 'CANCELLED'
    DONE = 'DONE'


class WorkModel(db.Model):
    __tablename__ = 'models'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    date = db.Column(db.DateTime(timezone=True), nullable=False)
    master_id = db.Column(
        db.Integer, db.ForeignKey('masters.id'), nullable=True
    )
    service_id = db.Column(
        db.Integer, db.ForeignKey('services.id'), nullable=True
    )
    status = db.Column(
        db.Enum(PurchaseStatus), nullable=False, default=PurchaseStatus.NEW
    )

    def jsonify(self):
        from ..utils import convert_to_utc
        return {
            'id': self.id,
            'user_id': self.user_id,
            'date': convert_to_utc(self.date).isoformat(),
            'master_id': self.master_id,
            'service_id': self.service_id,
            'status': self.status.name.lower(),

        }
