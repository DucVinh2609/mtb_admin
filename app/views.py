from flask               import render_template, request, url_for, redirect, send_from_directory, jsonify, session
from flask_login         import login_user, logout_user, current_user, login_required
from werkzeug.exceptions import HTTPException, NotFound, abort
from flask_restful import Resource, Api
from datetime import date, timedelta, datetime
from time import mktime
from dateutil.parser import parse
from flask_wtf import Form
from wtforms.fields.html5 import DateField
from wtforms import StringField
from werkzeug.utils import secure_filename

import os, logging 

from app        import app, lm, db, bc
from app.models import User
from app.forms  import LoginForm, RegisterForm, AddMovietypesForm, EditMovietypesForm, AddMovieFormatsForm, EditMovieFormatsForm, AddRolesForm, EditRolesForm, AddEmployeesForm, EditEmployeesForm, AddCountriesForm, EditCountriesForm, AddMoviesForm, EditMoviesForm, AddSeattypesForm, EditSeattypesForm, AddRoomformatsForm, EditRoomformatsForm, AddRoomsForm, EditRoomsForm, AddStatusForm, EditStatusForm, EditPassForm
from flaskext.mysql import MySQL

UPLOAD_FOLDER = 'D:/python/heroku/mtb-admin/app/static/assets/img/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

api = Api(app)
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'mtb_db'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
# app.config['MYSQL_DATABASE_USER'] = 'ducvinh26091997'
# app.config['MYSQL_DATABASE_PASSWORD'] = 'ducvinh26091997'
# app.config['MYSQL_DATABASE_DB'] = 'mtb_admin'
# app.config['MYSQL_DATABASE_HOST'] = 'db4free.net'
mysql.init_app(app)

tvalue= str(datetime.today().strftime("%Y-%m-%d"))
today = datetime.strptime(tvalue, '%Y-%m-%d').date()
class Database:
  def __init__(self):
    self.con = mysql.connect()
    self.cur = self.con.cursor()
  def list_movietypes(self):
    self.cur.execute("SELECT id, name from movietypes")
    result = self.cur.fetchall()
    return result
  def list_movieformats(self):
    self.cur.execute("SELECT id, name from movieformats")
    result = self.cur.fetchall()
    return result
  def list_roles(self):
    self.cur.execute("SELECT id, role_name from roles")
    result = self.cur.fetchall()
    return result
  def list_employees(self):
    self.cur.execute("SELECT username, fullname, birthday, address, phone, gender, role_name, avatar from employees INNER JOIN roles ON employees.role_id = roles.id ")
    result = self.cur.fetchall()
    return result
  def list_countries(self):
    self.cur.execute("SELECT country_code, country from countries")
    result = self.cur.fetchall()
    return result
  def list_movies(self):
    self.cur.execute("SELECT id, name, movieformat_id, movietype_id, duration, country_code, start_date, end_date, image, note, description from movies")
    result = self.cur.fetchall()
    return result
  def list_seattypes(self):
    self.cur.execute("SELECT id, seattype_name from seattypes")
    result = self.cur.fetchall()
    return result
  def list_roomformats(self):
    self.cur.execute("SELECT id, name from roomformats")
    result = self.cur.fetchall()
    return result
  def list_rooms(self):
    self.cur.execute("SELECT id, room_name, roomformat_id, status, max_row_seat, max_seat_row, note from rooms")
    result = self.cur.fetchall()
    return result
  def list_status(self):
    self.cur.execute("SELECT id, seat_condition from status")
    result = self.cur.fetchall()
    return result
  def list_showings(self):
    self.cur.execute("SELECT room_id, time, showtime, showings.id, movie_id, movies.name, duration from showings INNER JOIN movies ON showings.movie_id = movies.id ORDER BY time ASC")
    result = self.cur.fetchall()
    return result
  def count_member(self):
    self.cur.execute("SELECT COUNT(username) from members")
    result = self.cur.fetchone()
    return result
  def total_sale(self):
    self.cur.execute("SELECT price, create_at from tickets")
    result = self.cur.fetchall()
    return result
  def seat_on_room(self):
    self.cur.execute("SELECT max_row_seat, max_seat_row, id from rooms")
    result = self.cur.fetchall()
    return result
  def count_showing(self):
    self.cur.execute("SELECT room_id FROM showings WHERE showtime=%s",today)
    result = self.cur.fetchall()
    return result
  def seat_booked_day(self):
    self.cur.execute("SELECT price, unitprice FROM tickets d INNER JOIN showings v ON v.id = d.showing_id WHERE v.showtime=%s",today)
    result = self.cur.fetchall()
    return result
  def ticket_purchase(self):
    self.cur.execute("SELECT username FROM tickets")
    result = self.cur.fetchall()
    return result
@app.route('/sitemap.xml')
def sitemap():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'sitemap.xml')

@app.route('/googlee35aa2f2fd7b0c5b.html')
def google():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'googlee35aa2f2fd7b0c5b.html')

@app.route('/print')
def printMsg():
    app.logger.warning('testing warning log')
    app.logger.error('testing error log')
    app.logger.info('testing info log')
    return "Check your console"

# provide login manager with load_user callback
@lm.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# authenticate user
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('username', None)
    session.pop('avatar', None)
    # Redirect to login page
    return redirect(url_for('login'))

# register user
@app.route('/register.html', methods=['GET', 'POST'])
def register():
    
    # declare the Registration Form
    form = RegisterForm(request.form)

    msg = None

    if request.method == 'GET': 

        return render_template('layouts/auth-default.html',
                                content=render_template( 'pages/register.html', form=form, msg=msg ) )

    # check if both http method is POST and form is valid on submit
    if form.validate_on_submit():

        # assign form data to variables
        username = request.form.get('username', '', type=str)
        password = request.form.get('password', '', type=str) 
        email    = request.form.get('email'   , '', type=str) 

        # filter User out of database through username
        user = User.query.filter_by(user=username).first()

        # filter User out of database through username
        user_by_email = User.query.filter_by(email=email).first()

        if user or user_by_email:
            msg = 'Error: User exists!'
        
        else:         

            pw_hash = password #bc.generate_password_hash(password)

            user = User(username, email, pw_hash)

            user.save()

            msg = 'User created, please <a href="' + url_for('login') + '">login</a>'     

    else:
        msg = 'Input error'     

    return render_template('layouts/auth-default.html',
                            content=render_template( 'pages/register.html', form=form, msg=msg ) )

