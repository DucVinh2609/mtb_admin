from flask               import render_template, request, url_for, redirect, send_from_directory, jsonify
from flask_login         import login_user, logout_user, current_user, login_required
from werkzeug.exceptions import HTTPException, NotFound, abort
from flask_restful import Resource, Api

import os, logging 

from app        import app, lm, db, bc
from app.models import User
from app.forms  import LoginForm, RegisterForm, AddMovietypesForm, EditMovietypesForm, AddMovieFormatsForm, EditMovieFormatsForm, AddRolesForm, EditRolesForm, AddEmployeesForm, EditEmployeesForm, AddCountriesForm, EditCountriesForm, AddMoviesForm, EditMoviesForm, AddSeattypesForm, EditSeattypesForm, AddRoomformatsForm, EditRoomformatsForm
from flaskext.mysql import MySQL

api = Api(app)
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'mtb_db'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
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
    self.cur.execute("SELECT username, fullname, birthday, address, phone, gender, role_id, avatar from employees")
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
@app.route('/logout.html')
def logout():
    logout_user()
    return redirect(url_for('index'))

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
      data = cursor.fetchone()
      if data is None:
        msg = "Username or Password is wrong"
      else:
        return redirect('/')
    return render_template('layouts/auth-default.html', content=render_template( 'pages/login.html', form=form, msg=msg ) )

@app.route('/icons.html')
def icons():

    return render_template('layouts/default.html',
                            content=render_template( 'pages/icons.html') )

# Render the profile page
@app.route('/profile.html')
def profile():

    return render_template('layouts/default.html',
                            content=render_template( 'pages/profile.html') )


# Render the tables page
@app.route('/tables.html')
def tables():

    return render_template('layouts/default.html',
                            content=render_template( 'pages/tables.html') )

# App main route + generic routing
@app.route('/', defaults={'path': 'index.html'})
@app.route('/<path>')
def index(path):

    content = None

    try:

        # try to match the pages defined in -> pages/<input file>
        return render_template('layouts/default.html',
                                content=render_template( 'pages/'+path) )
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
  return render_template('layouts/default.html', content=render_template( 'pages/movietypes/index.html',result=res, content_type='application/json'))

@app.route('/new_movietypes')
def add_movietypes():
  form = AddMovietypesForm(request.form)
  msg = None
  return render_template('layouts/default.html', content=render_template( 'pages/movietypes/new.html', form=form, msg=msg))

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
      return render_template('layouts/default.html', content=render_template( 'pages/movietypes/edit.html', form=form, row=row))
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
  return render_template('layouts/default.html', content=render_template( 'pages/movieformats/index.html',result=res, content_type='application/json'))

@app.route('/new_movieformats')
def add_movieformats():
  form = AddMovieFormatsForm(request.form)
  msg = None
  return render_template('layouts/default.html', content=render_template( 'pages/movieformats/new.html', form=form, msg=msg))

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
      return render_template('layouts/default.html', content=render_template( 'pages/movieformats/edit.html', form=form, row=row))
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
  return render_template('layouts/default.html', content=render_template( 'pages/roles/index.html',result=res, content_type='application/json'))

@app.route('/new_roles')
def add_roles():
  form = AddRolesForm(request.form)
  msg = None
  return render_template('layouts/default.html', content=render_template( 'pages/roles/new.html', form=form, msg=msg))

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
      return render_template('layouts/default.html', content=render_template( 'pages/roles/edit.html', form=form, row=row))
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
  return render_template('layouts/default.html', content=render_template( 'pages/employees/index.html',result=res, content_type='application/json'))

@app.route('/new_employees')
def add_employees():
  form = AddEmployeesForm(request.form)
  msg = None
  return render_template('layouts/default.html', content=render_template( 'pages/employees/new.html', form=form, msg=msg))

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
    cursor.execute("SELECT username, fullname, birthday, address, phone, gender, role_id, avatar from employees WHERE username=%s", username)
    row = cursor.fetchone()
    if row:
      return render_template('layouts/default.html', content=render_template( 'pages/employees/edit.html', form=form, row=row))
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
    avatar = request.form.get('avatar', '', type=str)
    if username and fullname and birthday and address and phone and gender and role_id and avatar and request.method == 'POST':
      sql = "UPDATE employees SET fullname=%s,birthday=%s,address=%s,phone=%s,gender=%s,role_id=%s,avatar=%s WHERE username=%s"
      data = (fullname, birthday, address, phone, gender, role_id, avatar, username,)
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
  return render_template('layouts/default.html', content=render_template( 'pages/countries/index.html',result=res, content_type='application/json'))

