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

class Movies(Resource):
  def get(self):
			conn = mysql.connect()
			cursor = conn.cursor(pymysql.cursors.DictCursor)
			cursor.execute("SELECT id id, name name, movieformat_id movieformat_id, movietype_id movietype_id, duration duration, country_code country_code, start_date start_date, end_date end_date, image image, note note, description description from movies")
			rows = cursor.fetchall()
			resp = jsonify(rows)
			resp.status_code = 200
			return resp