from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, HiddenField
from wtforms.validators import DataRequired


class AppForm(FlaskForm):
    id = HiddenField('id:')
    name = StringField('Name:', validators=[DataRequired()])
    is_active = BooleanField('Active:')

    def load(self, data):
        self.id.default = data.id
        self.name.default = data.name
        self.is_active.default = data.is_active
        self.process()
