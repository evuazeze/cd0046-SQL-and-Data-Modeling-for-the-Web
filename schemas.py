from marshmallow import Schema, fields, pre_dump
from models import *


class ArtistShowSchema(Schema):
    class Meta:
        model = Show
        include_relationships = True
        load_instance = True
        include_fk = True

    artist_id = fields.Integer()
    artist_name = fields.Function(lambda obj: obj.artist.name)
    artist_image_link = fields.Function(lambda obj: obj.artist.image_link)
    start_time = fields.Str()


class VenueShowSchema(Schema):
    class Meta:
        model = Show
        include_relationships = True
        load_instance = True
        include_fk = True

    venue_id = fields.Integer()
    venue_name = fields.Function(lambda obj: obj.venue.name)
    venue_image_link = fields.Function(lambda obj: obj.venue.image_link)
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
    past_shows = fields.List(fields.Nested(ArtistShowSchema()))
    upcoming_shows = fields.List(fields.Nested(ArtistShowSchema()))
    past_shows_count = fields.Function(lambda obj: len(obj.past_shows))
    upcoming_shows_count = fields.Function(lambda obj: len(obj.upcoming_shows))


class ArtistSchema(Schema):
    class Meta:
        model = Artist
        include_relationships = True
        load_instance = True
        include_fk = True

    id = fields.Integer()
    name = fields.Str()
    city = fields.Str()
    state = fields.Function(lambda obj: obj.state.name)
    phone = fields.Str()
    image_link = fields.Str()
    website = fields.Str()
    seeking_venue = fields.Str()
    seeking_description = fields.Str()
    facebook_link = fields.Str()
    genres = fields.Pluck('self', 'name', many=True)
    past_shows = fields.List(fields.Nested(VenueShowSchema()))
    upcoming_shows = fields.List(fields.Nested(VenueShowSchema()))
    past_shows_count = fields.Function(lambda obj: len(obj.past_shows))
    upcoming_shows_count = fields.Function(lambda obj: len(obj.upcoming_shows))


class VenueThumbnailSchema(Schema):
    class Meta:
        model = Venue
        include_relationships = True
        load_instance = True
        include_fk = True

    id = fields.Integer()
    name = fields.Str()
    num_upcoming_shows = fields.Function(lambda obj: len(obj.upcoming_shows))


def venue_grouper_partition(items, city, state, container_name):
    return [
        {
            city: grouper[0],
            state: grouper[1],
            container_name: [item for item in items if item.city == grouper[0] and item.state == grouper[1]],
        }
        for grouper in set((item.city, item.state) for item in items)
    ]


class VenueGrouperSchema(Schema):
    class Meta:
        model = Venue
        include_relationships = True
        load_instance = True
        include_fk = True

    city = fields.Str()
    state = fields.Function(lambda obj: obj['state'].name)
    venues = fields.List(fields.Nested(VenueThumbnailSchema()))

    @pre_dump(pass_many=True)
    def partition_venues(self, data, many):
        return venue_grouper_partition(data, 'city', 'state', 'venues')


def venue_search_partition(items, count, container_name):
    return {
        count: len(container_name),
        container_name: [item for item in items],
    }


class VenueSearchSchema(Schema):
    class Meta:
        model = Venue
        include_relationships = True
        load_instance = True
        include_fk = True

    count = fields.Function(lambda obj: len(obj['data']))
    data = fields.List(fields.Nested(VenueThumbnailSchema()))

    @pre_dump(pass_many=False)
    def partition_venues(self, data, many):
        return venue_search_partition(data, 'count', 'data')