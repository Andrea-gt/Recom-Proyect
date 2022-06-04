from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, EmailField, IntegerField
from wtforms.validators import DataRequired, EqualTo, Email, NumberRange

class LoginForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired()])
    email = EmailField('Correo', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    remember_me = BooleanField('Recordar Contraseña')
    submit = SubmitField('Inicia Sesion')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    name = StringField('Nombre', validators=[DataRequired()])
    age = IntegerField('Edad', validators=[DataRequired(), NumberRange(1,130)])
    gender = StringField('Género', validators=[DataRequired()])
    dpto = StringField('Departamento', validators=[DataRequired()])
    prof = StringField('Profesión', validators=[DataRequired()])
    fav = StringField('Animal favorito', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Registrarse')
