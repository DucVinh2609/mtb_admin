import pymysql
from app import app
from flask import jsonify
from flask import flash, request
from flask_restful import Resource, Api
from flaskext.mysql import MySQL

mysql = MySQL()
 
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'mtb_db'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

class apiMovies(Resource):
  def get(self):
			conn = mysql.connect()
			cursor = conn.cursor(pymysql.cursors.DictCursor)
			cursor.execute("SELECT id id, name name, movieformat_id movieformat_id, movietype_id movietype_id, duration duration, country_code country_code, start_date start_date, end_date end_date, image image, note note, description description from movies")
			rows = cursor.fetchall()
			resp = jsonify(rows)
			resp.status_code = 200
			return resp

class apiMovieDetail(Resource):
  def get(self, id):
			conn = mysql.connect()
			cursor = conn.cursor(pymysql.cursors.DictCursor)
			cursor.execute("SELECT id id, name name, movieformat_id movieformat_id, movietype_id movietype_id, duration duration, country_code country_code, start_date start_date, end_date end_date, image image, note note, description description from movies WHERE id=%s",id)
			rows = cursor.fetchall()
			resp = jsonify(rows)
			resp.status_code = 200
			return resp

class apiMovieDetailDate(Resource):
  def get(self, id):
			conn = mysql.connect()
			cursor = conn.cursor(pymysql.cursors.DictCursor)
			sql="SELECT id id, movie_id movie_id, room_id room_id, showtime showtime from showings WHERE movie_id=%s GROUP BY showtime ORDER BY showtime DESC"
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
			cursor.execute("SELECT id id, movie_id movie_id, room_id room_id, showtime showtime from showings WHERE movie_id=%s",id)
			rows = cursor.fetchall()
			resp = jsonify(rows)
			resp.status_code = 200
			return resp
