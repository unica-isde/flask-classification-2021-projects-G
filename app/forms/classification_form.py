from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, DecimalField
from wtforms.validators import DataRequired

from app.utils.list_images import list_images
from config import Configuration

from wtforms.widgets import NumberInput

conf = Configuration()


class ClassificationForm(FlaskForm):
    brightness = DecimalField(places=2, default=0, widget=NumberInput(min=0, max=1, step=0.05))
    contrast = DecimalField(places=2, default=0, widget=NumberInput(min=0, max=1, step=0.05))
    saturation = DecimalField(places=2, default=0, widget=NumberInput(min=0, max=1, step=0.05))
    hue = DecimalField(places=2, default=0, widget=NumberInput(min=0, max=0.5, step=0.025))

    model = SelectField('model', choices=conf.models, validators=[DataRequired()])
    image = SelectField('image', choices=list_images(), validators=[DataRequired()])
    submit = SubmitField('Submit')
