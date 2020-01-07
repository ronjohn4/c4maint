from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, \
    TextAreaField, HiddenField, DateField, DecimalField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
import dateutil.parser


def validate_dob(form, field):
    try:
        dateutil.parser.parse(str(field.data))
    except ValueError:
        raise ValueError("Incorrect data format, should be YYYY-MM-DD")


class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')


class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    remember_me = BooleanField('remember me')
    submit = SubmitField('Sign In')


class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Request Password Reset')


class ParentForm(FlaskForm):
    id = HiddenField('id:', validators=[DataRequired()])
    name = StringField('Name:', validators=[DataRequired()])
    email = StringField('Email:', validators=[DataRequired(), Email()])
    # https://en.wikipedia.org/wiki/ISO/IEC_5218
    sex = SelectField('Sex', choices=[('0', 'Not known'), ('1', 'male'), ('2', 'female'), ('9', 'Not Applicable')])
    dob = StringField('DOB:', validators=[validate_dob])
    is_tobacco_user = BooleanField('Tobacco User:')
    income_amount = DecimalField('Income Amount:', places=2)

    def load(self, data):
        self.id.default = data.id
        self.name.default = data.name
        self.email.default = data.email
        self.sex.default = data.sex
        self.dob.default = data.dob
        self.is_tobacco_user.default = data.is_tobacco_user
        self.income_amount.default = data.income_amount
        self.process()
