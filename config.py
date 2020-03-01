import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess2'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT') or None
    ADMINS = ['your-email@example.com']
    ROWS_PER_PAGE_FULL = 20
    ROWS_PER_PAGE_FILTER = 10
    TEMPLATES_AUTO_RELOAD = True