# authenticate user
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    msg = None

    if form.validate_on_submit():
      username = request.form.get('username', '', type=str)
      password = request.form.get('password', '', type=str) 
      conn = mysql.connect()
      cursor = conn.cursor()
      cursor.execute("SELECT * from employees where username='" + username + "' and password='" + password + "'")
      account = cursor.fetchone()
      if account:
        session['loggedin'] = True
        session['username'] = account[0]
        session['avatar'] = account[8]
        return redirect('/home')
      else:
        msg = "Username or Password is wrong"
    return render_template('layouts/auth-default.html', content=render_template( 'pages/login.html', form=form, msg=msg ) )

# Profile
@app.route('/profile')
def profile():
    # Check if user is loggedin
    if 'loggedin' in session:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM employees WHERE username = %s', [session['username']])
        account = cursor.fetchone()
        return render_template('layouts/default.html', content=render_template( 'pages/profile.html', account=account, username=session['username'], avatar=session['avatar'] ) )
    return redirect(url_for('login'))

@app.route('/icons.html')
def icons():

    return render_template('layouts/default.html',
                            content=render_template( 'pages/icons.html') )

# Settings
@app.route('/settings')
def settings():
  try:
    form = EditEmployeesForm(request.form)
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT username, fullname, birthday, address, phone, gender, role_id, avatar, about from employees WHERE username=%s", session['username'])
    row = cursor.fetchone()
    if row:
      return render_template('layouts/default.html', content=render_template( 'pages/settings.html', form=form, row=row, username=session['username'], avatar=session['avatar']))
    else:
      return 'Error loading #{username}'.format(username=username)
  except Exception as e:
    print(e)
  finally:
    cursor.close() 
    conn.close()

# Change password
@app.route('/change-password')
def password():
  form = EditPassForm(request.form)
  msg = None
  conn = mysql.connect()
  cursor = conn.cursor()
  cursor.execute("SELECT password FROM employees WHERE username=%s", session['username'])
  row = cursor.fetchone()
  return render_template('layouts/default.html', content=render_template( 'pages/change-password.html', row=row, form=form, msg=msg, username=session['username'], avatar=session['avatar']))

@app.route('/password/update/<string:new_password>')
def update_password(new_password):
  try:
      sql = "UPDATE employees SET password=%s WHERE username=%s"
      data = (new_password, session['username'],)
      conn = mysql.connect()
      cursor = conn.cursor()
      cursor.execute(sql, data)
      conn.commit()
      return redirect('/profile')
  except Exception as e:
    print(e)
  finally:
    cursor.close() 
    conn.close()

# Render the tables page
@app.route('/tables.html')
def tables():

    return render_template('layouts/default.html',
                            content=render_template( 'pages/tables.html') )

# App main route + generic routing
@app.route('/home')
def home():
    def db_query():
      db = Database()
      emps = db.count_member()
      return emps
    countmember = db_query()
    def db_query2():
      db = Database()
      emps = db.seat_on_room()
      return emps
    total_seat_room = db_query2()
    def db_query3():
      db = Database()
      emps = db.count_showing()
      return emps
    showing = db_query3()
    def db_query4():
      db = Database()
      emps = db.seat_booked_day()
      return emps
    seat_booked = db_query4()
    def db_query5():
      db = Database()
      emps = db.ticket_purchase()
      return emps
    ticket_purchase_form = db_query5()
    def db_query1():
      db = Database()
      emps = db.total_sale()
      return emps
    sale = db_query1()
    by_member = 0
    no_by_member = 0
    for row in ticket_purchase_form:
      if row[0]=="no":
        no_by_member += 1
      else:
        by_member += 1
    ratio = round((by_member/(no_by_member + by_member))*100,2)
    unratio = round(100-ratio,2)
    total = 0
    sale_may = 0
    sale_jun = 0
    sale_jul = 0
    sale_aug = 0
    sale_sep = 0
    sale_oct = 0
    sale_nov = 0
    sale_dec = 0
    for row in sale:
      total += int(row[0])
    for row in sale:
      if row[1].month==5:
        sale_may += row[0]
      elif row[1].month==6:
        sale_jun += row[0]
      elif row[1].month==7:
        sale_jul += row[0]
      elif row[1].month==8:
        sale_aug += row[0]
      elif row[1].month==9:
        sale_sep += row[0]
      elif row[1].month==10:
        sale_oct += row[0]
      elif row[1].month==11:
        sale_nov += row[0]
      elif row[1].month==12:
        sale_dec += row[0]
    total_seat_day = 0
    for row in showing:
      for row1 in total_seat_room:
        if row[0]==row1[2]:
            total_seat_day +=  int(row1[0])*int(row1[1])
    total_seat_booked_day = 0
    for row in seat_booked:
      total_seat_booked_day += int(row[0])/int(row[1])
    try:
      performance = round((total_seat_booked_day/total_seat_day)*100,2)
    except ZeroDivisionError:
      performance = 0
    # Check if user is loggedin
    if 'loggedin' in session:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM employees WHERE username = %s', [session['username']])
        account = cursor.fetchone()
        cursor1 = conn.cursor()
        cursor1.execute('SELECT * FROM members ORDER BY create_at DESC LIMIT 5')
        member = cursor1.fetchall()
        cursor2 = conn.cursor()
        cursor2.execute('SELECT COUNT(id) FROM tickets WHERE MONTH(create_at)=7')
        jul = cursor2.fetchone()
        cursor3 = conn.cursor()
        cursor3.execute('SELECT COUNT(id) FROM tickets WHERE MONTH(create_at)=8')
        aug = cursor3.fetchone()
        cursor4 = conn.cursor()
        cursor4.execute('SELECT COUNT(id) FROM tickets WHERE MONTH(create_at)=9')
        sep = cursor4.fetchone()
        cursor5 = conn.cursor()
        cursor5.execute('SELECT COUNT(id) FROM tickets WHERE MONTH(create_at)=10')
        oct = cursor5.fetchone()
        cursor6 = conn.cursor()
        cursor6.execute('SELECT COUNT(id) FROM tickets WHERE MONTH(create_at)=11')
        nov = cursor6.fetchone()
        cursor7 = conn.cursor()
        cursor7.execute('SELECT COUNT(id) FROM tickets WHERE MONTH(create_at)=12')
        dec = cursor7.fetchone()
        return render_template('layouts/default.html', content=render_template( 'pages/index.html', account=account, jul=jul, aug=aug, sep=sep, oct=oct, nov=nov, dec=dec, sale_may=sale_may, sale_jun=sale_jun, sale_jul=sale_jul, sale_aug=sale_aug, sale_sep=sale_sep, sale_oct=sale_oct, sale_nov=sale_nov, sale_dec=sale_dec, member=member, username=session['username'], avatar=session['avatar'], countmember=countmember, total=total, performance=performance, by_member=by_member, no_by_member=no_by_member, ratio=ratio, unratio=unratio))
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

