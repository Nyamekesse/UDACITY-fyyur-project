#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#


import json
from operator import itemgetter
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
import logging
from logging import Formatter, FileHandler

from sqlalchemy import desc
from forms import *
import datetime
from models import *
from config import DatabaseURI
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app.config['SQLALCHEMY_DATABASE_URI'] = DatabaseURI.SQLALCHEMY_DATABASE_URI
moment = Moment(app)
app.config.from_object('config')

db.init_app(app)

# db.create_all()
#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#


#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format, locale='en')


app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


@app.route('/')
def index():
    venues = Venue.query.order_by(desc(Venue.created_date)).limit(10).all()
    artists = Artist.query.order_by(desc(Artist.created_date)).limit(10).all()
    return render_template('pages/home.html', venues=venues, artists=artists)


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
    # query all venues
    getAllVenues = Venue.query.all()
    # create a empty list
    data = list()
    # create a set of unique/non repeating cities and states
    uniqueCity_States = {(venue.city, venue.state) for venue in getAllVenues}
    # returns sorted list of the generated set above
    uniqueCity_States = sorted(uniqueCity_States)
    for cities_and_states in uniqueCity_States:
        # group all venues using state and cities
        groupedVenues = [{"id": venue.id, "name": venue.name} for venue in getAllVenues if (
            venue.city == cities_and_states[0]) and (venue.state == cities_and_states[1])]
        # add grouped venues as well as the city and state which was used to group them to data list to be exported
        data.append(
            {"city": cities_and_states[0], "state": cities_and_states[1], "venues": groupedVenues})
    return render_template('pages/venues.html', areas=data)


@app.route('/venues/search', methods=['POST'])
def search_venues():
    initialInfo1 = ["count", "data"]
    passedList = list()
    listOfVenues = [{"id": venue.id, "name": venue.name} for venue in Venue.query.filter(
        Venue.name.ilike('%' + request.form.get('search_term') + '%')).all()]
    passedList.append(len(Venue.query.filter(Venue.name.ilike(
        '%' + request.form.get('search_term') + '%')).all()))
    passedList.append(listOfVenues)

    return render_template('pages/search_venues.html', results=dict(zip(initialInfo1, passedList)), search_term=request.form.get('search_term', ''))


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    # create empty list variables
    oldShows = list()
    upcomingNewShows = list()
    upcomingShowList = list()
    oldShowList = list()
    exportSingleVenueList = list()
    # initialize & assign variables to 0
    numberOfOldShows = numberOfUpcomingNewShows = 0
    # select the specific info by querying
    venue = Venue.query.get(venue_id)
    # create initial list to be used to match data later
    initialInfoList = ["artist_id", "artist_name",
                       "artist_image_link", "start_time"]
    expectedDataInfo = ["id", "name", "genres", "address", "city", "state", "phone", "website", "facebook_link", "seeking_talent",
                        "seeking_description", "image_link", "past_shows", "past_shows_count", "upcoming_shows", "upcoming_shows_count"]
    # loop through the show result queried
    for singleShow in venue.shows:
        if singleShow.start_time > datetime.datetime.now():
            numberOfUpcomingNewShows = numberOfUpcomingNewShows + 1
            upcomingShowList.append(singleShow.artist_id)
            upcomingShowList.append(singleShow.artist.name)
            upcomingShowList.append(singleShow.artist.image_link)
            upcomingShowList.append(
                format_datetime(str(singleShow.start_time)))
            upcomingShowsCombine = dict(zip(initialInfoList, upcomingShowList))
            upcomingNewShows.append(upcomingShowsCombine)
        else:
            numberOfOldShows = numberOfOldShows + 1
            oldShowList.append(singleShow.artist_id)
            oldShowList.append(singleShow.artist.name)
            oldShowList.append(singleShow.artist.image_link)
            oldShowList.append(format_datetime(str(singleShow.start_time)))
            oldShowsCombine = dict(zip(initialInfoList, oldShowList))
            oldShows.append(oldShowsCombine)
    # adding the needed info to initialized list variable
    exportSingleVenueList.append(venue_id)
    exportSingleVenueList.append(venue.name)
    exportSingleVenueList.append([genre for genre in venue.genres])
    exportSingleVenueList.append(venue.address)
    exportSingleVenueList.append(venue.city)
    exportSingleVenueList.append(venue.state)
    exportSingleVenueList.append(venue.phone)
    exportSingleVenueList.append(venue.website)
    exportSingleVenueList.append(venue.facebook_link)
    exportSingleVenueList.append(venue.seeking_talent)
    exportSingleVenueList.append(venue.seeking_description)
    exportSingleVenueList.append(venue.image_link)
    exportSingleVenueList.append(oldShows)
    exportSingleVenueList.append(numberOfOldShows)
    exportSingleVenueList.append(upcomingNewShows)
    exportSingleVenueList.append(numberOfUpcomingNewShows)

    data = dict(zip(expectedDataInfo, exportSingleVenueList))

    return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------


