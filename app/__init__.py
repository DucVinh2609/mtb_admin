import os

from flask            import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login      import LoginManager
from flask_bcrypt     import Bcrypt
from flask_ckeditor   import CKEditor
from flask_restful     import Api
from flask_cors import CORS
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
ckeditor = CKEditor(app)
api = Api(app) # flask_restful
app.config.from_object('app.configuration.Config')

db = SQLAlchemy  (app) # flask-sqlalchemy
bc = Bcrypt      (app) # flask-bcrypt

lm = LoginManager(   ) # flask-loginmanager
lm.init_app(app) # init the login manager

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

from app import views, models
from app.restapi.demo.main import apiMovieFormats, apiAddMovieFormats, apiEditMovieFormats, apiDeleteMovieFormats
from app.restapi.api_movies import apiMovies, apiMovieDetail, apiMovieDetailDate, apiMovieDetailTime
from app.restapi.api_showtime_by_idmovie import apiShowtimeByIdmovie
from app.restapi.apiMovieBest import apiBestMovies
from app.restapi.api_login import apiLogin
from app.restapi.api_max_row_seat import apiMaxRowSeat
from app.restapi.api_seat_was_booked import apiSeatWasBooked
from app.restapi.api_tickets import apiAddTickets
from app.restapi.api_rate import apiAddRate
from app.restapi.api_edit_members import apiEditMembers
from app.restapi.api_ticket_member import apiTicketByMember
# from app.restapi.apiMovieDetail import apiMovieDetail

# Inject REST api 
api.add_resource(apiMovieFormats, '/api/demo')
api.add_resource(apiAddMovieFormats, '/api/demo/add')
api.add_resource(apiEditMovieFormats, '/api/demo/edit/<int:id>')
api.add_resource(apiDeleteMovieFormats, '/api/demo/delete/<int:id>')
api.add_resource(apiMovies, '/api/list_movies')
api.add_resource(apiShowtimeByIdmovie, '/api/api_showtime_by_idmovie/<int:id>')
api.add_resource(apiBestMovies, '/api/best_movies')
api.add_resource(apiMovieDetail, '/api/movie_detail/<int:id>')
api.add_resource(apiMovieDetailDate, '/api/movie_detail_date/<int:id>')
api.add_resource(apiMovieDetailTime, '/api/movie_detail_time/<int:id>')
api.add_resource(apiLogin, '/api/login/<string:username>/<string:password>')
api.add_resource(apiMaxRowSeat, '/api/max_row_seat/<int:id>')
api.add_resource(apiSeatWasBooked, '/api/seat_was_booked/<int:id>')
api.add_resource(apiAddTickets, '/api/add_tickets')
api.add_resource(apiAddRate, '/api/rate/<string:username>/<int:movie_id>/<int:rate>')
api.add_resource(apiEditMembers, '/api/member/edit/<string:username>')
api.add_resource(apiTicketByMember, '/api/watchlist/<string:username>')