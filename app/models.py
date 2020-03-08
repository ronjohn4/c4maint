# https://flask-migrate.readthedocs.io/

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
    is_active = db.Column(db.Boolean)
    income_amount = db.Column(db.Numeric)

    def audit_format(self):
        return str({c.name: getattr(self, c.name) for c in self.__table__.columns})

    def __repr__(self):
        return '<Parent {}>'.format(self.name)


class ParentAudit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('parent.id'))
    a_datetime = db.Column(db.DateTime)
    a_user = db.Column(db.String(64))
    action = db.Column(db.String(64))
    before = db.Column(db.String)
    after = db.Column(db.String)

    def __repr__(self):
        return '<ParentAudit {}>'.format(self.datetime)
