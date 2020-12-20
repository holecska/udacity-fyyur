#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, jsonify
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import FlaskForm
from forms import *
from flask_migrate import Migrate
import os
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#
app = Flask(__name__)
app.config.from_object('config')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost:5432/fyyur'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)
moment = Moment(app)

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'venues'

    id = db.Column(db.Integer, primary_key=True, nullable = False)
    name = db.Column(db.String(), nullable = False)
    city = db.Column(db.String(120), nullable = False)
    state = db.Column(db.String(120), nullable = False)
    address = db.Column(db.String(120), nullable = False)
    phone = db.Column(db.String(120), nullable = False)
    facebook_link = db.Column(db.String(120), nullable = False)
    genres = db.Column(db.ARRAY(db.String))
    image_link = db.Column(db.String(500))
    seeking_talent = db.Column(db.Boolean, nullable = False)
    seeking_description = db.Column(db.Text)
    website = db.Column(db.String(200))
    shows = db.relationship('Show', backref='venue', lazy=True, passive_deletes=True)

class Artist(db.Model):
    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True, nullable = False)
    name = db.Column(db.String(120), nullable = False)
    city = db.Column(db.String(120), nullable = False)
    state = db.Column(db.String(120), nullable = False)
    phone = db.Column(db.String(120), nullable = False)
    facebook_link = db.Column(db.String(120), nullable = False)
    genres = db.Column(db.ARRAY(db.String))
    shows = db.relationship('Show', backref='artist', lazy=True)
    website = db.Column(db.String(200))
    seeking_venue = db.Column(db.Boolean, nullable = False)
    seeking_description = db.Column(db.Text)
    image_link = db.Column(db.String(500))

    def __repr__(self):
      return f'<Artist {self.id} {self.name} {self.city}>'

class Show(db.Model):
    __tablename__ = 'shows'

    id = db.Column(db.Integer, primary_key=True, nullable = False)
    start_time = db.Column(db.DateTime()) #nullable = False
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('venues.id', ondelete='CASCADE'), nullable=False)

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

  data = []
  cities_venue = []
  for city in Venue.query.with_entities(Venue.city).all():
      city = ''.join(city)
      hasThisCity = False

      for i in range(0, len(cities_venue)):
          if (cities_venue[i] == city):
              hasThisCity = True

      if not hasThisCity:
          cities_venue.append(city)

  venues = []
  for city_in_list in cities_venue:
      venuePerCity = []
      for venues_by_city in Venue.query.filter_by(city=city_in_list).all():
          state = venues_by_city.state
          new_venue = {
            "id": venues_by_city.id,
            "name": venues_by_city.name
          }
          venuePerCity.append(new_venue)
      venuesCollect  = venuePerCity
      venueCity = {
        "city": city_in_list
      }
      venueCity['state'] = state
      venueCity['venues'] = venuesCollect
      data.append(venueCity);

  return render_template('pages/venues.html', areas=data);

@app.route('/venues/search', methods=['POST'])
def search_venues():

  search_text = request.form['search_term']
  search_text = search_text.lower()
  split_search = search_text.split()

  venues = Venue.query.with_entities(Venue.name, Venue.id).all()

  counter = 0
  response = {}
  data = []
  for venue in venues:
      findObj = False

      for el in split_search:
          name = venue.name
          #SEARCHING in the Name words
          name_word = name.split()
          for word in name_word:
              e = word.lower()
              if e.find(el) !=-1:
                  findObj = True

      if findObj:
          venue_id = venue.id

          sub_result = {
            'id': venue.id,
            'name': venue.name,
            'num_upcoming_shows': Show.query.filter(Show.start_time < datetime.now(), Show.venue_id == venue_id).count()
          }
          data.append(sub_result)
          counter += 1

  response['count'] = counter
  response['data'] = data

  def myFunc(e):
      return e['num_upcoming_shows']
  response['data'].sort(key=myFunc)

  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):

  try:
      past_shows = Show.query.filter(Show.start_time < datetime.now(), Show.venue_id == venue_id).all()
      upcoming_shows = Show.query.filter(Show.start_time < datetime.now(), Show.venue_id == venue_id).all()
      venue = Venue.query.filter_by(id=venue_id).first_or_404()

      data = {
          'id': venue.id,
          'name': venue.name,
          'genres': venue.genres,
          'city': venue.city,
          'state':  venue.state,
          'address':  venue.address,
          'phone': venue.phone,
          'website': venue.website,
          'facebook_link': venue.facebook_link,
          'seeking_talent': venue.seeking_talent,
          'seeking_description': venue.seeking_description,
          'image_link': venue.image_link,
          'website': venue.website,
          'past_shows': [{
              'artist_id': p.artist_id,
              'artist_name': p.artist.name,
              'artist_image_link': p.artist.image_link,
              'start_time': p.start_time.strftime("%m/%d/%Y, %H:%M")
          } for p in past_shows],
          'upcoming_shows': [{
              'venue_id': u.artist_id,
              'venue_name': u.artist.name,
              'venue_image_link': u.artist.image_link,
              'start_time': u.start_time.strftime("%m/%d/%Y, %H:%M")
          } for u in upcoming_shows],
          'past_shows_count': len(past_shows),
          'upcoming_shows_count': len(upcoming_shows)
        }
      return render_template('pages/show_venue.html', venue=data)
  except:
      flash('Sorry we couldn\'t show the venue page')
      return redirect(url_for('index'))


