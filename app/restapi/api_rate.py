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


class apiAddRate(Resource):
  def post(self, username, movie_id, rate):
			if request.method == 'POST':
				sql = "INSERT INTO rates(movie_id, member_username, rate) VALUES(%s, %s, %s)"
				data = (movie_id, username, rate,)
				conn = mysql.connect()
				cursor = conn.cursor()
				cursor.execute(sql, data)
				conn.commit()
				resp = jsonify('User added rates!')
				resp.status_code = 200
				return resp


class apiListRateMember(Resource):
  def get(self, username, movie_id):
			if request.method == 'GET':
				conn = mysql.connect()
				cursor = conn.cursor(pymysql.cursors.DictCursor)
				cursor.execute("SELECT d.id id, d.rate rate FROM rates d INNER JOIN movies v ON v.id=d.movie_id WHERE member_username=%s AND movie_id=%s", (username, movie_id,))
				rows = cursor.fetchall()
				resp = jsonify(rows)
				resp.status_code = 200
				return resp

class apiDeleteRate(Resource):
  def delete(self, id):
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute("DELETE FROM rates WHERE id=%s", (id,))
			conn.commit()
			resp = jsonify('Rate deleted successfully!')
			resp.status_code = 200
			return resp

class apiListRateMovie(Resource):
  def get(self, movie_id):
			if request.method == 'GET':
				conn = mysql.connect()
				cursor = conn.cursor(pymysql.cursors.DictCursor)
				cursor.execute("SELECT d.id id, v.rate rate FROM rates d INNER JOIN movies v ON v.id=d.movie_id WHERE movie_id=%s", (movie_id,))
				rows = cursor.fetchall()
				resp = jsonify(rows)
				resp.status_code = 200
				return resp

class apiEditRateMovie(Resource):
  def put(self, movie_id, rate):
			if request.method == 'PUT':
				sql = "UPDATE movies SET rate=%s WHERE id=%s"
				data = (rate, movie_id,)
				conn = mysql.connect()
				cursor = conn.cursor()
				cursor.execute(sql, data)
				conn.commit()
				resp = jsonify('Movie rate updated successfully!')
				resp.status_code = 200
				return resp