@app.route('/<path>')
def index(path):

    content = None

    try:
      if 'loggedin' in session:
          conn = mysql.connect()
          cursor = conn.cursor()
          cursor.execute('SELECT * FROM employees WHERE username = %s', [session['username']])
          account = cursor.fetchone()
          return render_template('layouts/default.html', account=account,
                                content=render_template( 'pages/'+path) )
      # User is not loggedin redirect to login page
      return redirect(url_for('login'))
    except:
        
        return render_template('layouts/auth-default.html',
                                content=render_template( 'pages/404.html' ) )

# Movie Types

@app.route('/movietypes')
def movietypes():
  def db_query():
    db = Database()
    emps = db.list_movietypes()
    return emps
  res = db_query()
  logger = logging.getLogger('example_logger')
  logger.warning(res)
  return render_template('layouts/default.html', content=render_template( 'pages/movietypes/index.html',result=res, content_type='application/json', username=session['username'], avatar=session['avatar']))

@app.route('/new_movietypes')
def add_movietypes():
  form = AddMovietypesForm(request.form)
  msg = None
  return render_template('layouts/default.html', content=render_template( 'pages/movietypes/new.html', form=form, msg=msg, username=session['username'], avatar=session['avatar']))

@app.route('/movietypes/add', methods=['POST'])
def addMovietypes():
  try:
    form = AddMovietypesForm(request.form)
    msg = None
    id = request.form.get('id', '', type=int)
    name = request.form.get('name', '', type=str)        
    if id and name and request.method == 'POST':
      sql = "INSERT INTO movietypes (id, name) VALUES(%s, %s)"
      data = (id, name,)
      conn = mysql.connect()
      cursor = conn.cursor()
      cursor.execute(sql, data)
      conn.commit()
      return redirect('/movietypes')
    else:
      return redirect('/new_movietypes')
  except Exception as e:
    print(e)
	
  finally:
    cursor.close()
    conn.close()

@app.route('/movietypes/delete/<int:id>')
def delete_movietypes(id):
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute("DELETE FROM movietypes WHERE id=%s", (id,))
		conn.commit()
		return redirect('/movietypes')
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()

@app.route('/edit_movietypes/<int:id>')
def edit_movietypes(id):
  try:
    form = EditMovietypesForm(request.form)
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM movietypes WHERE id=%s", id)
    row = cursor.fetchone()
    if row:
      logger = logging.getLogger('example_logger')
      logger.warning(row)  
      return render_template('layouts/default.html', content=render_template( 'pages/movietypes/edit.html', form=form, row=row, username=session['username'], avatar=session['avatar']))
    else:
      return 'Error loading #{id}'.format(id=id)
  except Exception as e:
    print(e)
  finally:
    cursor.close() 
    conn.close()

@app.route('/movietypes/update', methods=['POST'])
def update_movietypes():
  try:		
    form = EditMovietypesForm(request.form)
    msg = None
    id = request.form.get('id', '', type=int)
    name = request.form.get('name', '', type=str)
    if name and id and request.method == 'POST':
      sql = "UPDATE movietypes SET name=%s WHERE id=%s"
      data = (name, id,)
      conn = mysql.connect()
      cursor = conn.cursor()
      cursor.execute(sql, data)
      conn.commit()
      return redirect('/movietypes')
    else:
      return redirect('/edit_movietypes/%s',id)
  except Exception as e:
    print(e)
  finally:
    cursor.close() 
    conn.close()

# Movie Formats

@app.route('/movieformats')
def movieformats():
  def db_query():
    db = Database()
    emps = db.list_movieformats()
    return emps
  res = db_query()
  logger = logging.getLogger('example_logger')
  logger.warning(res)
  return render_template('layouts/default.html', content=render_template( 'pages/movieformats/index.html',result=res, content_type='application/json', username=session['username'], avatar=session['avatar']))

@app.route('/new_movieformats')
def add_movieformats():
  form = AddMovieFormatsForm(request.form)
  msg = None
  return render_template('layouts/default.html', content=render_template( 'pages/movieformats/new.html', form=form, msg=msg, username=session['username'], avatar=session['avatar']))

@app.route('/movieformats/add', methods=['POST'])
def addMovieformats():
  try:
    form = AddMovieFormatsForm(request.form)
    msg = None
    id = request.form.get('id', '', type=int)
    name = request.form.get('name', '', type=str)        
    if id and name and request.method == 'POST':
      sql = "INSERT INTO movieformats (id, name) VALUES(%s, %s)"
      data = (id, name,)
      conn = mysql.connect()
      cursor = conn.cursor()
      cursor.execute(sql, data)
      conn.commit()
      return redirect('/movieformats')
    else:
      return redirect('/new_movieformats')
  except Exception as e:
    print(e)
	
  finally:
    cursor.close()
    conn.close()

@app.route('/movieformats/delete/<int:id>')
def delete_movieformats(id):
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute("DELETE FROM movieformats WHERE id=%s", (id,))
		conn.commit()
		return redirect('/movieformats')
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()

@app.route('/edit_movieformats/<int:id>')
def edit_movieformats(id):
  try:
    form = EditMovieFormatsForm(request.form)
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM movieformats WHERE id=%s", id)
    row = cursor.fetchone()
    if row:
      logger = logging.getLogger('example_logger')
      logger.warning(row)  
      return render_template('layouts/default.html', content=render_template( 'pages/movieformats/edit.html', form=form, row=row, username=session['username'], avatar=session['avatar']))
    else:
      return 'Error loading #{id}'.format(id=id)
  except Exception as e:
    print(e)
  finally:
    cursor.close() 
    conn.close()

