import pymysql
from app import app
from flask import jsonify
from flask import flash, request
from werkzeug import generate_password_hash, check_password_hash
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

class apiMovieFormats(Resource):
  def get(self):
			conn = mysql.connect()
			cursor = conn.cursor(pymysql.cursors.DictCursor)
			cursor.execute("SELECT id id, name name FROM movieformats")
			rows = cursor.fetchall()
			resp = jsonify(rows)
			resp.status_code = 200
			return resp

class apiAddMovieFormats(Resource):
  def post(self):
			id = request.json['id']
			name = request.json['name']
			# validate the received values
			if id and name and request.method == 'POST':
				# save edits
				sql = "INSERT INTO movieformats(id, name) VALUES(%s, %s)"
				data = (id, name,)
				conn = mysql.connect()
				cursor = conn.cursor()
				cursor.execute(sql, data)
				conn.commit()
				resp = jsonify('User added successfully!')
				resp.status_code = 200
				return resp

class apiEditMovieFormats(Resource):
  def put(self, id):
			_json = request.json
			_name = _json['name']	
			# validate the received values
			if _name and id and request.method == 'PUT':
				# save edits
				sql = "UPDATE movieformats SET name=%s WHERE id=%s"
				data = (_name, id,)
				conn = mysql.connect()
				cursor = conn.cursor()
				cursor.execute(sql, data)
				conn.commit()
				resp = jsonify('User updated successfully!')
				resp.status_code = 200
				return resp

class apiDeleteMovieFormats(Resource):
  def delete(self, id):
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute("DELETE FROM movieformats WHERE id=%s", (id,))
			conn.commit()
			resp = jsonify('User deleted successfully!')
			resp.status_code = 200
			return resp
