import pymysql
import json
from app import app
from flask import jsonify
from flask import flash, request
from flask_restful import Resource, Api
from flaskext.mysql import MySQL
from datetime import date, timedelta
from time import mktime

mysql = MySQL()
 
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'mtb_db'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
# app.config['MYSQL_DATABASE_USER'] = 'ducvinh26091997'
# app.config['MYSQL_DATABASE_PASSWORD'] = 'ducvinh26091997'
# app.config['MYSQL_DATABASE_DB'] = 'mtb_admin'
# app.config['MYSQL_DATABASE_HOST'] = 'db4free.net'
mysql.init_app(app)


class apiMovies(Resource):
  def get(self):
			conn = mysql.connect()
			cursor = conn.cursor(pymysql.cursors.DictCursor)
			cursor.execute("SELECT id id, name name, movieformat_id movieformat_id, movietype_id movietype_id, duration duration, country_code country_code, start_date start_date, end_date end_date, image image, note note, description description, rate rate from movies")
			rows = cursor.fetchall()
			resp = jsonify(rows)
			resp.status_code = 200
			return resp

class apiMovieDetail(Resource):
  def get(self, id):
			conn = mysql.connect()
			cursor = conn.cursor(pymysql.cursors.DictCursor)
			cursor.execute("SELECT id id, name name, movieformat_id movieformat_id, movietype_id movietype_id, duration duration, country_code country_code, start_date start_date, end_date end_date, image image, note note, description description, rate rate, director director, actors actors, url_video1 url_video1, url_video2 url_video2, image1 image1, image2 image2, age_limit age_limit from movies WHERE id=%s",id)
			rows = cursor.fetchall()
			resp = jsonify(rows)
			resp.status_code = 200
			return resp

class apiMovieDetailDate(Resource):
  def get(self, id):
			conn = mysql.connect()
			cursor = conn.cursor(pymysql.cursors.DictCursor)
			sql="SELECT DISTINCT showtime FROM showings WHERE movie_id=%s AND showtime >= CURDATE() ORDER BY showtime ASC"
			data=(id)
			cursor.execute(sql, data)
			rows = cursor.fetchall()
			resp = jsonify(rows)
			resp.status_code = 200
			return resp

class apiMovieDetailTime(Resource):
  def get(self, id):
			conn = mysql.connect()
			cursor = conn.cursor(pymysql.cursors.DictCursor)
			# sql=""
			# data=(id)
			cursor.execute("SELECT id id, movie_id movie_id, room_id room_id, showtime showtime, time time from showings WHERE movie_id=%s AND CAST(time AS time)>=CAST(CONVERT_TZ(NOW(),'+00:00','+07:00') AS time) ORDER BY time ASC",id)
			rows = cursor.fetchall()
			resp = jsonify(rows)
			resp.status_code = 200
			return resp