@app.route('/movieformats/update', methods=['POST'])
def update_movieformats():
  try:		
    form = EditMovieFormatsForm(request.form)
    msg = None
    id = request.form.get('id', '', type=int)
    name = request.form.get('name', '', type=str)
    if name and id and request.method == 'POST':
      sql = "UPDATE movieformats SET name=%s WHERE id=%s"
      data = (name, id,)
      conn = mysql.connect()
      cursor = conn.cursor()
      cursor.execute(sql, data)
      conn.commit()
      return redirect('/movieformats')
    else:
      return redirect('/edit_movieformats/%s',id)
  except Exception as e:
    print(e)
  finally:
    cursor.close() 
    conn.close()


# Roles

@app.route('/roles')
def roles():
  def db_query():
    db = Database()
    emps = db.list_roles()
    return emps
  res = db_query()
  logger = logging.getLogger('example_logger')
  logger.warning(res)
  return render_template('layouts/default.html', content=render_template( 'pages/roles/index.html',result=res, content_type='application/json', username=session['username'], avatar=session['avatar']))

@app.route('/new_roles')
def add_roles():
  form = AddRolesForm(request.form)
  msg = None
  return render_template('layouts/default.html', content=render_template( 'pages/roles/new.html', form=form, msg=msg, username=session['username'], avatar=session['avatar']))

@app.route('/roles/add', methods=['POST'])
def addRoles():
  try:
    form = AddRolesForm(request.form)
    msg = None
    id = request.form.get('id', '', type=int)
    role = request.form.get('role', '', type=str)        
    if id and role and request.method == 'POST':
      sql = "INSERT INTO roles (id, role_name) VALUES(%s, %s)"
      data = (id, role,)
      conn = mysql.connect()
      cursor = conn.cursor()
      cursor.execute(sql, data)
      conn.commit()
      return redirect('/roles')
    else:
      return redirect('/new_roles')
  except Exception as e:
    print(e)
	
  finally:
    cursor.close()
    conn.close()

@app.route('/roles/delete/<int:id>')
def delete_roles(id):
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute("DELETE FROM roles WHERE id=%s", (id,))
		conn.commit()
		return redirect('/roles')
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()

@app.route('/edit_roles/<int:id>')
def edit_roles(id):
  try:
    form = EditRolesForm(request.form)
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT id, role_name FROM roles WHERE id=%s", id)
    row = cursor.fetchone()
    if row:
      logger = logging.getLogger('example_logger')
      logger.warning(row)  
      return render_template('layouts/default.html', content=render_template( 'pages/roles/edit.html', form=form, row=row, username=session['username'], avatar=session['avatar']))
    else:
      return 'Error loading #{id}'.format(id=id)
  except Exception as e:
    print(e)
  finally:
    cursor.close() 
    conn.close()

@app.route('/roles/update', methods=['POST'])
def update_roles():
  try:		
    form = EditRolesForm(request.form)
    msg = None
    id = request.form.get('id', '', type=int)
    role = request.form.get('role', '', type=str)
    if role and id and request.method == 'POST':
      sql = "UPDATE roles SET role_name=%s WHERE id=%s"
      data = (role, id,)
      conn = mysql.connect()
      cursor = conn.cursor()
      cursor.execute(sql, data)
      conn.commit()
      return redirect('/roles')
    else:
      return redirect('/edit_roles/%s',id)
  except Exception as e:
    print(e)
  finally:
    cursor.close() 
    conn.close()

# Employees

@app.route('/employees')
def employees():
  def db_query():
    db = Database()
    emps = db.list_employees()
    return emps
  res = db_query()
  return render_template('layouts/default.html', content=render_template( 'pages/employees/index.html',result=res, content_type='application/json', username=session['username'], avatar=session['avatar']))

@app.route('/new_employees')
def add_employees():
  form = AddEmployeesForm(request.form)
  msg = None
  return render_template('layouts/default.html', content=render_template( 'pages/employees/new.html', form=form, msg=msg, username=session['username'], avatar=session['avatar']))

@app.route('/employees/add', methods=['POST'])
def addEmployees():
  try:
    form = AddEmployeesForm(request.form)
    msg = None
    username = request.form.get('username', '', type=str)
    password = request.form.get('password', '', type=str)
    fullname = request.form.get('fullname', '', type=str)
    birthday = request.form.get('birthday', '', type=str)      
    address = request.form.get('address', '', type=str)  
    phone = request.form.get('phone', '', type=str)
    gender = request.form.get('gender', '', type=str)
    role_id = request.form.get('role_id', '', type=int)
    avatar = request.form.get('avatar', '', type=str)
    if username and password and fullname and birthday and address and phone and gender and role_id and avatar and request.method == 'POST':
      sql = "INSERT INTO employees (username, password, fullname, birthday, address, phone, gender, role_id, avatar) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
      data = (username, password, fullname, birthday, address, phone, gender, role_id, avatar,)
      conn = mysql.connect()
      cursor = conn.cursor()
      cursor.execute(sql, data)
      conn.commit()
      return redirect('/employees')
    else:
      return redirect('/new_employees')
  except Exception as e:
    print(e)
	
  finally:
    cursor.close()
    conn.close()

@app.route('/employees/delete/<string:username>')
def delete_employees(username):
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute("DELETE FROM employees WHERE username=%s", (username,))
		conn.commit()
		return redirect('/employees')
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()

@app.route('/edit_employees/<string:username>')
def edit_employees(username):
  try:
    form = EditEmployeesForm(request.form)
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT username, fullname, birthday, address, phone, gender, role_id, avatar, about from employees WHERE username=%s", username)
    row = cursor.fetchone()
    if row:
      return render_template('layouts/default.html', content=render_template( 'pages/employees/edit.html', form=form, row=row, username=session['username'], avatar=session['avatar']))
    else:
      return 'Error loading #{username}'.format(username=username)
  except Exception as e:
    print(e)
  finally:
    cursor.close() 
    conn.close()

