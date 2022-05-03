from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Email


class TodoForm(FlaskForm):
    title = StringField('Lable', validators=[DataRequired()])
    description = TextAreaField('Input', validators=[DataRequired()])
    done = BooleanField('Required')
     
    
    