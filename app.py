#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import re
import dateutil.parser
import babel
from datetime import datetime
from flask import (
  Flask, 
  render_template,
  request, 
  Response,
  flash, redirect,
  url_for,
  jsonify
)
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
import os
from flask_migrate import Migrate
from models import *
import collections

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db.init_app(app)
collections.Callable= collections.abc.Callable
# TODO: connect to a local postgresql database
migrate = Migrate(app, db)
#----------------------------------------------------------------------------#
# Models.

#----------------------------------------------------------------------------#


    # TODO: implement any missing fields, as a database migration using Flask-Migrate

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
  venue_city_state = Venue.query.distinct(Venue.city, Venue.state).all()
  data = []

  datetime.now()

  for venue in venue_city_state:
    response = {
        'city': venue.city,
        'state': venue.state
    }
    venues = Venue.query.filter_by(city=venue.city, state=venue.state)
    venues_list = []
    for venue in venues:
     venue_shows = Show.query.filter_by(venue_id=venue.id).all()
     num_upcoming = 0
     for show in venue_shows:
      if show.start_time > datetime.now():
       num_upcoming += 1
     venues_list.append({
         "id": venue.id,
         "name": venue.name,
         "num_upcoming_shows": num_upcoming
     })
     response['venues'] = venues_list
    data.append(response)
  return render_template('pages/venues.html', areas=data)


@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  search_term = request.form.get('search_term', '')
  venue_search = Venue.query.filter(
      Venue.name.ilike('%' + search_term + '%')).all()
  response = {
      "count": len(venue_search),
      "data": venue_search
  }
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id

  venue = Venue.query.get(venue_id)
  upcoming_shows = []
  past_shows = []
  if not venue:
   return render_template('pages/home.html')

  else:
      for show in venue.shows:
        temp_show = {
            'artist_id': show.artist_id,
            'artist_name': show.artist.name,
            'artist_image_link': show.artist.image_link,
            'start_time': show.start_time.strftime("%m/%d/%Y, %H:%M")}

        if show.start_time <= datetime.now():
          past_shows.append(temp_show)
        else:
          upcoming_shows.append(temp_show)

      data = {
          "id": venue.id,
          "name": venue.name,
          "genres": venue.genres,
          "address": venue.address,
          "city": venue.city,
          "state": venue.state,
          "phone": venue.phone,
          "website_link": venue.website_link,
          "facebook_link": venue.facebook_link,
          "seeking_talent": venue.seeking_talent,
          "seeking_description": venue.seeking_description,
          "image_link": venue.image_link,
          "past_shows": past_shows,
          "upcoming_shows": upcoming_shows,
          "past_shows_count": len(past_shows),
          "upcoming_shows_count": len(upcoming_shows),
      }

      return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------


@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
    # TODO: modify data to be the data object returned from db insertion
  form = VenueForm()
  try:
    venue = Venue(
        name=form.name.data,
        city=form.city.data,
        state=form.state.data,
        address=form.address.data,
        phone=form.phone.data,
        genres=form.genres.data,
        facebook_link=form.facebook_link.data,
        image_link=form.image_link.data,
        website_link=form.website_link.data,
        seeking_talent=form.seeking_talent.data,
        seeking_description=form.seeking_description.data)

    db.session.add(venue)
    db.session.commit()
  # on successful db insert, flash success
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
  except:
    flash('An error occurred. Venue ' +
          request.form['name'] + ' could not be listed.')
  finally:
    db.session.close()
    return render_template('pages/home.html')


