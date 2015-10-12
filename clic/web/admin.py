from __future__ import absolute_import

from flask import Flask, render_template
from wtforms.fields import PasswordField

from flask.ext.security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin, login_required
from flask.ext.admin.contrib import sqla
from flask_admin import Admin, BaseView, expose
from flask_mail import Mail
from flask_admin.contrib.sqla import ModelView

from models import db, Annotation, Category, Role, User, List

# app = Flask(__name__, static_url_path='')
app = Flask('clic.web', static_url_path='')
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://jdejoode:isabelle@localhost/annotation_dev"
app.config["DEBUG"] = True
# when testing = True, the login_required decorator is disabled.
app.config["TESTING"] = True
app.config["SECRET_KEY"] = "qdfmkqj fmqksjfdm k"
app.config['MAIL_SERVER'] = 'smtp.qsdfqsdfqskjdfmlqsjdfmlkjjqsdf.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'username'
app.config['MAIL_PASSWORD'] = 'password'
app.config['SECURITY_REGISTERABLE'] = True
app.config['SECURITY_TRACKABLE'] = True
app.config['SECURITY_RECOVERABLE'] = True

mail = Mail(app)
db.init_app(app)
# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)


# Taken from: https://github.com/sasaporta/flask-security-admin-example/blob/master/main.py
# Customized User model for SQL-Admin
class UserAdmin(sqla.ModelView):

    # Don't display the password on the list of Users
    column_exclude_list = list = ('password',)

    # Don't include the standard password field when creating or editing a User (but see below)
    form_excluded_columns = ('password',)

    # Automatically display human-readable names for the current and available Roles when creating or editing a User
    column_auto_select_related = True

    # Prevent administration of Users unless the currently logged-in user has the "admin" role
    def is_accessible(self):
        return current_user.has_role('admin')

    # On the form for creating or editing a User, don't display a field corresponding to the model's password field.
    # There are two reasons for this. First, we want to encrypt the password before storing in the database. Second,
    # we want to use a password field (with the input masked) rather than a regular text field.
    def scaffold_form(self):

        # Start with the standard form as provided by Flask-Admin. We've already told Flask-Admin to exclude the
        # password field from this form.
        form_class = super(UserAdmin, self).scaffold_form()

        # Add a password field, naming it "password2" and labeling it "New Password".
        form_class.password2 = PasswordField('New Password')
        return form_class

    # This callback executes when the user saves changes to a newly-created or edited User -- before the changes are
    # committed to the database.
    def on_model_change(self, form, model, is_created):

        # If the password field isn't blank...
        if len(model.password2):

            # ... then encrypt the new password prior to storing it in the database. If the password field is blank,
            # the existing password in the database will be retained.
            model.password = utils.encrypt_password(model.password2)


# Customized Role model for SQL-Admin
class RoleAdmin(sqla.ModelView):

    # Prevent administration of Roles unless the currently logged-in user has the "admin" role
    def is_accessible(self):
        return current_user.has_role('admin')

class MyAnnotations(BaseView):
    @expose('/')
    @login_required
    def index(self):
        return self.render('concordance-results.html')


@app.route('/')
@login_required
def home():
    return render_template('test.html')


class AnnotationModelView(ModelView):
    column_filters = ('notes',)
    column_searchable_list = ('notes',)


admin = Admin(app)
# admin.add_view(MyAnnotations(name="Test"))
admin.add_view(AnnotationModelView(Annotation, db.session))
admin.add_view(ModelView(Category, db.session))
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Role, db.session))
admin.add_view(ModelView(List, db.session))
# Add Flask-Admin views for Users and Roles
# admin.add_view(UserAdmin(User, db.session))
# admin.add_view(RoleAdmin(Role, db.session))

if __name__ == "__main__":

    @app.before_first_request
    def initialize_database():
        db.create_all()
    
    app.run()
