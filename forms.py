from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class AddItemForm(FlaskForm):
    itemName = StringField('Item Name', validators=[DataRequired()])
    submit = SubmitField('Submit')