#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    error = False
    try:
      data = request.get_json()
      genres = request.get_json()['genres']
      venue = Venue(name=data['name'], city=data['city'], state=data['state'], address=data['address'], phone=data['phone'], facebook_link=data['facebook_link'], genres=genres,  image_link=data['image_link'],  seeking_description=data['seeking_description'], seeking_talent=data['seeking_talent'], website=data['website'])
      db.session.add(venue)
      db.session.commit()
    except:
      error = True
      db.session.rollback()
    finally:
      db.session.close()
    if error:
        return jsonify({'success': 'no'})
    else:
        return jsonify({'success': 'ok'})

@app.route('/venues/<venue_id>', methods=['POST'])
def delete_venue(venue_id):

  #try:
  venue = Venue.query.filter_by(id=venue_id).first_or_404()

  db.session.delete(venue)
  db.session.commit()
  flash('The Venue was successfully deleted with its all shows!')
  return redirect(url_for('index'))
#except:
  #flash('Sorry we couldn\'t delete the venue')
  #return redirect(url_for('index'))
#finally:
  db.session.close()

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  artists = Artist.query.order_by('id').all()

  return render_template('pages/artists.html', artists=artists)

@app.route('/artists/search', methods=['POST'])
def search_artists():

  search_text = request.form['search_term']
  search_text = search_text.lower()
  split_search = search_text.split()

  artists = Artist.query.with_entities(Artist.name, Artist.id).all()
  print(artists)
  counter = 0
  response = {}
  data = []
  for artist in artists:
      findObj = False

      for el in split_search:
          name = artist.name
          #SEARCHING in the Name words
          name_word = name.split()
          for word in name_word:
              e = word.lower()
              if e.find(el) !=-1:
                  findObj = True

      if findObj:
          artist_id = artist.id

          sub_result = {
            'id': artist.id,
            'name': artist.name,
            'upcoming_shows': Show.query.filter(Show.start_time < datetime.now(), Show.artist_id == artist_id).count()
          }
          data.append(sub_result)
          counter += 1

  response['count'] = counter
  response['data'] = data
  #print(split_search)
  def myFunc(e):
      return e['upcoming_shows']
  response['data'].sort(key=myFunc)

  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):

    try:
        past_shows = Show.query.filter(Show.start_time < datetime.now(), Show.artist_id == artist_id).all()
        upcoming_shows = Show.query.filter(Show.start_time < datetime.now(), Show.artist_id == artist_id).all()
        artist = Artist.query.filter_by(id=artist_id).first_or_404()

        data = {
            'id': artist.id,
            'name': artist.name,
            'genres': artist.genres,
            'city': artist.city,
            'state':  artist.state,
            'phone': artist.phone,
            'website': artist.website,
            'facebook_link': artist.facebook_link,
            'seeking_venue': artist.seeking_venue,
            'seeking_description': artist.seeking_description,
            'image_link': artist.image_link,
            'past_shows': [{
                'venue_id': p.venue_id,
                'venue_name': p.venue.name,
                'venue_image_link': p.venue.image_link,
                'start_time': p.start_time.strftime("%m/%d/%Y, %H:%M")
            } for p in past_shows],
            'upcoming_shows': [{
                'venue_id': u.venue_id,
                'venue_name': u.venue.name,
                'venue_image_link': u.venue.image_link,
                'start_time': u.start_time.strftime("%m/%d/%Y, %H:%M")
            } for u in upcoming_shows],
            'past_shows_count': len(past_shows),
            'upcoming_shows_count': len(upcoming_shows)
          }

        return render_template('pages/show_artist.html', artist=data)
    except:
       flash('Sorry we couldn\'t show the artist')
       return redirect(url_for('index'))

