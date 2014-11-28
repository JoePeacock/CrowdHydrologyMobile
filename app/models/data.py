from app import db
from datetime import datetime


class Data(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    # Establish relationship to station
    station_id = db.Column(db.Integer, db.ForeignKey('stations.id'))

    # TODO: Talk to chris about whether this should be an int or float.
    water_level = db.Column(db.Float)
    water_clarity = db.Column(db.Integer)
    image = db.Column(db.String)

    created_at = db.Column(db.DateTime, default=datetime.now())

    def __init__(self, **kwargs):
        self.__dict__.update(**kwargs)
