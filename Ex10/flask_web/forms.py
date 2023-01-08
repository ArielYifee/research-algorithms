from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import SubmitField


class DataForm(FlaskForm):
    picture = FileField('Select picture to optimize', validators=[FileAllowed(['jpg', 'png'])])    
    submit = SubmitField('Submit')