@app.route('/employees/update', methods=['POST'])
def update_employees():
  try:		
    form = EditEmployeesForm(request.form)
    msg = None
    username = request.form.get('username', '', type=str)
    fullname = request.form.get('fullname', '', type=str)
    birthday = request.form.get('birthday', '', type=str)      
    address = request.form.get('address', '', type=str)  
    phone = request.form.get('phone', '', type=str)
    gender = request.form.get('gender', '', type=str)
    role_id = request.form.get('role_id', '', type=int)
    about = request.form.get('about', '', type=str)
    if username and fullname and birthday and address and phone and gender and role_id and about and request.method == 'POST':
      sql = "UPDATE employees SET fullname=%s,birthday=%s,address=%s,phone=%s,gender=%s,role_id=%s,about=%s WHERE username=%s"
      data = (fullname, birthday, address, phone, gender, role_id, about, username,)
      conn = mysql.connect()
      cursor = conn.cursor()
      cursor.execute(sql, data)
      conn.commit()
      return redirect('/employees')
    else:
      return redirect('/edit_employees/%s',username)
  except Exception as e:
    print(e)
  finally:
    cursor.close() 
    conn.close()

# Countries

@app.route('/countries')
def countries():
  def db_query():
    db = Database()
    emps = db.list_countries()
    return emps
  res = db_query()
  logger = logging.getLogger('example_logger')
  logger.warning(res)
  return render_template('layouts/default.html', content=render_template( 'pages/countries/index.html',result=res, content_type='application/json', username=session['username'], avatar=session['avatar']))

@app.route('/new_countries')
def add_countries():
  form = AddCountriesForm(request.form)
  msg = None
  return render_template('layouts/default.html', content=render_template( 'pages/countries/new.html', form=form, msg=msg, username=session['username'], avatar=session['avatar']))

@app.route('/countries/add', methods=['POST'])
def addCountries():
  try:
    form = AddCountriesForm(request.form)
    msg = None
    country_code = request.form.get('country_code', '', type=str)
    country = request.form.get('country', '', type=str)        
    if country_code and country and request.method == 'POST':
      sql = "INSERT INTO countries (country_code, country) VALUES(%s, %s)"
      data = (country_code, country,)
      conn = mysql.connect()
      cursor = conn.cursor()
      cursor.execute(sql, data)
      conn.commit()
      return redirect('/countries')
    else:
      return redirect('/new_countries')
  except Exception as e:
    print(e)
	
  finally:
    cursor.close()
    conn.close()

@app.route('/countries/delete/<string:country_code>')
def delete_countries(country_code):
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute("DELETE FROM countries WHERE country_code=%s", (country_code,))
		conn.commit()
		return redirect('/countries')
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()

@app.route('/edit_countries/<string:country_code>')
def edit_countries(country_code):
  try:
    form = EditCountriesForm(request.form)
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT country_code, country FROM countries WHERE country_code=%s", country_code)
    row = cursor.fetchone()
    if row:
      logger = logging.getLogger('example_logger')
      logger.warning(row)  
      return render_template('layouts/default.html', content=render_template( 'pages/countries/edit.html', form=form, row=row, username=session['username'], avatar=session['avatar']))
    else:
      return 'Error loading #{country_code}'.format(country_code=country_code)
  except Exception as e:
    print(e)
  finally:
    cursor.close() 
    conn.close()

@app.route('/countries/update', methods=['POST'])
def update_countries():
  try:		
    form = EditCountriesForm(request.form)
    msg = None
    country_code = request.form.get('country_code', '', type=str)
    country = request.form.get('country', '', type=str)
    if country_code and country and request.method == 'POST':
      sql = "UPDATE countries SET country=%s WHERE country_code=%s"
      data = (country, country_code,)
      conn = mysql.connect()
      cursor = conn.cursor()
      cursor.execute(sql, data)
      conn.commit()
      return redirect('/countries')
    else:
      return redirect('/edit_countries/%s',id)
  except Exception as e:
    print(e)
  finally:
    cursor.close() 
    conn.close()


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Movies

@app.route('/movies')
def movies():
  def db_query():
    db = Database()
    emps = db.list_movies()
    return emps
  res = db_query()
  conn = mysql.connect()
  cursor = conn.cursor()
  cursor.execute("SELECT id, name from movieformats")
  movieformat = cursor.fetchall()
  cursor1 = conn.cursor()
  cursor1.execute("SELECT id, name from movietypes")
  movietype = cursor1.fetchall()
  cursor2 = conn.cursor()
  cursor2.execute("SELECT country_code, country from countries")
  country = cursor2.fetchall()
  return render_template('layouts/default.html', content=render_template( 'pages/movies/index.html',result=res, movieformat=movieformat, movietype=movietype, country=country, content_type='application/json', username=session['username'], avatar=session['avatar']))

@app.route('/new_movies')
def add_movies():
  form = AddMoviesForm(request.form)
  form1 = ExampleForm()
  tvalue= str(datetime.today().strftime("%Y-%m-%d"))
  today = datetime.strptime(tvalue, '%Y-%m-%d').date()
  msg = None
  conn = mysql.connect()
  cursor = conn.cursor()
  cursor.execute("SELECT id, name from movieformats")
  movieformat = cursor.fetchall()
  cursor1 = conn.cursor()
  cursor1.execute("SELECT id, name from movietypes")
  movietype = cursor1.fetchall()
  cursor2 = conn.cursor()
  cursor2.execute("SELECT country_code, country from countries")
  country = cursor2.fetchall()
  return render_template('layouts/default.html', content=render_template( 'pages/movies/new.html', today=today, form=form, form1=form1, movieformat=movieformat, movietype=movietype, country=country, msg=msg, username=session['username'], avatar=session['avatar']))

@app.route('/movies/add', methods=['POST'])
def addMovies():
  try:
    form1 = ExampleForm()
    start_date = str(form1.startDate.data.strftime('%Y-%m-%d'))
    end_date = str(form1.endDate.data.strftime('%Y-%m-%d'))
    movieformat_id = request.form.get('movieformat_id')
    movietype_id = request.form.get('movietype_id')
    country_code = request.form.get('country_code')
    form = AddMoviesForm(request.form)
    msg = None
    name = request.form.get('name', '', type=str)   
    duration = request.form.get('duration', '', type=str)  
    start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
    end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
    note = request.form.get('note', '', type=str)
    description = request.form.get('description')
    if request.method == 'POST':
      file = request.files['image']
      if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        image = "/static/assets/img/uploads/"+filename
        sql = "INSERT INTO movies (name, movieformat_id, movietype_id, duration, country_code, start_date, end_date, image, note, description) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        data = (name, movieformat_id, movietype_id, duration, country_code, start_date, end_date, image, note, description,)
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sql, data)
        conn.commit()
        return redirect('/movies')
    else:
      return redirect('/new_movies')
  except Exception as e:
    print(e)
	
  finally:
    cursor.close()
    conn.close()

