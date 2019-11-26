import os

from flask            import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login      import LoginManager
from flask_bcrypt     import Bcrypt

from flask_restful     import Api

# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

api = Api(app) # flask_restful

app.config.from_object('app.configuration.Config')

db = SQLAlchemy  (app) # flask-sqlalchemy
bc = Bcrypt      (app) # flask-bcrypt

lm = LoginManager(   ) # flask-loginmanager
lm.init_app(app) # init the login manager

from app import views, models
from app.restapi.demo.main import apiMovieFormats, apiAddMovieFormats, apiEditMovieFormats, apiDeleteMovieFormats
from app.restapi.api_movies import apiMovies
from app.restapi.api_showtime_by_idmovie import apiShowtimeByIdmovie

# Inject REST api 
api.add_resource(apiMovieFormats, '/api/demo')
api.add_resource(apiAddMovieFormats, '/api/demo/add')
api.add_resource(apiEditMovieFormats, '/api/demo/edit/<int:id>')
api.add_resource(apiDeleteMovieFormats, '/api/demo/delete/<int:id>')
api.add_resource(apiMovies, '/api/list_movies')
api.add_resource(apiShowtimeByIdmovie, '/api/api_showtime_by_idmovie/<int:id>')
