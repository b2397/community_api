# from app import db, ma
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref
from marshmallow import fields
from flask_marshmallow import Marshmallow
from datetime import datetime
from marshmallow_sqlalchemy.schema import *  #SQLAlchemyAutoSchema, auto_field

# Init db
db = SQLAlchemy()
# db = SQLAlchemy(app)

# Init ma
ma = Marshmallow()

# ma = Marshmallow(app)


# User Class/Model
class User(db.Model):
    __tablename__ = "Users"
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(100), unique=True)
    # datetime_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    datetime_created = db.Column(db.DateTime, default=datetime.utcnow)
    datetime_updated = db.Column(db.DateTime, onupdate=datetime.utcnow)
    # questions = db.relationship("Question", backref="user", passive_deletes=True)


# def __init__(self, user_name):
#     self.user_name = user_name


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_relationships = True
        load_instance = True


'''
# User Schema
class UserSchema(ma.ModelSchema):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class Meta:
        model = User
        # sqla_session = db.session
'''


# Question Class/Model
class Question(db.Model):
    __tablename__ = "Questions"
    question_id = db.Column(db.Integer, primary_key=True)
    question_title = db.Column(db.String(200), nullable=False)
    question_text = db.Column(db.String(1000))
    user_id = db.Column(db.Integer, db.ForeignKey('Users.user_id', ondelete='CASCADE'), nullable=False)
    # user_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'), nullable=False)
    # user_id = db.Column(db.Integer, db.ForeignKey('Users.user_id', ondelete='CASCADE'))
    user = db.relationship("User", lazy='subquery', backref=backref("questions", passive_deletes='all'))
    # user = db.relationship("User", backref='questions', cascade='all,delete')
    datetime_created = db.Column(db.DateTime, default=datetime.utcnow)
    datetime_updated = db.Column(db.DateTime, onupdate=datetime.utcnow)

    # def __init__(self, q_title, q_text, user_id):
    #     self.q_title = q_title
    #     self.q_text = q_text
    #     self.user_id = user_id

    # def __repr__(self):
    #     return "<Question(title={self.q_title!r})>".format(self=self)


class QuestionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Question
        include_fk = True
        include_relationships = True
        load_instance = True


'''
# Question Schema
class QuestionSchema(ma.ModelSchema):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class Meta:
        model = Question
        include_fk = True
'''


# Answer Class/Model
class Answer(db.Model):
    __tablename__ = "Answers"
    answer_id = db.Column(db.Integer, primary_key=True)
    answer_text = db.Column(db.String(1000), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('Questions.question_id', ondelete='CASCADE'), nullable=False)
    question = db.relationship("Question", lazy='subquery', backref=backref("answers", passive_deletes='all'))
    user_id = db.Column(db.Integer, db.ForeignKey('Users.user_id', ondelete='CASCADE'), nullable=False)
    user = db.relationship("User", lazy='subquery', backref=backref("answers", passive_deletes='all'))
    datetime_created = db.Column(db.DateTime, default=datetime.utcnow)
    datetime_updated = db.Column(db.DateTime, onupdate=datetime.utcnow)


# Answer Schema
class AnswerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Answer
        include_fk = True
        include_relationships = True
        load_instance = True


'''
# Answer Schema
class AnswerSchema(ma.ModelSchema):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class Meta:
        model = Answer
        include_fk = True
'''


# BM_User_x_Question Class/Model
class BM_User_x_Question(db.Model):
    __tablename__ = "BM_Users_x_Questions"
    # bm_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.user_id', ondelete='CASCADE'), primary_key=True)
    user = db.relationship("User", lazy='subquery', backref=backref("question_bookmarks", passive_deletes='all'))
    question_id = db.Column(db.Integer, db.ForeignKey('Questions.question_id', ondelete='CASCADE'), primary_key=True)
    question = db.relationship("Question", lazy='subquery', backref=backref("bookmarks", passive_deletes='all'))
    datetime_created = db.Column(db.DateTime, default=datetime.utcnow)
    datetime_updated = db.Column(db.DateTime, onupdate=datetime.utcnow)


# BM_User_x_Question Schema
class BM_User_x_QuestionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = BM_User_x_Question
        # include_fk = True
        # include_relationships = True
        load_instance = True

    # user_id = fields.Int()
    # question_id = fields.Int()
    # datetime_created = auto_field
    # datetime_updated = auto_field


# BM_User_x_Answer Class/Model
class BM_User_x_Answer(db.Model):
    __tablename__ = "BM_Users_x_Answers"
    # bm_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.user_id', ondelete='CASCADE'), primary_key=True)
    user = db.relationship("User", lazy='subquery', backref=backref("answer_bookmarks", passive_deletes='all'))
    answer_id = db.Column(db.Integer, db.ForeignKey('Answers.answer_id', ondelete='CASCADE'), primary_key=True)
    answer = db.relationship("Answer", lazy='subquery', backref=backref("bookmarks", passive_deletes='all'))
    datetime_created = db.Column(db.DateTime, default=datetime.utcnow)
    datetime_updated = db.Column(db.DateTime, onupdate=datetime.utcnow)


# BM_User_x_Answer Schema
class BM_User_x_AnswerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = BM_User_x_Answer
        load_instance = True