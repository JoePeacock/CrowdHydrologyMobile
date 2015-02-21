from flask import url_for
from sqlalchemy.orm import relationship
from app import db


class Station(db.Model):

    __tablename__ = 'stations'

    id = db.Column(db.Integer, primary_key=True)

    state = db.Column(db.String(80), unique=True)
    id_number = db.Column(db.Integer)

    name = db.Column(db.String(160), unique=True)
    long_name = db.Column(db.String(160))

    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

    online = db.Column(db.Boolean, default=True)

    # One to many to data points
    data_points = relationship("Data", backref='stations')

    def serialize(self):
        return {
            'name': self.long_name,
            'state': self.state,
            'id': self.name,
            'latitude': self.latitude,
            'longitgude': self.longitude,
            'online': self.online,
            'data_url': url_for("get_data", label_name=self.name, _external=True)
        }

    def serialize_data(self):
        return {
            'name': self.long_name,
            'state': self.state,
            'station_id': self.name,
            'latitude': self.latitude,
            'longitgude': self.longitude,
            'online': self.online,
            'data_points': [d.serialize() for d in self.data_points]
        }

    def __init__(self, **kwargs):
        self.__dict__.update(**kwargs)
