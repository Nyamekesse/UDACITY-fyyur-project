from flask_sqlalchemy import SQLAlchemy
import datetime
from sqlalchemy.dialects.postgresql import ARRAY
from flask_migrate import Migrate
from flask import Flask
from enum import unique
app = Flask(__name__)
db = SQLAlchemy()
migrate = Migrate(app, db)
#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#


class Venue(db.Model):
    __tablename__ = 'venues'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False, unique=True)
    genres = db.Column(ARRAY(db.String()), nullable=False, default=[])
    image_link = db.Column(db.String(500), nullable=False)
    facebook_link = db.Column(db.String(120), nullable=True)
    website = db.Column(db.String(200), nullable=True)
    seeking_talent = db.Column(db.Boolean, nullable=True, default=False)
    seeking_description = db.Column(db.String(300), nullable=True)
    shows = db.relationship('Show', backref='venues',
                            lazy='joined', cascade='all, delete')

    def __repr__(self):
        return f'<Venue ID: {self.id}, Venue name: {self.name}>'


class Artist(db.Model):
    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False, unique=True)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False, unique=True)
    genres = db.Column(ARRAY(db.String()), default=[], nullable=False)
    image_link = db.Column(db.String(500), nullable=False)
    website = db.Column(db.String(200), nullable=True)
    facebook_link = db.Column(db.String(120), nullable=True)
    seeking_venue = db.Column(db.Boolean, nullable=True, default=False)
    seeking_description = db.Column(db.String(300), nullable=True)
    shows = db.relationship('Show', backref='artists',
                            lazy='joined', cascade='all, delete')

    def __repr__(self):
        return f'<Artist ID: {self.id}, Artist name: {self.name}>'


class Show(db.Model):
    __tablename__ = 'shows'
    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey(
        'artists.id'), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey(
        'venues.id'), nullable=False)
    start_time = db.Column(
        db.DateTime, default=datetime.datetime.now, nullable=False)

    def __repr__(self):
        return f'<Artist ID: {self.artist_id}, Venue ID: {self.venue_id} ,Start Time: {self.start_time}>'
