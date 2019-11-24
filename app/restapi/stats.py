from flask import Flask, request
from flask_restful import Resource, Api
from json import dumps
from flask_jsonpify import jsonify
from flaskext.mysql import MySQL

app = Flask(__name__)
api = Api(app)
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'mtb_db'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
conn = mysql.connect()

class Tracks(Resource):
  def get(self):
    query = conn.execute("SELECT id, name FROM movieformats;")
    result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
    return jsonify(result)

api.add_resource(Tracks, '/tracks')

if __name__ == '__main__':
  app.run()