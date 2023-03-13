from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class PokeForm(FlaskForm):
    name = StringField('API Lookup:', validators=[DataRequired()], render_kw={"placeholder": "Enter Name of Pokemon"})
    submit_btn = SubmitField('Submit', name='submit', validators=[DataRequired()])
    catch_btn = SubmitField('Catch', name='catch')