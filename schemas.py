from marshmallow import Schema, fields
from models import *


class ShowSchema(Schema):
    class Meta:
        model = Show
        include_relationships = True
        load_instance = True
        include_fk = True

    artist_id = fields.Integer()
    artist_name = fields.Function(lambda obj: obj.artist.name)
    artist_image_link = fields.Function(lambda obj: obj.artist.image_link)
    start_time = fields.Str()


class VenueSchema(Schema):
    class Meta:
        model = Venue
        include_relationships = True
        load_instance = True
        include_fk = True

    id = fields.Integer()
    name = fields.Str()
    city = fields.Str()
    state = fields.Function(lambda obj: obj.state.name)
    address = fields.Str()
    phone = fields.Str()
    image_link = fields.Str()
    website = fields.Str()
    seeking_talent = fields.Str()
    seeking_description = fields.Str()
    facebook_link = fields.Str()
    genres = fields.Pluck('self', 'name', many=True)
    past_shows = fields.List(fields.Nested(ShowSchema()))
    upcoming_shows = fields.List(fields.Nested(ShowSchema()))
    past_shows_count = fields.Function(lambda obj: len(obj.past_shows))
    upcoming_shows_count = fields.Function(lambda obj: len(obj.upcoming_shows))