@app.route('/movies/delete/<int:id>')
def delete_movies(id):
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute("DELETE FROM movies WHERE id=%s", (id,))
		conn.commit()
		return redirect('/movies')
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()

@app.route('/edit_movies/<int:id>')
def edit_movies(id):
  try:
    form = EditMoviesForm(request.form)
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, movieformat_id, movietype_id, duration, country_code, start_date, end_date, image, note, description from movies WHERE id=%s", id)
    row = cursor.fetchone()
    cursor1 = conn.cursor()
    cursor1.execute("SELECT id, name from movieformats")
    movieformat = cursor1.fetchall()
    cursor2 = conn.cursor()
    cursor2.execute("SELECT id, name from movietypes")
    movietype = cursor2.fetchall()
    cursor3 = conn.cursor()
    cursor3.execute("SELECT country_code, country from countries")
    country = cursor3.fetchall()
    if row:
      return render_template('layouts/default.html', content=render_template( 'pages/movies/edit.html', form=form, movieformat=movieformat, movietype=movietype, country=country, row=row, username=session['username'], avatar=session['avatar']))
    else:
      return 'Error loading #{id}'.format(id=id)
  except Exception as e:
    print(e)
  finally:
    cursor.close() 
    conn.close()

@app.route('/movies/update', methods=['POST'])
def update_movies():
  try:		
    movieformat_id = request.form.get('movieformat_id')
    movietype_id = request.form.get('movietype_id')
    country_code = request.form.get('country_code')
    form = EditMoviesForm(request.form)
    msg = None
    id = request.form.get('id', '', type=int)
    name = request.form.get('name', '', type=str)  
    duration = request.form.get('duration', '', type=int)  
    start_date = request.form.get('start_date', '', type=str)
    end_date = request.form.get('end_date', '', type=str)
    note = request.form.get('note', '', type=str)
    description = request.form.get('description', '', type=str)
    if request.method == 'POST':
      file = request.files['image']
      if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        image = "/static/assets/img/uploads/"+filename
        sql = "UPDATE movies SET name=%s,movieformat_id=%s,movietype_id=%s,duration=%s,country_code=%s,start_date=%s,end_date=%s,image=%s,note=%s,description=%s WHERE id=%s"
        data = (name, movieformat_id, movietype_id, duration, country_code, start_date, end_date, image, note, description, id,)
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sql, data)
        conn.commit()
        return redirect('/movies')
    else:
      return redirect('/edit_movies/%s',username)
  except Exception as e:
    print(e)
  finally:
    cursor.close() 
    conn.close()

# Seat Types

@app.route('/seattypes')
def seattypes():
  def db_query():
    db = Database()
    emps = db.list_seattypes()
    return emps
  res = db_query()
  logger = logging.getLogger('example_logger')
  logger.warning(res)
  return render_template('layouts/default.html', content=render_template( 'pages/seattypes/index.html',result=res, content_type='application/json', username=session['username'], avatar=session['avatar']))

@app.route('/new_seattypes')
def add_seattypes():
  form = AddSeattypesForm(request.form)
  msg = None
  return render_template('layouts/default.html', content=render_template( 'pages/seattypes/new.html', form=form, msg=msg, username=session['username'], avatar=session['avatar']))

@app.route('/seattypes/add', methods=['POST'])
def addSeattypes():
  try:
    form = AddSeattypesForm(request.form)
    msg = None
    id = request.form.get('id', '', type=int)
    seattype_name = request.form.get('seattype_name', '', type=str)        
    if id and seattype_name and request.method == 'POST':
      sql = "INSERT INTO seattypes (id, seattype_name) VALUES(%s, %s)"
      data = (id, seattype_name,)
      conn = mysql.connect()
      cursor = conn.cursor()
      cursor.execute(sql, data)
      conn.commit()
      return redirect('/seattypes')
    else:
      return redirect('/new_seattypes')
  except Exception as e:
    print(e)
	
  finally:
    cursor.close()
    conn.close()

@app.route('/seattypes/delete/<int:id>')
def delete_seattypes(id):
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute("DELETE FROM seattypes WHERE id=%s", (id,))
		conn.commit()
		return redirect('/seattypes')
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()

@app.route('/edit_seattypes/<int:id>')
def edit_seattypes(id):
  try:
    form = EditSeattypesForm(request.form)
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT id, seattype_name FROM seattypes WHERE id=%s", id)
    row = cursor.fetchone()
    if row:
      logger = logging.getLogger('example_logger')
      logger.warning(row)  
      return render_template('layouts/default.html', content=render_template( 'pages/seattypes/edit.html', form=form, row=row, username=session['username'], avatar=session['avatar']))
    else:
      return 'Error loading #{id}'.format(id=id)
  except Exception as e:
    print(e)
  finally:
    cursor.close() 
    conn.close()

@app.route('/seattypes/update', methods=['POST'])
def update_seattypes():
  try:		
    form = EditSeattypesForm(request.form)
    msg = None
    id = request.form.get('id', '', type=int)
    seattype_name = request.form.get('seattype_name', '', type=str)
    if seattype_name and id and request.method == 'POST':
      sql = "UPDATE seattypes SET seattype_name=%s WHERE id=%s"
      data = (seattype_name, id,)
      conn = mysql.connect()
      cursor = conn.cursor()
      cursor.execute(sql, data)
      conn.commit()
      return redirect('/seattypes')
    else:
      return redirect('/edit_seattypes/%s',id)
  except Exception as e:
    print(e)
  finally:
    cursor.close() 
    conn.close()

# Room Formats

@app.route('/roomformats')
def roomformats():
  def db_query():
    db = Database()
    emps = db.list_roomformats()
    return emps
  res = db_query()
  logger = logging.getLogger('example_logger')
  logger.warning(res)
  return render_template('layouts/default.html', content=render_template( 'pages/roomformats/index.html',result=res, content_type='application/json', username=session['username'], avatar=session['avatar']))

