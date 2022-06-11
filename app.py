# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#

import sys

import dateutil.parser
import babel
from flask import render_template, request, flash, redirect, url_for, abort
import logging
from logging import Formatter, FileHandler

from forms import *
from schemas import *

engine = db.engine
# ----------------------------------------------------------------------------#
# Filters.
# ----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format, locale='en')


app.jinja_env.filters['datetime'] = format_datetime


# ----------------------------------------------------------------------------#
# Controllers.
# ----------------------------------------------------------------------------#

@app.route('/')
def index():
    return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
    distinct_venues = db.session.query(Venue).join(State, Venue.state_id == State.id).distinct(Venue.id, Venue.city, State.name).all()
    venue_grouper_schema = VenueGrouperSchema(many=True)
    return render_template('pages/venues.html', areas=venue_grouper_schema.dump(distinct_venues))


@app.route('/venues/search', methods=['POST'])
def search_venues():
    term = request.form.get('search_term', '')
    venues = Venue.query.filter(Venue.name.ilike(f'%{term}%')).all()
    search_schema = SearchSchema()
    response = search_schema.dump(venues)
    return render_template('pages/search_venues.html', results=response,
                           search_term=request.form.get('search_term', ''))


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    # shows the venue page with the given venue_id
    venue = db.session.query(Venue).join(Venue.genres).filter(Venue.id == venue_id).first()
    venue_schema = VenueSchema()
    return render_template('pages/show_venue.html', venue=venue_schema.dump(venue))


#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    # return render_template('forms/new_show.html', form=form)
    error = False
    data = {}
    try:
        name = request.form['name']
        city = request.form['city']
        state = State.query.filter_by(name=request.form['state']).first()
        address = request.form['address']
        phone = request.form['phone']
        image_link = request.form['image_link']
        facebook_link = request.form['facebook_link']
        website_link = request.form['website_link']
        seeking_talent = True if 'seeking_talent' in request.form else False
        seeking_description = request.form['seeking_description']

        venue = Venue(
            name=name,
            city=city,
            state_id=state.id,
            address=address,
            phone=phone,
            image_link=image_link,
            facebook_link=facebook_link,
            website=website_link,
            seeking_talent=seeking_talent,
            seeking_description=seeking_description
        )

        genres = request.form.getlist('genres')
        genres = [Genre.query.filter_by(name=genre).first() for genre in genres]
        venue.genres = genres
        db.session.add(venue)
        db.session.commit()

        data['id'] = venue.id
        data['name'] = venue.name
    except():
        db.session.rollback()
        error = True
        print(sys.exc_info())
    finally:
        db.session.close()

    if error:
        # on unsuccessful db insert, flash an error
        flash('An error occurred. Venue ' + data.name + ' could not be listed.')
        abort(500)
    else:
        # on successful db insert, flash success
        flash('Venue ' + request.form['name'] + ' was successfully listed!')

    return render_template('pages/home.html')


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    error = False
    try:
        venue = Venue.query.get(venue_id)
        db.session.delete(venue)
        db.session.commit()
    except():
        db.session.rollback()
        error = True
        print(sys.exc_info())
    finally:
        db.session.close()

    if error:
        # on unsuccessful db insert, flash an error
        flash('An error occurred. Venue could not be deleted.')
        abort(500)
    else:
        # on successful db insert, flash success
        flash('Venue was successfully deleted!')


#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
    data = Artist.query.with_entities(Artist.id, Artist.name).all()
    return render_template('pages/artists.html', artists=data)


@app.route('/artists/search', methods=['POST'])
def search_artists():
    term = request.form.get('search_term', '')
    artists = Artist.query.filter(Artist.name.ilike(f'%{term}%')).all()
    search_schema = SearchSchema()
    response = search_schema.dump(artists)
    return render_template('pages/search_artists.html', results=response,
                           search_term=request.form.get('search_term', ''))


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    # shows the artist page with the given artist_id
    artist = db.session.query(Artist).join(Artist.genres).filter(Artist.id == artist_id).first()
    artist_schema = ArtistSchema()
    return render_template('pages/show_artist.html', artist=artist_schema.dump(artist))


