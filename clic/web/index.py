from __future__ import absolute_import

from flask import Flask, render_template, url_for, redirect, request
import os
from werkzeug import secure_filename
from flask_admin import AdminIndexView
from flask.ext.security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin, login_required
from flask.ext.admin.contrib import sqla
from flask_admin import Admin, BaseView, expose, AdminIndexView
from flask_mail import Mail
from flask_admin.contrib.sqla import ModelView
from flask_security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin, login_required, current_user
# from flask.ext.login import LoginManager

from clic.web.api import api, fetchClusters, fetchKeywords
from clic.chapter_repository import ChapterRepository
from clic.web.forms import BOOKS, SUBSETS
from models import db, Annotation, Category, Role, User, List, Tag, Note, Subset


# app = Flask('clic.web', static_url_path='')
app = Flask(__name__, static_url_path='')
app.register_blueprint(api, url_prefix='/api')
app.config.from_pyfile('config.py')
mail = Mail(app)
db.init_app(app)
# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

# login_manager = LoginManager()
# login_manager.init_app(app)

# @login_manager.user_loader
# def load_user(user_id):
#    return User.get(user_id)


'''
Application routes
'''

#==============================================================================
# Home, about, docs, 404
#==============================================================================
@app.route('/', methods=['GET'])
def index():
    return redirect(url_for('concordances')) # current home page. may change

@app.route('/about/', methods=['GET'])
def about():
    return render_template("info/about.html")

@app.route('/documentation/', methods=['GET'])
def documentation():
    return render_template("info/documentation.html")

@app.route('/releases/', methods=['GET'])
def releases():
    return render_template("info/releases.html")

@app.route('/blog/', methods=['GET'])
def blog():
    return render_template("info/blog.html")

#==============================================================================
# Concordances
#==============================================================================
@app.route('/concordances/', methods=['GET'])
def concordances():
    if 'terms' in request.args.keys(): # form was submitted
        return render_template("concordance-results.html")
    else:
        return render_template("concordance-form.html")

#==============================================================================
# Keywords
#==============================================================================
@app.route('/keywords/', methods=['GET'])
def keywords():
    if 'testIdxGroup' in request.args.keys(): # form was submitted

        # get parameters for redirecting to the concordance page
        IdxGroup = request.args.get('testIdxGroup')
        testCollection = request.args.get('testCollection')
        testIdxMod = request.args.get('testIdxMod')
        selectWords = "whole"

        args = request.args
        keywords_result = fetchKeywords(args)

        return render_template("keywords-results.html",
                               IdxGroup=IdxGroup,
                               testCollection=testCollection,
                               testIdxMod=testIdxMod,
                               selectWords=selectWords,
                               keywords=keywords_result)

    else:
        return render_template("keywords-form.html")

#==============================================================================
# Clusters
#==============================================================================
@app.route('/clusters/', methods=['GET'])
def clusters():
    if 'testIdxGroup' in request.args.keys(): # form was submitted

        IdxGroup = request.args.get('testIdxGroup')
        # FIXME this might not work when dealing with only a few books,
        # rather than an entire subcorpus, in that case better use:
        # collection = args.getlist('testCollection') ## args is a
        ## multiDictionary: use .getlist() to access individual books
        testCollection = request.args.get('testCollection')
        testIdxMod = request.args.get('testIdxMod')
        selectWords = "whole"

        args = request.args
        clusters_result = fetchClusters(args)

        return render_template("clusters-results.html",
                               IdxGroup=IdxGroup,
                               testCollection=testCollection,
                               testIdxMod=testIdxMod,
                               selectWords=selectWords,
                               clusters=clusters_result)

    else:
        return render_template("clusters-form.html")

#==============================================================================
# Chapters
#==============================================================================
@app.route('/chapter/<book>/<int:number>/')
@app.route('/chapter/<book>/<int:number>/<int:word_index>/<search_term>/')
def chapterView(number, book, word_index=None, search_term=None):
    chapter_repository = ChapterRepository()

    if word_index is None:
        chapter, book_title = chapter_repository.get_chapter(number, book)
    else:
        chapter, book_title = chapter_repository.get_chapter_with_highlighted_search_term(number, book, word_index, search_term)

    return render_template("chapter-view.html", content=chapter, book_title=book_title)

#==============================================================================
# Subsets
#==============================================================================
@app.route('/subsets/', methods=["GET"])
def subsets():
    """
    This is a quick and dirty method to display the subsets in our db.
    It now uses GET parameters, but should probably use POST parameters
    ideally.
    The basic design for POST parameters was almost ready but there were a
    few issues.
    """


    book = request.args.get('book')
    subset = request.args.get('subset')

    if book and subset:
        return redirect(url_for('subsets_display',
                                book=book,
                                subset=subset))

    return render_template("subsets-form.html")


@app.route('/subsets/<book>/<subset>/', methods=["GET", "POST"])
def subsets_display(book=None, subset=None):

    if book and subset:
        # make sure they are not malicious names
        book = secure_filename(book)
        subset = secure_filename(subset)

        if book not in BOOKS:
            return redirect(url_for('page_not_found'))

        if subset not in SUBSETS:
            return redirect(url_for('page_not_found'))

        BASE_DIR = os.path.dirname(__file__)
        filename = "../textfiles/{0}/{1}_{0}.txt".format(subset, book)
        with open(os.path.join(BASE_DIR, filename), 'r') as the_file:
            result = the_file.readlines()

        return render_template("subsets-results.html",
                               book=book,
                               subset=subset,
                               result=result,
                               )

    else:
        return redirect(url_for('subsets'))

