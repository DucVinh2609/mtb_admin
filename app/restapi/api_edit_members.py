import pymysql
import json
from app import app
from flask import jsonify,session
from flask import flash, request
from flask_restful import Resource, Api
from flaskext.mysql import MySQL
from datetime import date, timedelta, datetime
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

class apiEditMembers(Resource):
  def post(self, username):
    _json = request.json
    _fullname = _json['fullname']
    _birthday = _json['birthday']
    _address = _json['address']
    _phone = _json['phone']
    _gender = _json['gender']
    _birthday = datetime.strptime(_birthday, '%Y-%m-%d').date()
		# validate the received values
    if _fullname and _birthday and _address and _phone and _gender and username and request.method == 'POST':
			# save edits
      sql = "UPDATE members SET fullname=%s, birthday=%s, address=%s, phone=%s, gender=%s WHERE username=%s"
      data = (_fullname, _birthday, _address, _phone, _gender, username,)
      conn = mysql.connect()
      cursor = conn.cursor()
      cursor.execute(sql, data)
      conn.commit()
      resp = jsonify('Member updated successfully!')
      resp.status_code = 200
      return resp