@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    form = VenueForm()
    try:
        new_venue = Venue(
            name=form.name.data,
            city=form.city.data,
            state=form.state.data,
            address=form.address.data,
            phone=form.phone.data,
            genres=form.genres.data,
            image_link=form.image_link.data,
            website=form.website_link.data,
            facebook_link=form.facebook_link.data,
            seeking_talent=form.seeking_talent.data,
            seeking_description=form.seeking_description.data
        )
        db.session.add(new_venue)
        db.session.commit()
        # on successful db insert, lash success
        flash('Venue ' + request.form['name'] + ' was successfully listed!')
    except Exception as e:
        flash('Venue ' + request.form['name'] + ' was unsuccessfully listed!')
        print(e)
    finally:
        db.session.close()
        return render_template('pages/home.html')


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    try:
        venueToBeDeleted = Venue.query.get(venue_id)
        db.session.delete(venueToBeDeleted)
        db.session.commit()
    # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
    # clicking that button delete it from the db then redirect the user to the homepage
    except Exception as e:
        db.session.rollback()
        print(e)
    finally:
        db.session.close()
        return render_template('pages/home.html')

#  Artists
#  ----------------------------------------------------------------


@app.route('/artists')
def artists():
    data = [{"id": artist.id, "name": artist.name}
            for artist in Artist.query.order_by(Artist.name).all()]
    return render_template('pages/artists.html', artists=data)


@app.route('/artists/search', methods=['POST'])
def search_artists():
    initialInfo1 = ["count", "data"]
    passedList = list()
    listOfArtist = [{"id": artist.id, "name": artist.name} for artist in Artist.query.filter(
        Artist.name.ilike('%' + request.form.get('search_term') + '%')).all()]

    passedList.append(len(Artist.query.filter(Artist.name.ilike(
        '%' + request.form.get('search_term') + '%')).all()))
    passedList.append(listOfArtist)

    return render_template('pages/search_artists.html', results=dict(zip(initialInfo1, passedList)), search_term=request.form.get('search_term', ''))


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    # shows the artist page with the given artist_id
    # create empty list variables
    oldShows = list()
    upcomingNewShows = list()
    oldShowsList = list()
    newUpcomingShowsList = list()
    exportSingleArtist = list()
    # initialize & assign variables to 0
    numberOfOldShows = numberOfUpcomingNewShows = 0
    initialInfoList = ["venue_id", "venue_name",
                       "venue_image_link", "start_time"]
    expectedDataInfo = ["id", "name", "genres", "city", "state", "phone", "website", "facebook_link", "seeking_venue",
                        "seeking_description", "image_link", "past_shows", "past_shows_count", "upcoming_shows", "upcoming_shows_count"]
    artist = Artist.query.get(artist_id)
    # loop through the artist result queried
    for singleShow in artist.shows:
        if singleShow.start_time > datetime.datetime.now():
            numberOfUpcomingNewShows = numberOfUpcomingNewShows + 1
            newUpcomingShowsList.append(singleShow.venue_id)
            newUpcomingShowsList.append(singleShow.venue.name)
            newUpcomingShowsList.append(singleShow.venue.image_link)
            newUpcomingShowsList.append(
                format_datetime(str(singleShow.start_time)))
            upcomingShowsCombine = dict(
                zip(initialInfoList, newUpcomingShowsList))
            upcomingNewShows.append(upcomingShowsCombine)
        else:
            numberOfOldShows = numberOfOldShows + 1
            oldShowsList.append(singleShow.venue_id)
            oldShowsList.append(singleShow.venue.name)
            oldShowsList.append(singleShow.venue.image_link)
            oldShowsList.append(format_datetime(str(singleShow.start_time)))
            oldShowsCombine = dict(zip(initialInfoList, oldShowsList))
            oldShows.append(oldShowsCombine)

    # adding the needed info to initialized list variable
    exportSingleArtist.append(artist_id)
    exportSingleArtist.append(artist.name)
    exportSingleArtist.append([genre for genre in artist.genres])
    exportSingleArtist.append(artist.city)
    exportSingleArtist.append(artist.state)
    exportSingleArtist.append(artist.phone)
    exportSingleArtist.append(artist.website)
    exportSingleArtist.append(artist.facebook_link)
    exportSingleArtist.append(artist.seeking_venue)
    exportSingleArtist.append(artist.seeking_description)
    exportSingleArtist.append(artist.image_link)
    exportSingleArtist.append(oldShows)
    exportSingleArtist.append(numberOfOldShows)
    exportSingleArtist.append(upcomingNewShows)
    exportSingleArtist.append(numberOfUpcomingNewShows)
    return render_template('pages/show_artist.html', artist=dict(zip(expectedDataInfo, exportSingleArtist)))

