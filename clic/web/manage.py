# -*- coding: utf-8 -*-

'''
This meta file is used to migrate the database and apply the migrations.

It provides a management command.
'''

from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
import os

from index import app, db
# app.config.from_object(os.environ['APP_SETTINGS'])
from models import *

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
