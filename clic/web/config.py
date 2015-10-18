SQLALCHEMY_DATABASE_URI = "postgresql://jdejoode:isabelle@localhost/annotation_dev"
DEBUG = False
# when testing = True, the login_required decorator is disabled.
TESTING = False
# FIXME not very secret here
SECRET_KEY = "qdfmkqjfmqksjfdmk"
MAIL_SERVER = 'smtp.qsdfqsdfqskjdfmlqsjdfmlkjjqsdf.com'
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USERNAME = 'username'
MAIL_PASSWORD = 'password'
# SECURITY_PASSWORD_HASH = "bcrypt"
# SECURITY_PASSWORD_SALT = "AasdsSDLKJFDasdflasdlfjhLJKHDlsdfjkhLKJ"
# https://pythonhosted.org/Flask-Security/models.html
SECURITY_REGISTERABLE = True
SECURITY_TRACKABLE = False
SECURITY_RECOVERABLE = False
SECURITY_CONFIRMABLE = False  # TODO