#  Update
#  ----------------------------------------------------------------


@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    artist = Artist.query.get_or_404(artist_id)
    form = ArtistForm()
    form.name.data = artist.name
    form.city.data = artist.city
    form.state.data = artist.state
    form.phone.data = artist.phone
    form.genres.data = artist.genres
    form.image_link.data = artist.image_link
    form.website_link.data = artist.website
    form.facebook_link.data = artist.facebook_link
    form.seeking_venue.data = artist.seeking_venue
    form.seeking_description.data = artist.seeking_description

    return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    form = ArtistForm()
    # artist record with ID <artist_id> using the new attributes
    try:
        artist = Artist.query.get_or_404(artist_id)
        artist.name = form.name.data
        artist.city = form.city.data
        artist.state = form.state.data
        artist.phone = form.phone.data
        artist.genres = form.genres.data
        artist.image_link = form.image_link.data
        artist.website = form.website_link.data
        artist.facebook_link = form.facebook_link.data
        artist.seeking_venue = form.seeking_venue.data
        artist.seeking_description = form.seeking_description.data
        db.session.commit()
    except Exception as e:
        print(e)
    finally:
        db.session.close()
        return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    venue = Venue.query.get_or_404(venue_id)
    if not venue:
        return redirect(url_for('index'))
    else:
        form = VenueForm()
        form.name.data = venue.name
        form.city.data = venue.city
        form.state.data = venue.state
        form.address.data = venue.address
        form.phone.data = venue.phone
        form.genres.data = venue.genres
        form.image_link.data = venue.image_link
        form.website_link.data = venue.website
        form.facebook_link.data = venue.facebook_link
        form.seeking_talent.data = venue.seeking_talent
        form.seeking_description.data = venue.seeking_description
    return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    form = VenueForm()
    try:
        venue = Venue.query.get_or_404(venue_id)
        venue.name = form.name.data
        venue.city = form.city.data
        venue.state = form.state.data
        venue.address = form.address.data
        venue.phone = form.phone.data
        venue.genres = form.genres.data
        venue.image_link = form.image_link.data
        venue.website = form.website_link.data
        venue.facebook_link = form.facebook_link.data
        venue.seeking_talent = form.seeking_talent.data
        venue.seeking_description = form.seeking_description.data
        db.session.commit()
    except Exception as e:
        print(e)
    finally:
        db.session.close()
        return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------


@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    form = ArtistForm()
    # called upon submitting the new artist listing form
    form = ArtistForm()
    try:
        new_artist = Artist(
            name=form.name.data,
            city=form.city.data,
            state=form.state.data,
            phone=form.phone.data,
            genres=form.genres.data,
            image_link=form.image_link.data,
            website=form.website_link.data,
            facebook_link=form.facebook_link.data,
            seeking_venue=form.seeking_venue.data,
            seeking_description=form.seeking_description.data
        )
        db.session.add(new_artist)
        db.session.commit()
        # on successful db insert, flash success
        flash('Artist ' + request.form['name'] + ' was successfully listed!')
    except Exception as e:
        flash('Artist ' + request.form['name'] + ' was unsuccessfully listed!')
        print(e)
    finally:
        db.session.close()
        return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
    # displays list of shows at /shows
    all_shows = db.session.query(Show).join(Artist).join(Venue).all()

    data = [{"venue_id": show.venue_id, "venue_name": show.venue.name, "artist_id": show.artist_id,
             "artist_name": show.artist.name, "artist_image_link": show.artist.image_link, "start_time": show.start_time.isoformat()} for show in all_shows]

    return render_template('pages/shows.html', shows=data)


@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()

    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    # called to create new shows in the db, upon submitting new show listing form
    form = ShowForm()
    try:
        new_show = Show(artist_id=form.artist_id.data,
                        venue_id=form.venue_id.data, start_time=form.start_time.data)
        db.session.add(new_show)
        db.session.commit()
        # on successful db insert, flash success
        flash('Show was successfully listed!')
    except:
        # e.g., flash('An error occurred. Show could not be listed.')
        # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
        db.session.rollback()
        flash('Show was unsuccessfully listed!')
    finally:
        db.session.close()
        return render_template('pages/home.html')


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(400)
def bad_request_error(error):
    return render_template('errors/400.html'), 400


@app.errorhandler(409)
def duplicate_resource_error(error):
    return render_template('errors/409.html'), 409


@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
