from flask import render_template, flash, Blueprint
from forms import *
from models import *
routeShows = Blueprint('shows', __name__)

#  Shows
#  ----------------------------------------------------------------


@routeShows.route('/shows')
def shows():
    # displays list of shows at /shows
    all_shows = db.session.query(Show).join(Artist).join(Venue).all()

    data = [{"venue_id": show.venue_id, "venue_name": show.venues.name, "artist_id": show.artist_id,
             "artist_name": show.artists.name, "artist_image_link": show.artists.image_link, "start_time": show.start_time.isoformat()} for show in all_shows]

    return render_template('pages/shows.html', shows=data)


@routeShows.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@routeShows.route('/shows/create', methods=['POST'])
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
    except Exception as e:
        # e.g., flash('An error occurred. Show could not be listed.')
        # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
        db.session.rollback()
        flash('Show was unsuccessfully listed!')
        print(e)
    finally:
        db.session.close()
        return render_template('pages/home.html')