#  ----------------------------------------------------------------
#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  artist = Artist.query.filter_by(id=artist_id).first_or_404()
  print(artist.seeking_venue)
  form = ArtistForm(obj=artist)

  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    error = False
    try:
        form_data = request.form
        artist = Artist.query.filter_by(id=artist_id).first_or_404()

        artist.name = request.form['name']
        artist.genres = request.form.getlist('genres')
        artist.city = request.form['city']
        artist.state = request.form['state']
        artist.phone = request.form['phone']
        artist.website = request.form['website']
        artist.facebook_link = request.form['facebook_link']
        #print(request.form['seeking_venue'].value)
        option = request.form.getlist('seeking_venue')
        #print(option)
        if option[0] == 'True':
           artist.seeking_venue = True
        else:
           artist.seeking_venue = False

        artist.seeking_description = request.form['seeking_description']
        artist.image_link = request.form['image_link']

        db.session.add(artist)
        db.session.commit()

    except:
        error = True
        db.session.rollback()
    finally:
        db.session.close()

    if error:
        flash('Sorry, an error occured, we couldn\'t edit this artist')
        return redirect(url_for('show_artist', artist_id=artist_id))
    else:
        flash('edit this artist was succesfull')
        return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  venue = Venue.query.filter_by(id=venue_id).first_or_404()
  form = VenueForm(obj=venue)
  print(venue)
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):

  error = False
  try:
      form_data = request.form
      venue = Venue.query.filter_by(id=venue_id).first_or_404()

      venue.name = request.form['name']
      venue.genres = request.form.getlist('genres')
      venue.address = request.form['address']
      venue.city = request.form['city']
      venue.state = request.form['state']
      venue.phone = request.form['phone']
      venue.website = request.form['website_link']
      venue.facebook_link = request.form['facebook_link']

      if (request.form['seeking_talent']) == 'on':
          venue.seeking_talent = True
      else:
          venue.seeking_talent = False

      venue.seeking_description = request.form['seeking_description']
      venue.image_link = request.form['image_link']

      db.session.add(venue)
      db.session.commit()

  except:
      error = True
      db.session.rollback()
  finally:
      db.session.close()
  if error:
      flash('Sorry, an error occured, we couldn\'t edit this value')
      return redirect(url_for('show_venue', venue_id=venue_id))
  else:
      flash('edit this value was succesfull')
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
    try:
      data = request.get_json()
      genres = request.get_json()['genres']
      artist = Artist(name=data['name'], city=data['city'], state=data['state'], phone=data['phone'], facebook_link=data['facebook_link'], genres=genres, website=data['website'], seeking_venue=data['seeking_venue'], image_link=data['image_link'], seeking_description=data['seeking_description'])
      db.session.add(artist)
      db.session.commit()
    except:
      error = True
      db.session.rollback()
    finally:
      db.session.close()
    if error:
        return jsonify({'success': 'no'})
    else:
        return jsonify({'success': 'ok'})

#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # num_shows should be aggregated based on number of upcoming shows per venue.
    try:

      shows = Show.query.join(Venue, Show.venue_id == Venue.id).join(Artist, Artist.id == Show.artist_id).filter(Show.start_time > datetime.now()).order_by((Show.start_time).desc()).all()
      data = []
      for show in shows:
          newShowObj = {
            'venue_id': show.venue.id,
            'venue_name': show.venue.name,
            'artist_id': show.artist.id,
            'artist_name': show.artist.name,
            'artist_image_link': show.artist.image_link,
            'start_time': show.start_time.strftime("%m/%d/%Y, %H:%M")
          }
          data.append(newShowObj)
      print(data)
      return render_template('pages/shows.html', shows=data)

    except:
       flash('Sorry we couldn\'t render the shows')
       return redirect(url_for('index'))

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    error = False
    try:
      data = request.get_json()

      show = Show(start_time=data['start'], artist_id=data['artist'],  venue_id=data['venue'])
      db.session.add(show)
      db.session.commit()

    except:
      error = True
      db.session.rollback()
    finally:
      db.session.close()
    if error:
        return jsonify({'success': 'no'})
    else:
        return jsonify({'success': 'ok'})

#----------------------------------------------------------------------------#
# errorhandler
#----------------------------------------------------------------------------#
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
