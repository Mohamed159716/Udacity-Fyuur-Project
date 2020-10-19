from flask import render_template, jsonify
from app import db
from sqlalchemy import text
import sqlalchemy
import datetime
from datetime import *

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session,sessionmaker
from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    ForeignKey,
    DateTime,
    Sequence,
    Float
)
import datetime


#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

# showing = db.Table('showing',
#   db.Column('venue_id', db.Integer, db.ForeignKey('Venue.id')),
#   db.Column('artist_id', db.Integer, db.ForeignKey('Artist.id')),
#   db.Column('start_time', db.String(50))
# )

class Showing(db.Model):
    __tablename__ = "Showing"
    id = Column(Integer, primary_key = True)
    venue_id = Column(Integer, ForeignKey('Venue.id'), nullable = False),
    artist_id = Column(Integer, ForeignKey('Artist.id'), nullable = False),
    start_time = Column(String(50))

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = Column(db.Integer,db.Sequence('venue_id'), primary_key=True)
    name = db.Column(String(120))
    city = Column(String(120))
    state = Column(String(120))
    address = Column(String(120))
    genres = Column(String(120))
    phone = Column(String(120))
    seeking_venue = Column(String(10), default = "True")
    seeking_description = Column(String(300))
    website = Column(String(120))
    image_link = Column(String(500))
    facebook_link = Column(String(120))


    def __repr__(self):
      return f"<Venue Id: {self.id}, Name: {self.name}, City: {self.city}, Address: {self.address}, Phone: {self.phone}>"

    def create(self):
        venue_data = Venue(
            name = self('name'), 
            city = self("city"), 
            state = self("state"), 
            address = self("address"), 
            phone = self("phone"), 
            seeking_venue = self("seeking_venue"), 
            seeking_description = self("seeking_description"), 
            website = self("website") ,
            facebook_link = self("facebook_link"), 
            image_link = self("image_link")
        )
        db.session.add(venue_data)
        db.session.commit()

    def read():
        return Venue.query.order_by("id").all()

    def show_venue(self):
        data = Venue.query.get(self)

        today_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        venue_data = []
        query = sqlalchemy.text(f"select artist_id, start_time from showing where venue_id = {self}")  
        query_result = db.engine.execute(query)
        fetch_all_data = query_result.fetchall()
        for row in fetch_all_data:    
            venue_data.append(row)

        upcomming_show_count = 0
        past_show_count = 0

        upcomming_show_arr = []
        past_show_arr = []

        upcomming_show_artist_arr = []
        past_show_artist_arr = []

        for i in range(0, len(venue_data)):
            if today_date > venue_data[i][1]:
                past_show_count += 1
                past_show_arr.append(venue_data[i])
                past_show_artist_arr.append(Artist.query.get(venue_data[i][0]))
            else:
                upcomming_show_count += 1
                upcomming_show_arr.append(venue_data[i])
                upcomming_show_artist_arr.append(Artist.query.get(venue_data[i][0]))

        return { 
            "venue": data,
            "upcomming_artist" :  upcomming_show_artist_arr,
            "upcomming_date" :  upcomming_show_arr,
            "upcomming_count" :  upcomming_show_count,

            "past_artist" :  past_show_artist_arr,
            "past_date" :  past_show_arr,
            "past_count" :  past_show_count
        
        }

    def update(self, venue_id):
        data = Venue.query.get(venue_id)
        data.name = self('name')
        data.city = self('city')
        data.state = self('state')
        data.phone = self('phone')
        data.genres = self('geners')
        data.seeking_venue = self('seeking_venue')
        data.seeking_description = self('description')
        data.website = self('website')
        data.facebook_link = self('facebook_link')
        data.image_link = self('image_link')

        db.session.commit()

    def delete(self):
        try:
            Venue.query.filter_by(id = self).delete()
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.rollback()
        return jsonify({'success': True})


#----------------------------------------------------------------------
# Artist Model
#-------------


class Artist(db.Model):
    __tablename__ = 'Artist'

    id = Column(Integer,Sequence('artist_id'), primary_key=True)
    name = Column(String)
    city = Column(String(120))
    state = Column(String(120))
    phone = Column(String(120))
    seeking_venue = Column(String(10), default = "True")
    seeking_description = Column(String(300))
    genres = Column(String(120))
    website = Column(String(120))
    image_link = Column(String(500))
    facebook_link = Column(String(120))

    # show = db.relationship('Venue', secondary=showing, backref=db.backref('show', lazy='joined'))

    #Venue = db.relationship("Show", backref="showing")

    def create(self):
        artist_data = Artist(
            name = self('name'), 
            city = self("city"), 
            state = self("state"), 
            phone = self("phone"),
            genres = self("genres"), 
            seeking_venue = self("seeking_venue"), 
            seeking_description = self("seeking_description"), 
            website = self("website") ,
            facebook_link = self("facebook_link"), 
            image_link = self("image_link")
        )
        db.session.add(artist_data)
        db.session.commit()

    def read():
        return Artist.query.order_by("id").all()

    def show_artist(self):
        data = Artist.query.get(self)

        today_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 

        artist_data = []
        query = sqlalchemy.text(f"select venue_id, start_time from showing where artist_id = {self}")  
        query_result = db.engine.execute(query)
        fetch_all_data = query_result.fetchall()
        for row in fetch_all_data:    
            artist_data.append(row)

        upcomming_show_count = 0
        past_show_count = 0

        upcomming_show_arr = []
        past_show_arr = []

        upcomming_show_venue_arr = []
        past_show_venue_arr = []

        for i in range(0, len(artist_data)):
            if today_date > artist_data[i][1]:
                past_show_count += 1
                past_show_arr.append(artist_data[i])
                past_show_venue_arr.append(Venue.query.get(artist_data[i][0]))
            else:
                upcomming_show_count += 1
                upcomming_show_arr.append(artist_data[i])
                upcomming_show_venue_arr.append(Venue.query.get(artist_data[i][0]))
        return { 
            "artist": data,
            "upcomming_venue" :  upcomming_show_venue_arr,
            "upcomming_date" :  upcomming_show_arr,
            "upcomming_count" :  upcomming_show_count,

            "past_venue" :  past_show_venue_arr,
            "past_date" :  past_show_arr,
            "past_count" :  past_show_count

        }



    def update(self, artist_id):
        data = Artist.query.get(artist_id)
        data.name = self('name'), 
        data.city = self("city"), 
        data.state = self("state"), 
        data.phone = self("phone"),
        data.genres = self("genres"), 
        data.seeking_venue = self("seeking_venue"), 
        data.seeking_description = self("seeking_description"), 
        data.website = self("website") ,
        data.facebook_link = self("facebook_link"), 
        data.image_link = self("image_link")

        db.session.commit()

    def delete(self):
        try:
            Artist.query.filter_by(id = self).delete()
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.rollback()
        return jsonify({'success': True})