@app.route('/new_roomformats')
def add_roomformats():
  form = AddRoomformatsForm(request.form)
  msg = None
  return render_template('layouts/default.html', content=render_template( 'pages/roomformats/new.html', form=form, msg=msg, username=session['username'], avatar=session['avatar']))

@app.route('/roomformats/add', methods=['POST'])
def addRoomformats():
  try:
    form = AddRoomformatsForm(request.form)
    msg = None
    id = request.form.get('id', '', type=int)
    name = request.form.get('name', '', type=str)        
    if id and name and request.method == 'POST':
      sql = "INSERT INTO roomformats (id, name) VALUES(%s, %s)"
      data = (id, name,)
      conn = mysql.connect()
      cursor = conn.cursor()
      cursor.execute(sql, data)
      conn.commit()
      return redirect('/roomformats')
    else:
      return redirect('/new_roomformats')
  except Exception as e:
    print(e)
	
  finally:
    cursor.close()
    conn.close()

@app.route('/roomformats/delete/<int:id>')
def delete_roomformats(id):
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute("DELETE FROM roomformats WHERE id=%s", (id,))
		conn.commit()
		return redirect('/roomformats')
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()

@app.route('/edit_roomformats/<int:id>')
def edit_roomformats(id):
  try:
    form = EditRoomformatsForm(request.form)
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM roomformats WHERE id=%s", id)
    row = cursor.fetchone()
    if row:
      logger = logging.getLogger('example_logger')
      logger.warning(row)  
      return render_template('layouts/default.html', content=render_template( 'pages/roomformats/edit.html', form=form, row=row, username=session['username'], avatar=session['avatar']))
    else:
      return 'Error loading #{id}'.format(id=id)
  except Exception as e:
    print(e)
  finally:
    cursor.close() 
    conn.close()

@app.route('/roomformats/update', methods=['POST'])
def update_roomformats():
  try:		
    form = EditRoomformatsForm(request.form)
    msg = None
    id = request.form.get('id', '', type=int)
    name = request.form.get('name', '', type=str)
    if name and id and request.method == 'POST':
      sql = "UPDATE roomformats SET name=%s WHERE id=%s"
      data = (name, id,)
      conn = mysql.connect()
      cursor = conn.cursor()
      cursor.execute(sql, data)
      conn.commit()
      return redirect('/roomformats')
    else:
      return redirect('/edit_roomformats/%s',id)
  except Exception as e:
    print(e)
  finally:
    cursor.close() 
    conn.close()

# Rooms

@app.route('/rooms')
def rooms():
  def db_query():
    db = Database()
    emps = db.list_rooms()
    return emps
  res = db_query()
  logger = logging.getLogger('example_logger')
  logger.warning(res)
  return render_template('layouts/default.html', content=render_template( 'pages/rooms/index.html',result=res, content_type='application/json', username=session['username'], avatar=session['avatar']))

@app.route('/new_rooms')
def add_rooms():
  form = AddRoomsForm(request.form)
  msg = None
  return render_template('layouts/default.html', content=render_template( 'pages/rooms/new.html', form=form, msg=msg, username=session['username'], avatar=session['avatar']))

@app.route('/rooms/add', methods=['POST'])
def addRooms():
  try:
    form = AddRoomsForm(request.form)
    msg = None
    id = request.form.get('id', '', type=int)
    room_name = request.form.get('room_name', '', type=str)
    roomformat_id = request.form.get('roomformat_id', '', type=int)
    status = request.form.get('status', '', type=str)      
    max_row_seat = request.form.get('max_row_seat', '', type=int)
    max_seat_row = request.form.get('max_seat_row', '', type=int)
    note = request.form.get('note', '', type=str)
    if id and room_name and roomformat_id and status and max_row_seat and max_seat_row and note and request.method == 'POST':
      sql = "INSERT INTO rooms (id, room_name, roomformat_id, status, max_row_seat, max_seat_row, note) VALUES(%s, %s, %s, %s, %s, %s, %s )"
      data = (id, room_name, roomformat_id, status, max_row_seat, max_seat_row, note,)
      conn = mysql.connect()
      cursor = conn.cursor()
      cursor.execute(sql, data)
      conn.commit()
      return redirect('/rooms')
    else:
      return redirect('/new_rooms')
  except Exception as e:
    print(e)
	
  finally:
    cursor.close()
    conn.close()

@app.route('/rooms/delete/<int:id>')
def delete_rooms(id):
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute("DELETE FROM rooms WHERE id=%s", (id,))
		conn.commit()
		return redirect('/rooms')
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()

@app.route('/edit_rooms/<int:id>')
def edit_rooms(id):
  try:
    form = EditRoomsForm(request.form)
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT id, room_name, roomformat_id, status, max_row_seat, max_seat_row, note FROM rooms WHERE id=%s", id)
    row = cursor.fetchone()
    if row:
      logger = logging.getLogger('example_logger')
      logger.warning(row)  
      return render_template('layouts/default.html', content=render_template( 'pages/rooms/edit.html', form=form, row=row, username=session['username'], avatar=session['avatar']))
    else:
      return 'Error loading #{id}'.format(id=id)
  except Exception as e:
    print(e)
  finally:
    cursor.close() 
    conn.close()

@app.route('/rooms/update', methods=['POST'])
def update_rooms():
  try:		
    form = EditRoomsForm(request.form)
    msg = None
    id = request.form.get('id', '', type=int)
    room_name = request.form.get('room_name', '', type=str)
    roomformat_id = request.form.get('roomformat_id', '', type=int)
    status = request.form.get('status', '', type=str)      
    max_row_seat = request.form.get('max_row_seat', '', type=int)
    max_seat_row = request.form.get('max_seat_row', '', type=int)
    note = request.form.get('note', '', type=str)
    if id and room_name and roomformat_id and status and max_row_seat and max_seat_row and note and request.method == 'POST':
      sql = "UPDATE rooms SET room_name=%s, roomformat_id=%s, status=%s, max_row_seat=%s, max_seat_row=%s, note=%s WHERE id=%s"
      data = (room_name, roomformat_id, status, max_row_seat, max_seat_row, note, id,)
      conn = mysql.connect()
      cursor = conn.cursor()
      cursor.execute(sql, data)
      conn.commit()
      return redirect('/rooms')
    else:
      return redirect('/edit_rooms/%s',id)
  except Exception as e:
    print(e)
  finally:
    cursor.close() 
    conn.close()

