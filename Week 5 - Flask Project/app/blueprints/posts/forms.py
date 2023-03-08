from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class PostForm(FlaskForm):
    img_url = StringField('Image URL:', validators=[DataRequired()])
    title  = StringField('Title:', validators=[DataRequired()])
    caption = StringField('Cpation', validators=[DataRequired()])
    submit_btn = SubmitField('Submit', validators=[DataRequired()])