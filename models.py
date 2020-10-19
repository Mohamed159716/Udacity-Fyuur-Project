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

#----------------------------------------------------------------------
# Artist Model
#-------------

class Artist(db.Model):
    __tablename__ = 'Artist'
    id = Column(Integer,Sequence('artist_id'),primary_key=True) 
    name = Column(String)
    city = Column(String(120))
    state = Column(String(120))
    phone = Column(String(120))
    seeking_venue = Column(String(10), default = True)
    seeking_description = Column(String(300))
    genres = Column(String(120))
    website = Column(String(120))
    image_link = Column(String(500))
    facebook_link = Column(String(120))

    #------ CRUD Operation -------- #

    def create(self):
        query = sqlalchemy.text(f'''INSERT INTO "Artist"
        (name, city,genres, state, phone, seeking_venue, seeking_description, website, facebook_link, image_link) 
        VALUES('{self('name')}', '{self('city')}', '{self('genres')}','{self('state')}', '{self('phone')}','{self('seeking_venue')}','{self('description')}','{self('website')}','{self('facebook_link')}', '{self('image_link')}')  ''')

        db.engine.execute(query)

        # artist_data = Artist(
        #     name = self('name'), 
        #     city = self("city"), 
        #     state = self("state"), 
        #     phone = self("phone"),
        #     genres = self("genres"), 
        #     seeking_venue = self("seeking_venue"), 
        #     seeking_description = self("seeking_description"), 
        #     website = self("website") ,
        #     facebook_link = self("facebook_link"), 
        #     image_link = self("image_link")
        # )
        # artist_data = Artist(
        #     name = self('name'),
        #     city = self('city')
        # )
        # db.session.add(artist_data)
        # db.session.commit()

    def read():
        return Artist.query.order_by("id").all()

    def show_artist(self):
        data = Artist.query.get(self)

        today_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 

        artist_data = []
        query = sqlalchemy.text(f'select artist_id, start_time from "Showing" where artist_id = {self}')   
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

#----------------------------------------------------------------------
# Venue Model
#-------------
class Venue(db.Model):
    __tablename__ = 'Venue'
    id = Column(Integer,Sequence('venue_id'),primary_key=True) 
    name = db.Column(String(120))
    city = Column(String(120))
    state = Column(String(120))
    address = Column(String(120))
    genres = Column(String(120))
    phone = Column(String(120))
    seeking_venue = Column(String(10), default = True)
    seeking_description = Column(String(300))
    website = Column(String(120))
    image_link = Column(String(500))
    facebook_link = Column(String(120))

    #------ CRUD Operation -------- #

    def create(self):
        query = sqlalchemy.text(f'''INSERT INTO "Venue"
        (name, city, state, address, phone, seeking_venue, seeking_description, website, facebook_link, image_link) 
        VALUES('{self('name')}', '{self('city')}', '{self('state')}', '{self('address')}','{self('phone')}','{self('seeking_venue')}','{self('description')}','{self('website')}','{self('facebook_link')}', '{self('image_link')}')  ''')

        db.engine.execute(query)


        # venue_data = Venue(
        #     name = self('name'), 
        #     city = self("city"), 
        #     state = self("state"), 
        #     address = self("address"), 
        #     phone = self("phone"), 
        #     seeking_venue = self("seeking_venue"), 
        #     seeking_description = self("seeking_description"), 
        #     website = self("website") ,
        #     facebook_link = self("facebook_link"), 
        #     image_link = self("image_link")
        # )

        # venue_data = Venue(
        #     name = self('name'),
        #     city = self('city')
        # )
        # db.session.add(venue_data)
        # db.session.commit()

    def read():
        return Venue.query.order_by("id").all()

    def show_venue(self):
        data = Venue.query.get(self)

        today_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        venue_data = []
        query = sqlalchemy.text(f'select artist_id, start_time from "Showing" where venue_id = {self}')  
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
# Association Model
#-------------
class Showing(db.Model):
    __tablename__ = 'Showing'
    id = Column(Integer,Sequence('map_seq'),primary_key=True)
    start_time = Column(String(50)) 
    artist_id = Column(Integer,ForeignKey('Artist.id'))
    venue_id = Column(Integer,ForeignKey('Venue.id'))

    #------ Create Operation -------- #
    def create_show(self):
        artist_id = self('artist_id')
        venue_id = self('venue_id')
        start_time = self('start_time')

        artist = Artist.query.get(artist_id)
        venue = Venue.query.get(venue_id)


        if artist and venue:

            # inser start date into association table
            sql_query = sqlalchemy.text(f''' INSERT INTO "Showing"(start_time, artist_id, venue_id) VALUES('{start_time}', {artist_id}, {venue_id}) ''')
            db.engine.execute(sql_query)
            # on successful db insert, flash success
            return True
        else:
            # on failed db insert, flash success
            return False

    #------ Read Operation -------- #

    def read_show():

        query = sqlalchemy.text(f'''select "Venue".id, "Venue".name, "Artist".id, "Artist".name,"Artist".image_link, "Showing".start_time from "Showing" join "Artist" on "Artist".id = "Showing".artist_id join "Venue" on "Venue".id = "Showing".venue_id''')
        query_result = db.engine.execute(query)
        fetch_data = query_result.fetchall()

        data = []
        for i in range(0, len(fetch_data)):
            test_data = {
            'venue_id': fetch_data[i][0],
            'venue_name': fetch_data[i][1],
            'artist_id': fetch_data[i][2],
            'artist_name': fetch_data[i][3],
            'artist_image_link': fetch_data[i][4],
            'start_time': fetch_data[i][5]
            }
            data.append(test_data)
        return data