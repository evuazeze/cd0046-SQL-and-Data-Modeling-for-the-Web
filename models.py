from flask import Flask
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class State(db.Model):
    __tablename__ = 'states'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)


venue_genres = db.Table('venue_genres',
                         db.Column('venue_id', db.Integer, db.ForeignKey('venues.id'), primary_key=True),
                         db.Column('genre_id', db.Integer, db.ForeignKey('genres.id'), primary_key=True)
                         )


class Venue(db.Model):
    __tablename__ = 'venues'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String)
    state_id = db.Column(db.Integer, db.ForeignKey('states.id'))
    address = db.Column(db.String)
    phone = db.Column(db.String)
    image_link = db.Column(db.String)
    website = db.Column(db.String)
    seeking_talent = db.Column(db.Boolean)
    seeking_description = db.Column(db.String)
    facebook_link = db.Column(db.String)
    state = db.relationship('State', backref='venues', lazy=True)
    past_shows = db.relationship('Show', primaryjoin=f"and_(Venue.id == Show.venue_id, cast(Show.start_time, Date) < func.current_date())", lazy=True)
    upcoming_shows = db.relationship('Show', primaryjoin=f"and_(Venue.id == Show.venue_id, cast(Show.start_time, Date) > func.current_date())", lazy=True)
    genres = db.relationship('Genre', secondary=venue_genres, backref='venues')


artist_genres = db.Table('artist_genres',
                         db.Column('artist_id', db.Integer, db.ForeignKey('artists.id'), primary_key=True),
                         db.Column('genre_id', db.Integer, db.ForeignKey('genres.id'), primary_key=True)
                         )


class Artist(db.Model):
    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String)
    state_id = db.Column(db.Integer, db.ForeignKey('states.id'))
    phone = db.Column(db.String)
    image_link = db.Column(db.String)
    facebook_link = db.Column(db.String)
    website = db.Column(db.String)
    seeking_venue = db.Column(db.Boolean)
    seeking_description = db.Column(db.Text)
    state = db.relationship('State', backref='artists', lazy=True)
    past_shows = db.relationship('Show',
                                 primaryjoin=f"and_(Artist.id == Show.artist_id, cast(Show.start_time, Date) < func.current_date())",
                                 lazy=True)
    upcoming_shows = db.relationship('Show',
                                     primaryjoin=f"and_(Artist.id == Show.artist_id, cast(Show.start_time, Date) > func.current_date())",
                                     lazy=True)
    genres = db.relationship('Genre', secondary=artist_genres, backref=db.backref('artists', lazy=True))


class Genre(db.Model):
    __tablename__ = 'genres'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f'<Genre id: {self.id}, name: {self.name} >'


class Show(db.Model):
    __tablename__ = 'shows'

    id = db.Column(db.Integer, primary_key=True)
    venue_id = db.Column(db.Integer, db.ForeignKey('venues.id'), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    artist = db.relationship("Artist", backref='shows', lazy=True)
    venue = db.relationship("Venue", backref='shows', lazy=True)
