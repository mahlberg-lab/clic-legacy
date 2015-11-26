# -*- coding: utf-8 -*-

'''
fixtures.py is a one-off script that loads textfiles into a postgres database
using the models defined in models.py

fixtures.py uses an command line argument:

    PYTHONPATH=/your/path/to/clic python fixtures.py path/to/input_dir

'''

import json
import os
import sys

from clic.web.index import app
from clic.web.models import db, Subset

input_dir = sys.argv[1]


BASE_DIR = os.path.dirname(__file__)
raw_booklist = open(os.path.join(BASE_DIR, '../booknames.json'), 'r')
booklist = json.load(raw_booklist)

SUBSETS = [
# all_suspensions,
'quotes',
'short_suspensions',
'long_suspensions',
'non_quotes',
# 'embedded_quotes',
# 'extended_quotes',
# 'non_suspended_narration',
# quotes_without_extended_quotes,
]

if __name__ == '__main__':

     # http://stackoverflow.com/a/19008403/2115409

     db.init_app(app)
     with app.app_context():
        # db.create_all()

        # change to the right folder
        os.chdir(input_dir)
        os.listdir(os.curdir)

        for folder in os.listdir(os.curdir):
            if folder in SUBSETS:
                for input_file in os.listdir(folder):
                    # parse the file names, fi. BH_non_suspended_quotes.txt
                    name = input_file.split('_')[0]  # BH
                    full_name = booklist[name]
                    # BH_non_suspended_quotes.txt -> #  BH_non_suspended_quotes
                    # -> #  non suspended quotes
                    kind = input_file.split('.')[0].split('_')[1:]
                    kind = '-'.join(kind)

                    with open(folder + '/' + input_file) as input:
                        contents = input.readlines()
                        print name, full_name, kind, len(contents)

                        for itm in contents:
                            db.session.add(Subset(book=full_name, abbr=name, kind=kind, text=itm))
            db.session.commit()