#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    error = False
    try:
        artist = Artist.query.get(artist_id)
        form = ArtistForm()

        form.name.data = artist.name
        form.city.data = artist.city
        form.state.data = artist.state.name
        form.state.choices = [(state.name, state.name) for state in State.query.all()]
        form.phone.data = artist.phone
        form.genres.data = [genre.name for genre in artist.genres]
        form.website_link.data = artist.website
        form.facebook_link.data = artist.facebook_link
        form.seeking_venue.data = artist.seeking_venue
        form.seeking_description.data = artist.seeking_description
        form.image_link.data = artist.image_link
    except():
        db.session.rollback()
        error = True
        print(sys.exc_info())
    finally:
        db.session.close()

    if error:
        flash('An error occurred. Data could not be fetched.')
        abort(500)

    return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    error = False
    data = {}
    artist = Artist.query.filter_by(id=artist_id).first()
    try:
        artist.name = request.form.get('name')
        artist.city = request.form.get('city')
        artist.state = State.query.filter_by(name=request.form.get('state')).first()
        artist.phone = request.form.get('phone')
        artist.genres = [Genre.query.filter_by(name=genre).first() for genre in request.form.getlist('genres')]
        artist.website = request.form.get('website_link')
        artist.facebook_link = request.form.get('facebook_link')
        artist.seeking_venue = True if 'seeking_venue' in request.form else False
        artist.seeking_description = request.form.get('seeking_description')
        artist.image_link = request.form.get('image_link')

        db.session.add(artist)
        db.session.commit()

        data['id'] = artist.id
        data['name'] = artist.name
    except():
        db.session.rollback()
        error = True
        print(sys.exc_info())
    finally:
        db.session.close()

    if error:
        flash('An error occurred. Artist could not be edited.')
        abort(500)
    else:
        flash('Artist was successfully edited!')

    return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    error = False
    try:
        venue = Venue.query.get(venue_id)
        form = VenueForm()

        form.name.data = venue.name
        form.city.data = venue.city
        form.state.data = venue.state.name
        form.address.data = venue.address
        form.state.choices = [(state.name, state.name) for state in State.query.all()]
        form.phone.data = venue.phone
        form.genres.data = [genre.name for genre in venue.genres]
        form.website_link.data = venue.website
        form.facebook_link.data = venue.facebook_link
        form.seeking_talent.data = venue.seeking_talent
        form.seeking_description.data = venue.seeking_description
        form.image_link.data = venue.image_link
    except():
        db.session.rollback()
        error = True
        print(sys.exc_info())
    finally:
        db.session.close()

    if error:
        flash('An error occurred. Data could not be fetched.')
        abort(500)

    return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    error = False
    data = {}
    try:
        venue = Venue.query.filter_by(id=venue_id).first()
        venue.name = request.form.get('name')
        venue.address = request.form.get('address')
        venue.city = request.form.get('city')
        venue.state = State.query.filter_by(name=request.form.get('state')).first()
        venue.phone = request.form.get('phone')
        venue.genres = [Genre.query.filter_by(name=genre).first() for genre in request.form.getlist('genres')]
        venue.website = request.form.get('website_link')
        venue.facebook_link = request.form.get('facebook_link')
        venue.seeking_talent = True if 'seeking_talent' in request.form else False
        venue.seeking_description = request.form.get('seeking_description')
        venue.image_link = request.form.get('image_link')

        db.session.add(venue)
        db.session.commit()

        data['id'] = venue.id
        data['name'] = venue.name
    except():
        db.session.rollback()
        error = True
        print(sys.exc_info())
    finally:
        db.session.close()

    if error:
        flash('An error occurred. Venue could not be edited.')
        abort(500)
    else:
        flash('Venue was successfully edited!')

    return redirect(url_for('show_venue', venue_id=venue_id))


#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    error = False
    data = {}

    try:
        name = request.form['name']
        city = request.form['city']
        state = State.query.filter_by(name=request.form['state']).first()
        phone = request.form['phone']
        image_link = request.form['image_link']
        facebook_link = request.form['facebook_link']
        website_link = request.form['website_link']
        seeking_venue = True if 'seeking_venue' in request.form else False
        seeking_description = request.form['seeking_description']

        artist = Artist(
            name=name,
            city=city,
            state_id=state.id,
            phone=phone,
            image_link=image_link,
            facebook_link=facebook_link,
            website=website_link,
            seeking_venue=seeking_venue,
            seeking_description=seeking_description
        )

        genres = request.form.getlist('genres')
        genres = [Genre.query.filter_by(name=genre).first() for genre in genres]
        artist.genres = genres
        db.session.add(artist)
        db.session.commit()

        data['id'] = artist.id
        data['name'] = artist.name
    except():
        db.session.rollback()
        error = True
        print(sys.exc_info())
    finally:
        db.session.close()

    if error:
        # on unsuccessful db insert, flash an error
        flash('An error occurred. Artist ' + data.name + ' could not be listed.')
        abort(500)
    else:
        # on successful db insert, flash success
        flash('Artist ' + request.form['name'] + ' was successfully listed!')

    return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
    # displays list of shows at /shows
    data = Show.query \
        .join(Venue, Show.venue_id == Venue.id) \
        .join(Artist, Show.artist_id == Artist.id) \
        .all()

    show_schema = ShowSchema(many=True)

    return render_template('pages/shows.html', shows=show_schema.dump(data))


@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    error = False
    data = {}

    try:
        venue = Venue.query.filter_by(id=request.form['venue_id']).first()
        artist = Artist.query.filter_by(id=request.form['artist_id']).first()
        start_time = request.form['start_time']

        show = Show(
            venue_id=venue.id,
            artist_id=artist.id,
            start_time=start_time
        )

        db.session.add(show)
        db.session.commit()

        data['id'] = show.id
    except():
        db.session.rollback()
        error = True
        print(sys.exc_info())
    finally:
        db.session.close()

    if error:
        # on unsuccessful db insert, flash an error
        flash('An error occurred. Show could not be listed.')
        abort(500)
    else:
        # on successful db insert, flash success
        flash('Show was successfully listed!')

    return render_template('pages/home.html')


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

# ----------------------------------------------------------------------------#
# Launch.
# ----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
