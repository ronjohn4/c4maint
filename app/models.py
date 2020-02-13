# one time creation of the migrations folder
#   flask db init

# commit current changes to the model and build the migration script
#   flask db migrate -m "comment"

# execute the migration script
#   flask db upgrade

from app import db


sex = {0: 'not known',
       1: 'male',
       2: 'female',
       9: 'not applicable'}


class Parent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    email = db.Column(db.String(120))
    sex = db.Column(db.Integer)  # https://en.wikipedia.org/wiki/ISO/IEC_5218
    dob = db.Column(db.Date)
    is_tobacco_user = db.Column(db.Boolean)
    income_amount = db.Column(db.Numeric)

    def __repr__(self):
        return '<Parent {}>'.format(self.name)


class Child(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    parent_id = db.Column(db.Integer, db.ForeignKey('parent.id'))

    def __repr__(self):
        return '<Child {}>'.format(self.name)