# Status

@app.route('/status')
def status():
  def db_query():
    db = Database()
    emps = db.list_status()
    return emps
  res = db_query()
  logger = logging.getLogger('example_logger')
  logger.warning(res)
  return render_template('layouts/default.html', content=render_template( 'pages/status/index.html',result=res, content_type='application/json', username=session['username'], avatar=session['avatar']))

@app.route('/new_status')
def add_status():
  form = AddStatusForm(request.form)
  msg = None
  return render_template('layouts/default.html', content=render_template( 'pages/status/new.html', form=form, msg=msg, username=session['username'], avatar=session['avatar']))

@app.route('/status/add', methods=['POST'])
def addStatus():
  try:
    form = AddStatusForm(request.form)
    msg = None
    id = request.form.get('id', '', type=int)
    seat_condition = request.form.get('seat_condition', '', type=str)        
    if id and seat_condition and request.method == 'POST':
      sql = "INSERT INTO status (id, seat_condition) VALUES(%s, %s)"
      data = (id, seat_condition,)
      conn = mysql.connect()
      cursor = conn.cursor()
      cursor.execute(sql, data)
      conn.commit()
      return redirect('/status')
    else:
      return redirect('/new_status')
  except Exception as e:
    print(e)
	
  finally:
    cursor.close()
    conn.close()

@app.route('/status/delete/<int:id>')
def delete_status(id):
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute("DELETE FROM status WHERE id=%s", (id,))
		conn.commit()
		return redirect('/status')
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()

@app.route('/edit_status/<int:id>')
def edit_status(id):
  try:
    form = EditStatusForm(request.form)
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT id, seat_condition FROM status WHERE id=%s", id)
    row = cursor.fetchone()
    if row:
      logger = logging.getLogger('example_logger')
      logger.warning(row)  
      return render_template('layouts/default.html', content=render_template( 'pages/status/edit.html', form=form, row=row, username=session['username'], avatar=session['avatar']))
    else:
      return 'Error loading #{id}'.format(id=id)
  except Exception as e:
    print(e)
  finally:
    cursor.close() 
    conn.close()

@app.route('/status/update', methods=['POST'])
def update_status():
  try:		
    form = EditStatusForm(request.form)
    msg = None
    id = request.form.get('id', '', type=int)
    seat_condition = request.form.get('seat_condition', '', type=str)
    if seat_condition and id and request.method == 'POST':
      sql = "UPDATE status SET seat_condition=%s WHERE id=%s"
      data = (seat_condition, id,)
      conn = mysql.connect()
      cursor = conn.cursor()
      cursor.execute(sql, data)
      conn.commit()
      return redirect('/status')
    else:
      return redirect('/edit_status/%s',id)
  except Exception as e:
    print(e)
  finally:
    cursor.close() 
    conn.close()

# Showings (Xuất chiếu)
class ExampleForm(Form):
    dt = DateField('DatePicker', format='%Y-%m-%d')
    startDate = DateField('DatePicker', format='%Y-%m-%d')
    endDate = DateField('DatePicker', format='%Y-%m-%d')
    id = StringField  ('Id')

@app.route('/showings', methods=['POST', 'GET'])
def showings():
  try:
    form = ExampleForm()
    id = request.form.get('id', '', type=int)
    tvalue= str(datetime.today().strftime("%Y-%m-%d"))
    if form.validate_on_submit():
      tvalue = str(form.dt.data.strftime('%Y-%m-%d'))
    def db_query():
      db = Database()
      emps = db.list_showings()
      return emps
    res = db_query()
    demo = datetime.strptime(tvalue, '%Y-%m-%d').date()
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT id, room_name from rooms")
    row = cursor.fetchall()
    cursor1 = conn.cursor()
    cursor1.execute("SELECT DISTINCT showtime from showings")
    row1 = cursor1.fetchall()
    cursor3 = conn.cursor()
    cursor3.execute("SELECT id, name from movies")
    row3 = cursor3.fetchall()
    if id:
      cursor2 = conn.cursor()
      cursor2.execute("SELECT name, time from showings INNER JOIN movies ON showings.movie_id = movies.id WHERE id=%s",id)
      row2 = cursor2.fetchone()
      logger = logging.getLogger('example_logger')
      logger.warning(row2)
    
    if row and row1:
      logger = logging.getLogger('example_logger')
      logger.warning(row3)
      
      for i in range(len(row1)):
        logger.warning(row1[i][0])
      for i in range(len(res)):
        logger.warning(res[i][1])
      return render_template('layouts/default.html', content=render_template( 'pages/showings/index.html', row=row, row1=row1, row3=row3, res=res, demo=demo, form=form, username=session['username'], avatar=session['avatar']))
    else:
      return 'Error loading '
  except Exception as e:
    print(e)
  finally:
    cursor.close() 
    conn.close()

@app.route('/showings/update/<string:id>/<string:movie_id>/<string:time>')
def update_showings(id, movie_id, time):
  try:
    time_obj = datetime.strptime(time, '%H:%M:%S').time()
    id_obj = int(id)
    movie_id_obj = int(movie_id)
    sql = "UPDATE showings SET movie_id=%s, time=%s WHERE id=%s"
    data = (movie_id_obj, time_obj, id_obj,)
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql, data)
    conn.commit()
    return redirect('/showings')
  except Exception as e:
    print(e)
  finally:
    cursor.close() 
    conn.close()

@app.route('/showings/add/<string:id>/<string:movie_id>/<string:time>/<string:date>')
def addShowings(id, movie_id, time, date):
  try:
    date_obj = datetime.strptime(date, '%Y-%m-%d').date()
    time_obj = datetime.strptime(time, '%H:%M:%S').time()
    id_obj = int(id)
    movie_id_obj = int(movie_id)
    sql = "INSERT INTO showings (movie_id, room_id, showtime, time) VALUES(%s, %s, %s, %s )"
    data = (movie_id_obj, id_obj, date_obj, time_obj,)
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql, data)
    conn.commit()
    return redirect('/showings')
  except Exception as e:
    print(e)
  finally:
    cursor.close() 
    conn.close()

@app.route('/showings/delete/<string:id>')
def delete_showings(id):
    id_obj = int(id)
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM showings WHERE id=%s", (id,))
    conn.commit()
    return redirect('/showings')