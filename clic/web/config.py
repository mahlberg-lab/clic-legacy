# -*- coding: utf-8 -*-
import os
import os.path
import random
import string

'''
The basic config for the app can be found in this file. It is imported in
index.py as part of the construction of the app variable.
'''

BASE_DIR = os.path.dirname(__file__)
CLIC_DIR = os.path.abspath(os.path.join(BASE_DIR, '../..'))

def textConfigParam(file_name, default=None):
    file_path = os.path.join(CLIC_DIR, file_name)
    if not os.path.exists(file_path):
        return default
    with open(file_path,'r') as f:
        return f.read().strip()

SQLALCHEMY_DATABASE_URI = "postgresql://%s:%s@localhost/db_annotation" % (
    'clic-dickens',
    textConfigParam('secret-dbpassword.txt', 'charles'),
)
SECRET_KEY = textConfigParam('secret-secretkey.txt', 'qdfmkqjfmqksjfdmk')

GA_KEY = textConfigParam('secret-googleanalytics-key.txt', 'TEST-KEY')

DEBUG = False
DEBUG_TB_INTERCEPT_REDIRECTS = False
# when testing = True, the login_required decorator is disabled.
TESTING = False
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
