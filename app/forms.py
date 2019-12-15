from flask_wtf          import FlaskForm
from flask_wtf.file     import FileField, FileRequired
from wtforms            import StringField, TextAreaField, SubmitField, PasswordField
from wtforms.fields.html5 import DateField
from flask_ckeditor import CKEditorField
from wtforms.validators import InputRequired, Email, DataRequired

class LoginForm(FlaskForm):
	username    = StringField  (u'Username'        , validators=[DataRequired()])
	password    = PasswordField(u'Password'        , validators=[DataRequired()])

class RegisterForm(FlaskForm):
	username    = StringField  (u'Username'  , validators=[DataRequired()])
	password    = PasswordField(u'Password'  , validators=[DataRequired()])
	email       = StringField  (u'Email'     , validators=[DataRequired(), Email()])

class AddMovietypesForm(FlaskForm):
	id    = StringField  (u'Id'        , validators=[DataRequired()])
	name    = StringField  (u'Name'        , validators=[DataRequired()])

class EditMovietypesForm(FlaskForm):
	id    = StringField  (u'Id'        , validators=[DataRequired()])
	name    = StringField  (u'Name'        , validators=[DataRequired()])

class AddMovieFormatsForm(FlaskForm):
	id    = StringField  (u'Id'        , validators=[DataRequired()])
	name    = StringField  (u'Name'        , validators=[DataRequired()])

class EditMovieFormatsForm(FlaskForm):
	id    = StringField  (u'Id'        , validators=[DataRequired()])
	name    = StringField  (u'Name'        , validators=[DataRequired()])

class AddRolesForm(FlaskForm):
	id    = StringField  (u'Id'        , validators=[DataRequired()])
	role    = StringField  (u'Role'        , validators=[DataRequired()])

class EditRolesForm(FlaskForm):
	id    = StringField  (u'Id'        , validators=[DataRequired()])
	role    = StringField  (u'Role'        , validators=[DataRequired()])

class AddCountriesForm(FlaskForm):
	country_code    = StringField  (u'Country Code'        , validators=[DataRequired()])
	country    = StringField  (u'Country'        , validators=[DataRequired()])

class EditCountriesForm(FlaskForm):
	country_code    = StringField  (u'Country Code'        , validators=[DataRequired()])
	country    = StringField  (u'Country'        , validators=[DataRequired()])

class AddEmployeesForm(FlaskForm):
	username    = StringField  (u'Username'        , validators=[DataRequired()])
	password    = PasswordField  (u'Password'        , validators=[DataRequired()])
	fullname    = StringField  (u'Fullname'        , validators=[DataRequired()])
	birthday    = StringField  (u'Birthday'        , validators=[DataRequired()])
	address    = StringField  (u'Address'        , validators=[DataRequired()])
	phone    = StringField  (u'Phone'        , validators=[DataRequired()])
	gender    = StringField  (u'Gender'        , validators=[DataRequired()])
	role_id    = StringField  (u'RoleId'        , validators=[DataRequired()])
	avatar    = StringField  (u'Avatar'        , validators=[DataRequired()])
	about    = StringField  (u'About'        , validators=[DataRequired()])	

class EditEmployeesForm(FlaskForm):
	username    = StringField  (u'Username'        , validators=[DataRequired()])
	password    = PasswordField  (u'Password'        , validators=[DataRequired()])
	fullname    = StringField  (u'Fullname'        , validators=[DataRequired()])
	birthday    = StringField  (u'Birthday'        , validators=[DataRequired()])
	address    = StringField  (u'Address'        , validators=[DataRequired()])
	phone    = StringField  (u'Phone'        , validators=[DataRequired()])
	gender    = StringField  (u'Gender'        , validators=[DataRequired()])
	role_id    = StringField  (u'RoleId'        , validators=[DataRequired()])
	avatar    = StringField  (u'Avatar'        , validators=[DataRequired()])
	about    = StringField  (u'About'        , validators=[DataRequired()])