@app.route('/venues/<int:venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  venue = Venue.query.get(venue_id)
  try:
    db.session.delete(venue)
    db.session.commit()
  except:
    db.session.rollback()
  finally:
    db.session.close()
  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to  return render_template('pages/home.html')
  return render_template('pages/home.html')

#  Artists
#  ----------------------------------------------------------------


@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  artists = Artist.query.all()
  data = []

  for artist in artists:
    response = {
      'name': artist.name,
      "id": artist.id
    }
    artists = Artist.query.filter_by(name=artist.name, id=artist.id)
    artist_list = []
    for artist in artists:
     artist_list.append({
        "id": artist.id,
        "name": artist.name,
         })
     response['artists'] = artist_list
    data.append(response)

  return render_template('pages/artists.html', artists=data)


@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  search_term = request.form.get('search_term', '').strip()
  artists = Artist.query.filter(
  Artist.name.ilike('%' + search_term + '%')).all()
  artist_list = []
  datetime.now()
  for artist in artists:
    artist_shows = Show.query.filter_by(artist_id=artist.id).all()
    num_upcoming = 0
    for show in artist_shows:
     if show.start_time > datetime.now():
       num_upcoming += 1

  artist_list.append({
    "id": artist.id,
     "name": artist.name
     })

  response = {
      "count": len(artists),
        "data": artist_list
      }

  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id
  artist = Artist.query.get(artist_id)
  upcoming_shows = []
  past_shows = []
  if not artist:
      return render_template('pages/home.html')
  else:
       for show in artist.shows:
         temp_show = {
             'venue_id': show.venue_id,
             'venue_name': show.venue.name,
             'venue_image_link': show.venue.image_link,
             'start_time': show.start_time.strftime("%m/%d/%Y, %H:%M")}

         if show.start_time <= datetime.now():
          past_shows.append(temp_show)
         else:
          upcoming_shows.append(temp_show)

  data = {
    "id": artist.id,
        "name": artist.name,
        "genres": artist.genres,
        "city": artist.city,
        "state": artist.state,
        "phone": artist.phone,
        "website_link": artist.website_link,
        "facebook_link": artist.facebook_link,
        "seeking_venue": artist.seeking_venue,
        "seeking_description": artist.seeking_description,
        "image_link": artist.image_link,
     "past_shows": past_shows,
     "upcoming_shows": upcoming_shows,
     "past_shows_count": len(past_shows),
     "upcoming_shows_count": len(upcoming_shows),
     }

  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
 
  artist = Artist.query.get(artist_id)
  form = ArtistForm(obj=artist) 
  artist = {
      "id": artist_id,
      "name": artist.name,
      "genres": artist.genres,
      "city": artist.city,
      "state": artist.state,
      "phone":artist.phone,
      "website_link": artist.website_link,
      "facebook_link": artist.facebook_link,
      "seeking_venue": artist.seeking_venue,
      "seeking_description": artist.seeking_description,
      "image_link": artist.image_link
  }

  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
 artist = Artist.query.get(artist_id)
 form=ArtistForm(request.form)
 artist.name=form.name.data
 artist.city=form.city.data,
 artist.state=form.state.data,
 artist.phone=form.phone.data,
 artist.genres=form.genres.data,
 artist.facebook_link=form.facebook_link.data,
 artist.image_link=form.image_link.data,
 artist.website_link=form.website_link.data,
 if form.validate():
    artist.seeking_venue= False
 artist.seeking_venue= form.seeking_venue.data 
 artist.seeking_description=form.seeking_description.data

 try: 
    db.session.commit()
  # on successful db insert, flash success
    flash('Artist ' + request.form['name'] + ' was successfully Edited!')
 except:
    flash('An error occurred. Artist' + request.form['name'] + ' could not be Edited.')
 finally:
    db.session.close()
 return redirect(url_for('show_artist', artist_id=artist_id))



@app.route('/artists/<int:artist_id>', methods=['DELETE'])
def delete_artist(artist_id):
  
  try:
    artist= Artist.query.filter_by(id=artist_id).first()
    db.session.delete(artist)
    db.session.commit()
  except:
    db.session.rollback()  
  finally:
    db.session.close() 
    return render_template('pages/home.html')


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
     
    venue = Venue.query.get(venue_id)  
  
    form = VenueForm(obj=venue)
    
    venue = {
        "id": venue_id,
        "name": venue.name,
        "genres": venue.genres,
        "address": venue.address,
        "city": venue.city,
        "state": venue.state,
        "phone":venue.phone,
        "website_link": venue.website_link,
        "facebook_link": venue.facebook_link,
        "seeking_talent": venue.seeking_talent,
        "seeking_description": venue.seeking_description,
        "image_link": venue.image_link
    }

    return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
 
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
 venue = Venue.query.get(venue_id)
 form=VenueForm(request.form)
 venue.name=form.name.data
 venue.address=form.address.data
 venue.city=form.city.data,
 venue.state=form.state.data,
 venue.phone=form.phone.data,
 venue.genres=form.genres.data,
 venue.facebook_link=form.facebook_link.data,
 venue.image_link=form.image_link.data,
 venue.website_link=form.website_link.data,
 if form.validate():
    venue.seeking_talent= False
 venue.seeking_talent= form.seeking_talent.data 
 venue.seeking_description=form.seeking_description.data

 try: 
    db.session.commit()
  # on successful db insert, flash success
    flash('Venue ' + request.form['name'] + ' was successfully Edited!')
 except:
    flash('An error occurred. Venue ' + request.form['name'] + ' could not be Edited.')
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
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  form=ArtistForm()
  try: 
    artist=Artist(
        name=form.name.data,
        city=form.city.data,
        state=form.state.data,
        phone=form.phone.data,
        genres=form.genres.data,
        facebook_link=form.facebook_link.data,
        image_link=form.image_link.data,
        website_link=form.website_link.data,
        seeking_venue=form.seeking_venue.data,
        seeking_description=form.seeking_description.data)   
  
    db.session.add(artist)  
    db.session.commit()
  # on successful db insert, flash success
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
  except:
    flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')
  finally:
    db.session.close()
    return render_template('pages/home.html')
  # on successful db insert, flash success
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.

 list_of_shows=[]
 shows=Show.query.all()
 for show in shows:
   list_of_shows.append({
             "venue_id": show.venue.id,
            "venue_name": show.venue.name,
            "artist_id": show.artist.id,
            "artist_name": show.artist.name,
            "artist_image_link": show.artist.image_link,
            "start_time": format_datetime(str(show.start_time))
   })

 return render_template('pages/shows.html', shows=list_of_shows)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  form=ShowForm(request.form)
  show=Show(
    artist_id=form.artist_id.data,
    venue_id=form.venue_id.data,
    start_time=form.start_time.data
  )
  try:
    db.session.add(show)
    db.session.commit()
    flash('Show was successfully listed!')
  except:
    db.session.rollback()
    flash('Show could not be listed')
  finally:
    db.session.close()   

  # on successful db insert, flash success
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
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