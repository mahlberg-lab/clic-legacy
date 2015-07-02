from sqlalchemy.dialects.postgresql import JSON
from flask.ext.security import UserMixin, RoleMixin
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, backref

db = SQLAlchemy()

class Annotation(db.Model):
    __tablename__ = 'annotations'

    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(
        db.Integer,
        db.ForeignKey('annotation_categories.id', ondelete='CASCADE'),
        nullable=True
        )
    notes = db.Column(db.Text())
    public = db.Column(db.Boolean, default=True)
    # name = db.Column(db.String())
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime,
                           server_default=db.func.now(),
                           onupdate=db.func.now())
    location = db.Column(db.String(50))
    proxinfo = db.Column(db.String(50))

    def __init__(self, url=""):
        self.url = url

    def __repr__(self):
        return '<id {}>'.format(self.id)


class Category(db.Model):
    __tablename__ = "annotation_categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    approved = db.Column(db.Boolean, default=False)
    explanation = db.Column(db.Text())
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime,
                           server_default=db.func.now(),
                           onupdate=db.func.now())
    annotations = db.relationship('Annotation',
                                  backref='category',
                                  lazy='dynamic')

    def __repr__(self):
        return '{}'.format(self.name)


roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    # Flask-Login integration
    def is_authenticated(self):
        return True

    def is_active(self):
        return self.active

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def __unicode__(self):
        return self.username



class List(db.Model):

    __tablename__ = 'lists'

    id = db.Column(db.Integer, primary_key=True)
    # version =
    # public = db.Column(db.Boolean, default=False)
    # time_created = db.Column(db.DateTime, timezone=True)
    # time_modified = db.Column(db.DateTime, timezone=True)
    raw_json = db.Column(JSON)
    # text_id = Column(Integer, ForeignKey('text.id'))
    # text = relationship("Text")

    def __init__(self, url, json):
        self.url = url
        self.raw_json = json

    def __repr__(self):
        return '<id {}>'.format(self.id)

#class AnnotationB(db.Model):
#    """
#    1: one text/hook, many annotations; fk on text/hook -> annotations
#    2: one text/hook, many annotations: fk on annotations -> text/hook
#    3: many texts/hooks, many annotations: m2m
#    4: many annotations, many texts/hook, but each annotation only on one text
#
#    Text : parent
#
#    annotation : child
#
#    or do not denormalize at all, simply add columns for the location of the
#    text, the text' json, and the user
#    not a good idea
#
#    you don't go from user->annotation, but from annotation->user
#    so too you go from annotation->text even if text is the more fundamental
#    entity and annotation the more concrete.
#
#    The idea is that you are most often going to be doing CRUD operations on
#    annotations.
#
#    But at the same time you want to be able to get all the annotations for
#    a specific text.
#    """
#
#    __tablename__ = 'annotations'
#
#    id = db.Column(db.Integer, primary_key=True)
#    # or id = string= BH.c4.p2.s1
#    url = db.Column(db.String())
#    # public = db.Column(db.Boolean, default=False)
#    # hook = #TODO
#    # time_created = db.Column(db.DateTime, timezone=True)
#    # time_modified = db.Column(db.DateTime, timezone=True)
#    # raw_json = db.Column(JSON)
#    # text_id = Column(Integer, ForeignKey('text.id'))
#    # text = relationship("Text")
#
#    # result_all = db.Column(JSON)
#    # result_no_stop_words = db.Column(JSON)
#
#    # def __init__(self, url, result_all, result_no_stop_words):
#    def __init__(self, url):
#        self.url = url
#        # self.result_all = result_all
#        # self.result_no_stop_words = result_no_stop_words
#
#    def __repr__(self):
#        return '<id {}>'.format(self.id)
#
#    def check_spelling(self):
#        pass
#
#    def check_near_neighbours(self):
#        pass
#
#    def strip_get_parameters(self, url):
#        pass
#
#    def last_modified(self, url):
#        pass
#
#
#class Hook(db.Model):
#
#    pass
#    # def __init__(self, #TODO):
#    #    self.a
#
#
#class Text(db.Model):
#
#    __tablename__ = 'text'
#    id = db.Column(Integer, primary_key=True)
#    annotation_id = db.Column(Integer, ForeignKey('annotation.id'))
#    annotation = db.relationship("Annotation", backref="annotations")
#
#    def check_uniqueness(self):
#        pass
