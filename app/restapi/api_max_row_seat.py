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
# app.config['MYSQL_DATABASE_USER'] = 'ducvinh26091997'
# app.config['MYSQL_DATABASE_PASSWORD'] = 'ducvinh26091997'
# app.config['MYSQL_DATABASE_DB'] = 'mtb_admin'
# app.config['MYSQL_DATABASE_HOST'] = 'db4free.net'
mysql.init_app(app)

class apiMaxRowSeat(Resource):
  def get(self, id):
			conn = mysql.connect()
			cursor = conn.cursor(pymysql.cursors.DictCursor)
			cursor.execute("SELECT max_row_seat max_row_seat, max_seat_row max_seat_row FROM rooms WHERE id=%s",id)
			rows = cursor.fetchall()
			resp = jsonify(rows)
			resp.status_code = 200
			return resp