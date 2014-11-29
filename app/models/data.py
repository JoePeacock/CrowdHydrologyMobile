from sqlalchemy_utils import ArrowType
import arrow

from app import db


class Data(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    station_id = db.Column(db.Integer, db.ForeignKey('stations.id'))

    water_level = db.Column(db.Float)
    water_clarity = db.Column(db.Integer)
    image = db.Column(db.String)

    created_at = db.Column(ArrowType, default=arrow.now)

    def serialize(self):
        return {
            'water_level': self.water_level,
            'water_clarity': self.water_clarity,
            'image': self.image,
            'created_at': self.created_at.timestamp
        }

    def __init__(self, **kwargs):
        self.__dict__.update(**kwargs)
