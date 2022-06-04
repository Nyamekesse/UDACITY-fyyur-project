import dateutil.parser
import babel
from flask import (Blueprint, redirect, render_template,
                   request, flash, url_for)
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


def validate_contact(num):
    if len(num) != 10:
        return False
    else:
        return True
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
    oldShowList = list()
    exportSingleVenueList = list()
    upcomingShowList = list()
    upcomingNewShows = list()
    oldShows = list()
    # select the specific info by querying
    venue = Venue.query.get(venue_id)
    # create initial list to be used to match data later
    initialInfoList = ["artist_id", "artist_name",
                       "artist_image_link", "start_time"]
    expectedDataInfo = ["id", "name", "genres", "address", "city", "state", "phone", "website", "facebook_link", "seeking_talent",
                        "seeking_description", "image_link", "past_shows", "past_shows_count", "upcoming_shows", "upcoming_shows_count"]
    # query to get upcoming shows using joins from shows table and artist table
    # filtering by start time being greater than present time
    upcoming_shows_query = db.session.query(Show).join(Artist).filter(
        Show.venue_id == venue_id).filter(Show.start_time > datetime.datetime.now()).all()
    for singleShow in upcoming_shows_query:
        upcomingShowList.append(singleShow.artist_id)
        upcomingShowList.append(singleShow.artists.name)
        upcomingShowList.append(singleShow.artists.image_link)
        upcomingShowList.append(
            format_datetime(str(singleShow.start_time)))
        upcomingShowsCombine = dict(zip(initialInfoList, upcomingShowList))
        upcomingShowList.clear()
        upcomingNewShows.append(upcomingShowsCombine)
    # query to get past shows using joins from shows table and artist table
    # filtering by start time being less than present time
    past_shows_query = db.session.query(Show).join(Artist).filter(
        Show.venue_id == venue_id).filter(Show.start_time < datetime.datetime.now()).all()
    for singleShow in past_shows_query:
        oldShowList.append(singleShow.artist_id)
        oldShowList.append(singleShow.artists.name)
        oldShowList.append(singleShow.artists.image_link)
        oldShowList.append(format_datetime(str(singleShow.start_time)))
        oldShowsCombine = dict(zip(initialInfoList, oldShowList))
        oldShowList.clear()
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
    exportSingleVenueList.append(len(past_shows_query))
    exportSingleVenueList.append(upcomingNewShows)
    exportSingleVenueList.append(len(upcoming_shows_query))

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
    form = VenueForm(request.form)
    isValid = validate_contact(request.form['phone'])
    try:
        if(isValid == False):
            flash('In correct contact number')
        elif form.validate_on_submit():
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
        flash('Venue ' + request.form['name'] +
              ' was unsuccessfully listed!\n'+e)
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
        return redirect(url_for('venues.show_venue', venue_id=venue_id))
