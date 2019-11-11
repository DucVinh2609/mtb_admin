from flask_wtf          import FlaskForm
from flask_wtf.file     import FileField, FileRequired
from wtforms            import StringField, TextAreaField, SubmitField, PasswordField
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

