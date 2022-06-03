
from flask import Blueprint, Flask, redirect, render_template, request, flash, url_for
import dateutil.parser
import babel
from forms import *
import datetime
from models import *
routeVenues = Blueprint('venues', __name__)


def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format, locale='en')

#  Venues
#  ----------------------------------------------------------------


@routeVenues.route('/venues')
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


@routeVenues.route('/venues/search', methods=['POST'])
def search_venues():
    initialInfo1 = ["count", "data"]
    passedList = list()
    listOfVenues = [{"id": venue.id, "name": venue.name} for venue in Venue.query.filter(
        Venue.name.ilike('%' + request.form.get('search_term') + '%')).all()]
    passedList.append(len(Venue.query.filter(Venue.name.ilike(
        '%' + request.form.get('search_term') + '%')).all()))
    passedList.append(listOfVenues)

    return render_template('pages/search_venues.html', results=dict(zip(initialInfo1, passedList)), search_term=request.form.get('search_term', ''))


@routeVenues.route('/venues/<int:venue_id>')
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
            upcomingShowList.append(singleShow.artists.name)
            upcomingShowList.append(singleShow.artists.image_link)
            upcomingShowList.append(
                format_datetime(str(singleShow.start_time)))
            upcomingShowsCombine = dict(zip(initialInfoList, upcomingShowList))
            upcomingNewShows.append(upcomingShowsCombine)
        else:
            numberOfOldShows = numberOfOldShows + 1
            oldShowList.append(singleShow.artist_id)
            oldShowList.append(singleShow.artists.name)
            oldShowList.append(singleShow.artists.image_link)
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


@routeVenues.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@routeVenues.route('/venues/create', methods=['POST'])
def create_venue_submission():
    form = VenueForm()
    try:
        if form.validate_on_submit():
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
            flash('Venue ' + request.form['name'] +
                  ' was successfully listed!')
    except Exception as e:
        flash('Venue ' + request.form['name'] + ' was unsuccessfully listed!')
        print(e)
    finally:
        db.session.close()
        return render_template('pages/home.html')


@routeVenues.route('/venues/<venue_id>', methods=['DELETE'])
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


@routeVenues.route('/venues/<int:venue_id>/edit', methods=['GET'])
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


@routeVenues.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    form = VenueForm()
    try:
        if form.validate_on_submit():
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
