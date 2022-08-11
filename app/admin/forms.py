from flask_wtf import FlaskForm
from wtforms import (StringField, SubmitField, TextAreaField, BooleanField)
from wtforms.validators import DataRequired, Length

class PostForm(FlaskForm):
    title   = StringField('Titulo', validators=[DataRequired(), Length(28)])
    context = TextAreaField('Contenido')
    submit  = SubmitField('Enviar')

class UserAdminForm(FlaskForm):
    is_admin = BooleanField('Administrador')
    submit = SubmitField('Guardar')