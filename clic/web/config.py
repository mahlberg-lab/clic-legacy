# -*- coding: utf-8 -*-

'''
The basic config for the app can be found in this file. It is imported in
index.py as part of the construction of the app variable.
'''

SQLALCHEMY_DATABASE_URI = "postgresql://clic-dickens:charles@localhost/db_annotation"
DEBUG = False
DEBUG_TB_INTERCEPT_REDIRECTS = False
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
# https://pythonhosted.org/Flask-Security/configuration.html
SECURITY_POST_LOGIN_VIEW = "/annotation"
SECURITY_REGISTERABLE = False
SECURITY_REGISTER_URL = "/charlesdickens"
SECURITY_POST_REGISTER_VIEW = "/annotation"
SECURITY_TRACKABLE = False
SECURITY_RECOVERABLE = False
SECURITY_SEND_REGISTER_EMAIL = False
SECURITY_CONFIRMABLE = False