class AddMoviesForm(FlaskForm):
	id    = StringField  (u'ID'        , validators=[DataRequired()])
	name    = StringField  (u'Name'        , validators=[DataRequired()])
	movieformat_id    = StringField  (u'Movie Format'        , validators=[DataRequired()])
	movietype_id    = StringField  (u'Movie Type'        , validators=[DataRequired()])
	duration    = StringField  (u'Duration'        , validators=[DataRequired()])
	country_code    = StringField  (u'Country'        , validators=[DataRequired()])
	start_date    = StringField  (u'Start Date'        , validators=[DataRequired()])
	end_date    = StringField  (u'End Date'        , validators=[DataRequired()])
	image    = StringField  (u'Image'        , validators=[DataRequired()])
	note    = StringField  (u'Note'        , validators=[DataRequired()])
	description    = CKEditorField  (u'Description'        , validators=[DataRequired()])

class EditMoviesForm(FlaskForm):
	id    = StringField  (u'ID'        , validators=[DataRequired()])
	name    = StringField  (u'Name'        , validators=[DataRequired()])
	movieformat_id    = StringField  (u'Movie Format'        , validators=[DataRequired()])
	movietype_id    = StringField  (u'Movie Type'        , validators=[DataRequired()])
	duration    = StringField  (u'Duration'        , validators=[DataRequired()])
	country_code    = StringField  (u'Country'        , validators=[DataRequired()])
	start_date    = StringField  (u'Start Date'        , validators=[DataRequired()])
	end_date    = StringField  (u'End Date'        , validators=[DataRequired()])
	image    = StringField  (u'Image'        , validators=[DataRequired()])
	note    = StringField  (u'Note'        , validators=[DataRequired()])
	description    = CKEditorField  (u'Description'        , validators=[DataRequired()])

class AddSeattypesForm(FlaskForm):
	id    = StringField  (u'Id'        , validators=[DataRequired()])
	seattype_name    = StringField  (u'Seattype Name'        , validators=[DataRequired()])

class EditSeattypesForm(FlaskForm):
	id    = StringField  (u'Id'        , validators=[DataRequired()])
	seattype_name    = StringField  (u'Seattype Name'        , validators=[DataRequired()])

class AddRoomformatsForm(FlaskForm):
	id    = StringField  (u'Id'        , validators=[DataRequired()])
	name    = StringField  (u'Name'        , validators=[DataRequired()])

class EditRoomformatsForm(FlaskForm):
	id    = StringField  (u'Id'        , validators=[DataRequired()])
	name    = StringField  (u'Name'        , validators=[DataRequired()])

class AddRoomsForm(FlaskForm):
	id    = StringField  (u'Id'        , validators=[DataRequired()])
	room_name    = StringField  (u'Room name'        , validators=[DataRequired()])
	roomformat_id = StringField  (u'Room name'        , validators=[DataRequired()])
	status = StringField  (u'Room name'        , validators=[DataRequired()])
	max_row_seat = StringField  (u'Room name'        , validators=[DataRequired()])
	max_seat_row = StringField  (u'Room name'        , validators=[DataRequired()])
	note = StringField  (u'Room name'        , validators=[DataRequired()])
class EditRoomsForm(FlaskForm):
	id    = StringField  (u'Id'        , validators=[DataRequired()])
	room_name    = StringField  (u'Room name'        , validators=[DataRequired()])
	roomformat_id = StringField  (u'Room name'        , validators=[DataRequired()])
	status = StringField  (u'Room name'        , validators=[DataRequired()])
	max_row_seat = StringField  (u'Room name'        , validators=[DataRequired()])
	max_seat_row = StringField  (u'Room name'        , validators=[DataRequired()])
	note = StringField  (u'Room name'        , validators=[DataRequired()])

class AddStatusForm(FlaskForm):
	id    = StringField  (u'Id'        , validators=[DataRequired()])
	seat_condition    = StringField  (u'Seat condition'        , validators=[DataRequired()])

class EditStatusForm(FlaskForm):
	id    = StringField  (u'Id'        , validators=[DataRequired()])
	seat_condition    = StringField  (u'Seat condition'        , validators=[DataRequired()])

class EditPassForm(FlaskForm):
	current_password    = PasswordField  (u'Current password'        , validators=[DataRequired()])
	new_password    = PasswordField  (u'New password'        , validators=[DataRequired()])
	confirm_password    = PasswordField  (u'Cofirm password'        , validators=[DataRequired()])
	