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

class apiTicketByMember(Resource):
  def get(self, username):
			conn = mysql.connect()
			cursor = conn.cursor(pymysql.cursors.DictCursor)
			cursor.execute("SELECT time time, room_name room_name, seats seats, name name, price price, create_at create_at FROM tickets INNER JOIN movies on movies.id=tickets.movie_id INNER JOIN rooms on rooms.id=tickets.room_id INNER JOIN showings on showings.id=tickets.showing_id WHERE username=%s",username)
			rows = cursor.fetchall()
			resp = jsonify(rows)
			resp.status_code = 200
			return resp