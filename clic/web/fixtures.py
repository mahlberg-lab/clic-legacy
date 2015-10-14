import os
from models import db, Subset
# importing from admin rather than db, because it needs app context
from admin import app


if __name__ == '__main__':

     # http://stackoverflow.com/a/19008403/2115409
     db.init_app(app)
     with app.app_context():
        # Extensions like Flask-SQLAlchemy now know what the "current" app
        # is while within this block. Therefore, you can now run........
        # db.create_all()
        # change to the right folder
        os.chdir('/Users/johan/projects/annotation/data/annotation/output/DNov/textract/')

        os.listdir(os.curdir)

        for folder in os.listdir(os.curdir):
            for input_file in os.listdir(folder):
                # parse the file names, fi. BH_non_suspended_quotes.txt
                name = input_file.split('_')[0]  # BH
                # BH_non_suspended_quotes.txt -> #  BH_non_suspended_quotes
                # -> #  non suspended quotes
                kind = input_file.split('.')[0].split('_')[1:]
                kind = '-'.join(kind)

                with open(folder + '/' + input_file) as input:
                    contents = input.readlines()
                    print name, kind, len(contents)

                    for itm in contents:
                        db.session.add(Subset(book=name, abbr=name, kind=kind, text=itm))

        db.session.commit()
