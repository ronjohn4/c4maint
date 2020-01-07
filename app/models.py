# one time creation of the migrations folder
#   flask db init

# commit current changes to the model and build the migration script
#   flask db migrate -m "comment"

# execute the migration script
#   flask db upgrade

from app import db


class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    email = db.Column(db.String(120))
    sex = db.Column(db.Integer)     # https://en.wikipedia.org/wiki/ISO/IEC_5218
    dob = db.Column(db.Date)
    is_tobacco_user = db.Column(db.Boolean)
    zip = db.Column(db.String(10))
    county = db.Column(db.String(30))
    coverage_start = db.Column(db.Date)
    income_amount = db.Column(db.Numeric)
    income_frequency = db.Column(db.String(8))  # annually, monthly, weekly

    def __repr__(self):
        return '<Account {}>'.format(self.last_name)


class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64))
    dob = db.Column(db.Date)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))

    def __repr__(self):
        return '<Member {}>'.format(self.first_name)


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    plan_id = db.Column(db.Integer, db.ForeignKey('plan.id'))
    estimated_monthly_premium = db.Column(db.Numeric)
    yearly_cost_estimate = db.Column(db.Numeric)

    def __repr__(self):
        return '<Member {}>'.format(self.id)


class Plan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    insurance_company = db.Column(db.String(64))
    plan_name = db.Column(db.String(64))
    annual_deductible = db.Column(db.Numeric)
    annual_out_of_pocket_maximum = db.Column(db.Numeric)

    def __repr__(self):
        return '<Plan {}>'.format(self.plan_name)


class RxPreferences(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    drug_name = db.Column(db.String(64))
    form = db.Column(db.String(64))
    strength = db.Column(db.String(64))
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))

    def __repr__(self):
        return '<RxPreferences {}>'.format(self.id)


class DrPreferences(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    last_name = db.Column(db.String(64))
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))

    def __repr__(self):
        return '<DrPreferences {}>'.format(self.last_name)


class Parent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    email = db.Column(db.String(120))
    sex = db.Column(db.Integer)     # https://en.wikipedia.org/wiki/ISO/IEC_5218
    dob = db.Column(db.Date)
    is_tobacco_user = db.Column(db.Boolean)
    income_amount = db.Column(db.Numeric)

    def __repr__(self):
        return '<Parent {}>'.format(self.name)
