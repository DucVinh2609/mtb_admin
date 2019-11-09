from flask               import render_template, request, url_for, redirect, send_from_directory
from flask_login         import login_user, logout_user, current_user, login_required
from werkzeug.exceptions import HTTPException, NotFound, abort

import os, logging 

from app        import app, lm, db, bc
from app.models import User
from app.forms  import LoginForm, RegisterForm, AddMovietypesForm, EditMovietypesForm
from flaskext.mysql import MySQL

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
@app.route('/login.html', methods=['GET', 'POST'])
def login():

    # Declare the login form
    form = LoginForm(request.form)

    # Flask message injected into the page, in case of any errors
    msg = None

    # check if both http method is POST and form is valid on submit
    if form.validate_on_submit():

        # assign form data to variables
        username = request.form.get('username', '', type=str)
        password = request.form.get('password', '', type=str) 

        # filter User out of database through username
        # user = User.query.filter_by(user=username).first()
        # if username == 'admin' and password== 'admin':
        #   return redirect(url_for('index'))
        # else:
        #   msg = "Unkkown user"
        # if user:
            
        #     #if bc.check_password_hash(user.password, password):
        #     if user.password == password:
        #         login_user(user)
        #         return redirect(url_for('index'))
        #     else:
        #         msg = "Wrong password. Please try again."
        # else:
        #     msg = "Unkkown user"
        
        cursor.execute("SELECT * from employees where username='" + username + "' and password='" + password + "'")
        data = cursor.fetchone()
        if data is None:
          msg = "Username or Password is wrong"
        else:
          return redirect(url_for('index'))

    return render_template('layouts/auth-default.html',
                            content=render_template( 'pages/login.html', form=form, msg=msg ) )

# Render the icons page
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
    cursor.execute("SELECT name FROM movietypes WHERE id=%s", id)
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