@app.route('/new_countries')
def add_countries():
  form = AddCountriesForm(request.form)
  msg = None
  return render_template('layouts/default.html', content=render_template( 'pages/countries/new.html', form=form, msg=msg))

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
      return render_template('layouts/default.html', content=render_template( 'pages/countries/edit.html', form=form, row=row))
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

# Movies

@app.route('/movies')
def movies():
  def db_query():
    db = Database()
    emps = db.list_movies()
    return emps
  res = db_query()
  return render_template('layouts/default.html', content=render_template( 'pages/movies/index.html',result=res, content_type='application/json'))

@app.route('/new_movies')
def add_movies():
  form = AddMoviesForm(request.form)
  msg = None
  return render_template('layouts/default.html', content=render_template( 'pages/movies/new.html', form=form, msg=msg))

@app.route('/movies/add', methods=['POST'])
def addMovies():
  try:
    form = AddMoviesForm(request.form)
    msg = None
    id = request.form.get('id', '', type=int)
    name = request.form.get('name', '', type=str)
    movieformat_id = request.form.get('movieformat_id', '', type=int)
    movietype_id = request.form.get('movietype_id', '', type=int)      
    duration = request.form.get('duration', '', type=int)  
    country_code = request.form.get('country_code', '', type=str)
    start_date = request.form.get('start_date', '', type=str)
    end_date = request.form.get('end_date', '', type=str)
    image = request.form.get('image', '', type=str)
    note = request.form.get('note', '', type=str)
    description = request.form.get('description', '', type=str)
    if id and name and movieformat_id and movietype_id and duration and country_code and start_date and end_date and image and note and description and request.method == 'POST':
      sql = "INSERT INTO movies (id, name, movieformat_id, movietype_id, duration, country_code, start_date, end_date, image, note, description) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
      data = (id, name, movieformat_id, movietype_id, duration, country_code, start_date, end_date, image, note, description,)
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
    if row:
      return render_template('layouts/default.html', content=render_template( 'pages/movies/edit.html', form=form, row=row))
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
    form = EditMoviesForm(request.form)
    msg = None
    id = request.form.get('id', '', type=int)
    name = request.form.get('name', '', type=str)
    movieformat_id = request.form.get('movieformat_id', '', type=int)
    movietype_id = request.form.get('movietype_id', '', type=int)      
    duration = request.form.get('duration', '', type=int)  
    country_code = request.form.get('country_code', '', type=str)
    start_date = request.form.get('start_date', '', type=str)
    end_date = request.form.get('end_date', '', type=str)
    image = request.form.get('image', '', type=str)
    note = request.form.get('note', '', type=str)
    description = request.form.get('description', '', type=str)
    if id and name and movieformat_id and movietype_id and duration and country_code and start_date and end_date and image and note and description and request.method == 'POST':
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
  return render_template('layouts/default.html', content=render_template( 'pages/seattypes/index.html',result=res, content_type='application/json'))

@app.route('/new_seattypes')
def add_seattypes():
  form = AddSeattypesForm(request.form)
  msg = None
  return render_template('layouts/default.html', content=render_template( 'pages/seattypes/new.html', form=form, msg=msg))

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
      return render_template('layouts/default.html', content=render_template( 'pages/seattypes/edit.html', form=form, row=row))
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
  return render_template('layouts/default.html', content=render_template( 'pages/roomformats/index.html',result=res, content_type='application/json'))

@app.route('/new_roomformats')
def add_roomformats():
  form = AddRoomformatsForm(request.form)
  msg = None
  return render_template('layouts/default.html', content=render_template( 'pages/roomformats/new.html', form=form, msg=msg))

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
      return render_template('layouts/default.html', content=render_template( 'pages/roomformats/edit.html', form=form, row=row))
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