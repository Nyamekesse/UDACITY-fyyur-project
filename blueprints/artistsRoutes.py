import babel
import dateutil.parser
from flask import (Blueprint, redirect, render_template,
                   request, flash, url_for)
from forms import *
import datetime
from models import *

routeArtists = Blueprint('artists', __name__)


def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format, locale='en')

#  Artists
#  ----------------------------------------------------------------


@routeArtists.route('/artists')
def artists():
    data = [{"id": artist.id, "name": artist.name}
            for artist in Artist.query.order_by(Artist.name).all()]
    return render_template('pages/artists.html', artists=data)


@routeArtists.route('/artists/search', methods=['POST'])
def search_artists():
    initialInfo1 = ["count", "data"]
    passedList = list()
    listOfArtist = [{"id": artist.id, "name": artist.name} for artist in Artist.query.filter(
        Artist.name.ilike('%' + request.form.get('search_term') + '%')).all()]

    passedList.append(len(Artist.query.filter(Artist.name.ilike(
        '%' + request.form.get('search_term') + '%')).all()))
    passedList.append(listOfArtist)

    return render_template('pages/search_artists.html', results=dict(zip(initialInfo1, passedList)), search_term=request.form.get('search_term', ''))


@routeArtists.route('/artists/<int:artist_id>')
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
    # query to get upcoming shows using joins from shows table and venue table
    # filtering by start time being greater than present time
    upcoming_shows_query = db.session.query(Show).join(Venue).filter(
        Show.artist_id == artist_id).filter(Show.start_time > datetime.datetime.now()).all()
    # looping through the gathered upcoming shows and appending
    # the needed info inside a list
    for singleShow in upcoming_shows_query:
        newUpcomingShowsList.append(singleShow.artist_id)
        newUpcomingShowsList.append(singleShow.venues.name)
        newUpcomingShowsList.append(singleShow.venues.image_link)
        newUpcomingShowsList.append(
            format_datetime(str(singleShow.start_time)))
        upcomingShowsCombine = dict(
            zip(initialInfoList, newUpcomingShowsList))
        newUpcomingShowsList.clear()
        upcomingNewShows.append(upcomingShowsCombine)
    # query to get upcoming shows using joins from shows table and venue table
    # filtering by start time being less than present time
    past_shows_query = db.session.query(Show).join(Venue).filter(
        Show.artist_id == artist_id).filter(Show.start_time < datetime.datetime.now()).all()
    # looping through the gathered past shows and appending
    # the needed info inside a list
    for singleShow in past_shows_query:
        oldShowsList.append(singleShow.artist_id)
        oldShowsList.append(singleShow.venues.name)
        oldShowsList.append(singleShow.venues.image_link)
        oldShowsList.append(format_datetime(
            str(singleShow.start_time)))
        oldShowsCombine = dict(zip(initialInfoList, oldShowsList))
        oldShowsList.clear()
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
    exportSingleArtist.append(len(past_shows_query))
    exportSingleArtist.append(upcomingNewShows)
    exportSingleArtist.append(len(upcoming_shows_query))
    return render_template('pages/show_artist.html', artist=dict(zip(expectedDataInfo, exportSingleArtist)))

#  Update
#  ----------------------------------------------------------------


@routeArtists.route('/artists/<int:artist_id>/edit', methods=['GET'])
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


@routeArtists.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    form = ArtistForm()
    # artist record with ID <artist_id> using the new attributes
    try:
        if form.validate_on_submit():
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
        return redirect(url_for('artists.show_artist', artist_id=artist_id))


#  Create Artist
#  ----------------------------------------------------------------
@routeArtists.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@routeArtists.route('/artists/create', methods=['POST'])
def create_artist_submission():
    # called upon submitting the new artist listing form
    form = ArtistForm(request.form)
    try:
        if form.validate_on_submit():
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
            flash('Artist ' + request.form['name'] +
                  ' was successfully listed!')
    except Exception as e:
        print(e)
        flash('Artist ' + request.form['name'] +
              ' was unsuccessfully listed!')
    finally:
        db.session.close()
        return render_template('pages/home.html')