#==============================================================================
# 404
#==============================================================================
@app.errorhandler(404)
def page_not_found(error):
    return render_template('page-not-found.html'), 404

#==============================================================================
# User annotation of subsets using Flask_admin
#==============================================================================

# limit the access to user that can log in
# https://github.com/flask-admin/flask-admin/issues/1049 or better:
# https://github.com/flask-admin/flask-admin/blob/master/examples/auth/app.py

# Create customized model view class
class SecuredModelView(sqla.ModelView):

    def is_accessible(self):
        if not current_user.is_active() or not current_user.is_authenticated():
            return False

        if current_user.has_role('superuser'):
            return True

        return False

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when a view is not accessible.
        """
        if not self.is_accessible():
            if current_user.is_authenticated():
                # permission denied
                abort(403)
            else:
                # login
                return redirect(url_for('security.login', next=request.url))

# @security.context_processor
# def security_context_processor():
#     return dict(
#         admin_base_template=admin.base_template,
#         admin_view=admin.index_view,
#         h=admin_helpers,
#     )


from flask_admin.contrib.sqla import tools
from sqlalchemy import or_

class PhraseSearchModelView(ModelView):

    # https://github.com/flask-admin/flask-admin/blob/master/flask_admin/contrib/sqla/tools.py
    # https://github.com/flask-admin/flask-admin/blob/master/flask_admin/contrib/sqla/view.py#L804
    # https://github.com/flask-admin/flask-admin/blob/master/flask_admin/templates/bootstrap3/admin/model/layout.html

    def _apply_search(self, query, count_query, joins, count_joins, search):
        """
            Apply search to a query.
        """
        # just disable the split to make it work
        terms = search.split(' ')

        for term in terms:
            if not term:
                continue

            stmt = tools.parse_like_term(term)

            filter_stmt = []
            count_filter_stmt = []

            for field, path in self._search_fields:
                query, joins, alias = self._apply_path_joins(query, joins, path, inner_join=False)

                count_alias = None

                if count_query is not None:
                    count_query, count_joins, count_alias = self._apply_path_joins(count_query,
                                                                                   count_joins,
                                                                                   path,
                                                                                   inner_join=False)

                column = field if alias is None else getattr(alias, field.key)
                filter_stmt.append(column.ilike(stmt))

                if count_filter_stmt is not None:
                    column = field if count_alias is None else getattr(count_alias, field.key)
                    count_filter_stmt.append(column.ilike(stmt))

            query = query.filter(or_(*filter_stmt))

            if count_query is not None:
                count_query = count_query.filter(or_(*count_filter_stmt))

        return query, count_query, joins, count_joins


class SubsetModelView(PhraseSearchModelView):
    column_filters = ('book', 'abbr', 'kind', 'corpus', 'text', 'notes', 'tags')
    column_searchable_list = ('abbr', 'text',)
    column_list = ('book', 'kind', 'text', 'tags', 'notes')
    # column_list = ('book', 'text',)
    # column_exclude_list = ['abbr','corpus']
    # column_editable_list could work with the above code included, but not great
    # column_editable_list = ['tags', 'notes']
    column_hide_backrefs = False

    # editing
    edit_modal = True
    form_excluded_columns = ['book', 'abbr', 'kind', 'corpus', 'text']
    # inline_models = (Tag, Note)

    # can_view_details = True
    can_create = False
    can_delete = False  # disable model deletion
    can_edit = True  # TODO disable editable fields
    can_export = True  # FIXME
    export_max_rows = 2000

    page_size = 50  # the number of entries to display on the list view

    def is_accessible(self):
        return current_user.has_role('can_annotate')

    # def get_list_form(self):
    #     return self.scaffold_list_form(CustomFieldList)

#    def init_search( self ):
#        r = super( SubsetModelView, self ).init_search()
#        self._search_joins['tags'] = Tag.name
#        return r

# def edit_form(self, obj):
#     form = model_form(models.Product, ProductEditForm)
#    if obj.searchType:
#            param_choices = [(x.id, x.label) for x in (obj.searchType.required_fields + obj.searchType.optional_fields)]
#            form.params.choices=param_choices
#        return form(obj=obj)


class TagModelView(ModelView):
    action_disallowed_list = ['delete',]
    form_excluded_columns = ['subset',]
    column_editable_list = ['name',]

    def is_accessible(self):
        return current_user.has_role('can_annotate')


class NoteModelView(ModelView):
    action_disallowed_list = ['delete',]
    column_filters = ('note',)
    column_editable_list = ['note',]
    form_excluded_columns = ['subset',]
    column_list = ('note',)

    def is_accessible(self):
        return current_user.has_role('can_annotate')


class UserAdmin(sqla.ModelView):

    # Prevent administration of Users unless the currently logged-in user has the "superman" role
    def is_accessible(self):
       return current_user.has_role('superman')


class RoleAdmin(sqla.ModelView):

    # Prevent administration of Roles unless the currently logged-in user has the "superman" role
    def is_accessible(self):
        return current_user.has_role('superman')


admin = Admin(
    app,
    template_mode='bootstrap3',
    index_view=AdminIndexView(
        name='Documentation',
        url='/annotation',
        template="user-annotation.html",
        )
    )

admin.add_view(SubsetModelView(Subset, db.session))
admin.add_view(TagModelView(Tag, db.session))
admin.add_view(NoteModelView(Note, db.session))
admin.add_view(UserAdmin(User, db.session))
admin.add_view(RoleAdmin(Role, db.session))

if __name__ == '__main__':

    @app.before_first_request
    def initialize_database():
        db.create_all()

    from flask_debugtoolbar import DebugToolbarExtension
    app.debug = True
    toolbar = DebugToolbarExtension(app)
    app.run()
