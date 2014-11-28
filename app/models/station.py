from sqlalchemy.orm import relationship
from app import db


class Station(db.Model):

    __tablename__ = 'stations'

    id = db.Column(db.Integer, primary_key=True)

    state = db.Column(db.String(80), unique=True)
    identification_number = db.Column(db.Integer)
    name = db.Column(db.String(160), unique=True)

    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

    online = db.Column(db.Boolean)

    # One to many to data points
    data_points = relationship("Data", backref='stations', lazy="joined")

    def __init__(self, **kwargs):
        self.__dict__.update(**kwargs)
