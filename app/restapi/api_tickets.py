import pymysql
from app import app
from flask import jsonify
from flask import flash, request
from flask_restful import Resource, Api
from flaskext.mysql import MySQL
from datetime import date, timedelta, datetime
from flask_mail import Mail, Message
from flask_qrcode import QRcode
import pyqrcode
mysql = MySQL()

qrcode = QRcode(app)
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

app.config['DEBUG'] = True 
app.config['TESTING'] = False 
app.config['MAIL_SERVER'] = 'smtp.gmail.com' 
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False 
# app.config['MAIL_DEBUG'] = True
app.config['MAIL_USERNAME'] = 'ducvinhnguyen2609@gmail.com'
app.config['MAIL_PASSWORD'] = 'Ducvinh26091997' 
app.config['MAIL_DEFAULT_SENDER'] = 'ducvinhnguyen2609@gmail.com'
app.config['MAIL_MAX_EMAILS'] = None
# app.config['MAIL_SUPPRESS_SEND'] = False
app.config['MAIL_ASCII_ATTACHMENTS'] = False

mail = Mail(app)

class apiAddTickets(Resource):
  def post(self):
      showing_id = request.json['showing_id']
      seats = request.json['seats']
      price = request.json['price']
      movie_id = request.json['movie_id']
      room_id = request.json['room_id']
      username = request.json['username']
      event_id = request.json['event_id']
      unitprice = request.json['unitprice']
      if username == "no":
        gmail = request.json['gmail']
      today= str(datetime.today().strftime("%Y-%m-%d"))
      create_at = datetime.strptime(today, '%Y-%m-%d').date()
      # validate the received values
      if request.method == 'POST':
				# save edits
        sql = "INSERT INTO tickets (showing_id, room_id, username, event_id, unitprice, seats, movie_id, price, create_at) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        data = (showing_id, room_id, username, event_id, unitprice, seats, movie_id, price, create_at,)
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sql, data)
        conn.commit()
        cursor1 = conn.cursor()
        cursor1.execute("SELECT name from movies WHERE id=%s",movie_id)
        movie = cursor1.fetchone()
        cursor2 = conn.cursor()
        cursor2.execute("SELECT room_name from rooms WHERE id=%s",room_id)
        room = cursor2.fetchone()
        cursor2 = conn.cursor()
        cursor2.execute("SELECT showtime, time from showings WHERE id=%s",showing_id)
        showing = cursor2.fetchone()
        cursor3 = conn.cursor()
        cursor3.execute("SELECT MAX(id) as LastID FROM tickets")
        lastticket = cursor3.fetchone()
        if username != "no":
          cursor4 = conn.cursor()
          cursor4.execute("SELECT email FROM tickets d INNER JOIN members v ON v.username = d.username WHERE d.id=%s",lastticket[0])
          email = cursor4.fetchone()
        link_to_post = "Movie: %s" % str(movie[0])+"\r\nRooms: %s" % str(room[0])+"\r\nShowings: %s" % str(showing[1])+" * %s" % str(showing[0].strftime("%d-%m-%Y"))+"\r\nSeats: %s" % seats
        url = pyqrcode.create(link_to_post, encoding="utf-8")
        url.png('app/static/assets/img/qrcode/'+str(lastticket[0])+'.png', scale=8)
        if username != "no":
          msg = Message('Booking ticket successful!', recipients=[str(email[0])])
        else:
          msg = Message('Booking ticket successful!', recipients=[gmail])
        msg.html = '<b>Confirm successful booking ticket!</b><br><br>You have successfully booked a ticket with the following ticket information: <br>Movies: '+str(movie[0])+'<br>Rooms: '+str(room[0])+'<br>Showings: '+str(showing[1])+' * '+str(showing[0].strftime("%d-%m-%Y"))+'<br>Seats: '+seats+'<br><div><img style="heigh: 200px; width: 200px;" src="http://localhost:5000/static/assets/img/qrcode/'+str(lastticket[0])+'.png"></div>'
        mail.send(msg)
        resp = jsonify([{"movie": str(movie[0]), "seats": seats, "price": price, "rooms": str(room[0]), "showings": str(showing[1]), "date": str(showing[0].strftime("%d-%m-%Y"))}])
        resp.status_code = 200
        return resp