# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#

import dateutil.parser
import babel
from flask import render_template
from flask_moment import Moment
import logging
from logging import (Formatter, FileHandler)
from sqlalchemy import desc
from models import (Artist, Venue, app, db)
from config import DatabaseURI
from blueprints.showsRoute import routeShows
from blueprints.venuesRoutes import routeVenues
from blueprints.artistsRoutes import routeArtists

# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#

app.config['SQLALCHEMY_DATABASE_URI'] = DatabaseURI.SQLALCHEMY_DATABASE_URI
moment = Moment(app)
app.config.from_object('config')
db.init_app(app)
app.register_blueprint(routeShows)
app.register_blueprint(routeVenues)
app.register_blueprint(routeArtists)


# ----------------------------------------------------------------------------#
# Models.
# ----------------------------------------------------------------------------#


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
    venues = Venue.query.order_by(desc(Venue.id)).limit(5).all()
    artists = Artist.query.order_by(desc(Artist.id)).limit(5).all()
    return render_template('pages/home.html', venues=venues, artists=artists)


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
