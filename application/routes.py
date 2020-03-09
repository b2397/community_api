from flask import Flask, request, jsonify, make_response, abort, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from datetime import datetime

from .models import *
from sqlalchemy.exc import IntegrityError
from marshmallow import exceptions as marshe

# Blueprints for all routes
users_blueprint = Blueprint('users_blueprint', __name__, url_prefix='/users')
questions_blueprint = Blueprint('questions_blueprint', __name__, url_prefix='/questions')
answers_blueprint = Blueprint('answers_blueprint', __name__, url_prefix='/answers')
bmuqs_blueprint = Blueprint('bmuqs_blueprint', __name__, url_prefix='/bmuqs')
bmuas_blueprint = Blueprint('bmuas_blueprint', __name__, url_prefix='/bmuas')

################################################################################################
# GET
################################################################################################


# Get All Users
# @users_blueprint.route('/', methods=['GET'])
@users_blueprint.route('/', methods=['GET'])
def get_users():
    # offset=1&limit=3
    all_users = User.query.all()
    users_schema = UserSchema(many=True)
    # result = users_schema.dump(all_users)
    # return jsonify(result)
    return users_schema.jsonify(all_users)


# Get All Questions
@questions_blueprint.route('/', methods=['GET'])
def get_questions():
    all_questions = Question.query.all()
    schema = QuestionSchema(many=True)
    return schema.jsonify(all_questions)


# Get All Answers
@answers_blueprint.route('/', methods=['GET'])
def get_answers():
    all_answers = Answer.query.all()
    schema = AnswerSchema(many=True)
    return schema.jsonify(all_answers)


# Get Single User
@users_blueprint.route('/<user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.filter_by(user_id=user_id).first_or_404(description=f"Failure. user_id:{user_id} not found.")
    user_schema = UserSchema()
    # dump_data = user_schema.dump(user)
    return user_schema.jsonify(user)


# Get Single Question
@questions_blueprint.route('/<question_id>', methods=['GET'])
def get_question(question_id):
    question = Question.query.filter_by(question_id=question_id).first_or_404(
        description=f"Failure. question_id:{question_id} not found.")
    # question = Question.query.get(question_id)
    question_schema = QuestionSchema()
    return question_schema.jsonify(question)


# Get Single Answer
@answers_blueprint.route('/<answer_id>', methods=['GET'])
def get_answer(answer_id):
    answer = Answer.query.filter_by(answer_id=answer_id).first_or_404(
        description=f"Failure. answer_id:{answer_id} not found.")
    # answer = Answer.query.get(answer_id)
    answer_schema = AnswerSchema()
    return answer_schema.jsonify(answer)


# Get all Questions for a single User
@users_blueprint.route('/<user_id>/questions', methods=['GET'])
def get_user_questions(user_id):
    user = User.query.get_or_404(ident=user_id, description=f"Failure. user_id:{user_id} not found.")
    # user = User.query.filter_by(user_id=user_id).get_or_404(description=f"Failure. user_id:{user_id} not found.")
    # for question in user.questions:
    #     print(question.question_title)
    schema = QuestionSchema(many=True)
    # dump_data = user_schema.dump(user)
    return schema.jsonify(user.questions)


# Get all Answers for a single Question
@questions_blueprint.route('/<question_id>/answers', methods=['GET'])
def get_answers_for_question(question_id):
    question = Question.query.get_or_404(ident=question_id,
                                         description=f"Failure. question_id:{question_id} not found.")
    schema = AnswerSchema(many=True)
    return schema.jsonify(question.answers)


# Get all bookmarked Questions for a single User
@users_blueprint.route('/<user_id>/bmuqs', methods=['GET'])
def get_bmuqs(user_id):
    user = User.query.get_or_404(ident=user_id, description=f"Failure. user_id:{user_id} not found.")
    schema = QuestionSchema(many=True)
    return schema.jsonify(user.question_bookmarks)


# Get all bookmarked Answers for a single User
@users_blueprint.route('/<user_id>/bmuas', methods=['GET'])
def get_bmuas(user_id):
    user = User.query.get_or_404(ident=user_id, description=f"Failure. user_id:{user_id} not found.")
    schema = AnswerSchema(many=True)
    return schema.jsonify(user.answer_bookmarks)


################################################################################################
# CREATE / POST
################################################################################################


# Create a User
@users_blueprint.route('/', methods=['POST'])
def add_user():
    new_user_data = request.get_json()
    schema = UserSchema()
    try:
        new_user = schema.load(new_user_data)
    except marshe.ValidationError as e:
        abort(400, e.messages)

    # Check for an existing user in the database
    existing_user = (User.query.filter(User.user_name == new_user.user_name).one_or_none())

    # If the user doesn't exist in the database, add them, otherwise abort
    if existing_user is None:
        # Add the user to the database
        db.session.add(new_user)
        db.session.commit()

        # return the serialized new user data, response code 201
        return schema.jsonify(new_user), 201

    else:
        abort(409, f"Failure. user_name:{new_user.user_name} already exists.")


# Create a Question
@questions_blueprint.route('/', methods=['POST'])
def add_question():
    new_question_data = request.get_json()
    schema = QuestionSchema()

    try:
        new_question = schema.load(new_question_data)
    except marshe.ValidationError as e:
        print(e)
        abort(400, e.messages)

    db.session.add(new_question)
    db.session.commit()
    return schema.jsonify(new_question), 201


# Create an Answer
@answers_blueprint.route('/', methods=['POST'])
def add_answer():
    new_answer_data = request.get_json()
    schema = AnswerSchema()

    try:
        new_answer = schema.load(new_answer_data)
    except marshe.ValidationError as e:
        print(e)
        abort(400, e.messages)

    db.session.add(new_answer)
    db.session.commit()
    return schema.jsonify(new_answer), 201


# Create a BM_User_x_Question
@bmuqs_blueprint.route('/', methods=['POST'])
def add_bmuq():
    new_bmuq = BM_User_x_Question()
    setattr(new_bmuq, 'user_id', request.json['user_id'])
    setattr(new_bmuq, 'question_id', request.json['question_id'])
    try:
        db.session.add(new_bmuq)
        db.session.commit()
    except Exception as e:
        abort(400, str(e.orig))
    return make_response(jsonify({'message': 'Question has been bookmarked.'}), 201)


# Create a BM_User_x_Answer
@bmuas_blueprint.route('/', methods=['POST'])
def add_bmua():
    new_bmua = BM_User_x_Answer()
    setattr(new_bmua, 'user_id', request.json['user_id'])
    setattr(new_bmua, 'answer_id', request.json['answer_id'])
    try:
        db.session.add(new_bmua)
        db.session.commit()
    except Exception as e:
        abort(400, str(e.orig))
    return make_response(jsonify({'message': 'Answer has been bookmarked.'}), 201)


################################################################################################
# UPDATE / PUT
################################################################################################


# Update a User
@users_blueprint.route('/<user_id>', methods=['PUT'])
def update_user(user_id):
    # Get the user to be updated from the db, or 404 if not found
    user = User.query.filter_by(user_id=user_id).first_or_404(description=f"Failure. user_id:{user_id} not found.")

    update_user_data = request.get_json()
    user_schema = UserSchema()
    try:
        update_user = user_schema.load(update_user_data)
    except marshe.ValidationError as e:
        abort(400, e.messages)

    user.user_name = update_user.user_name
    db.session.commit()
    return user_schema.jsonify(user)


# Update a Question
@questions_blueprint.route('/<question_id>', methods=['PUT'])
def update_question(question_id):
    # Get the question to be updated from the db, or 404 if not found
    question = Question.query.filter_by(question_id=question_id).first_or_404(
        description=f"Failure. question_id:{question_id} not found.")

    data = request.get_json()
    columns = ['question_text', 'question_title']
    for column_name in columns:
        for key in data:
            if column_name == key:
                setattr(question, column_name, data.get(key))

    db.session.commit()

    question_schema = QuestionSchema()
    data = question_schema.jsonify(question)

    return data


# Update an Answer
@answers_blueprint.route('/<answer_id>', methods=['PUT'])
def update_answer(answer_id):
    # Get the answer to be updated from the db, or 404 if not found
    answer = Answer.query.filter_by(answer_id=answer_id).first_or_404(
        description=f"Failure. answer_id:{answer_id} not found.")

    answer.answer_text = request.json['answer_text']
    db.session.commit()

    answer_schema = AnswerSchema()
    data = answer_schema.jsonify(answer)
    return data


################################################################################################
# DELETE
################################################################################################


# Delete a User
@users_blueprint.route('/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    # Get the user requested for deletion
    user = User.query.filter_by(user_id=user_id).first_or_404(description=f"Failure. user_id:{user_id} not found.")
    db.session.delete(user)
    db.session.commit()

    user_schema = UserSchema()
    return user_schema.jsonify(user)


# Delete a Question
@questions_blueprint.route('/<question_id>', methods=['DELETE'])
def delete_question(question_id):
    # Get the question requested for deletion
    question = Question.query.filter_by(question_id=question_id).first_or_404(
        description=f"Failure. question_id:{question_id} not found.")
    db.session.delete(question)
    db.session.commit()

    schema = QuestionSchema()
    return schema.jsonify(question)


# Delete an Answer
@answers_blueprint.route('/<answer_id>', methods=['DELETE'])
def delete_answer(answer_id):
    # Get the answer requested for deletion
    answer = Answer.query.filter_by(answer_id=answer_id).first_or_404(
        description=f"Failure. answer_id:{answer_id} not found.")
    db.session.delete(answer)
    db.session.commit()

    schema = AnswerSchema()
    return schema.jsonify(answer)


# Delete a BM_User_x_Question
@users_blueprint.route('/<user_id>/bmuqs/<question_id>', methods=['DELETE'])
def delete_bmuq(user_id, question_id):
    # Get the bmuq requested for deletion
    bmuq = BM_User_x_Question.query.filter_by(user_id=user_id, question_id=question_id).first_or_404(
        description=f"Failure. Bookmark not found for user_id:{user_id} and question_id:{question_id}.")
    db.session.delete(bmuq)
    db.session.commit()

    return make_response(jsonify({'message': 'Bookmarked question deleted.'}), 200)


# Delete a BM_User_x_Answer
@users_blueprint.route('/<user_id>/bmuas/<answer_id>', methods=['DELETE'])
def delete_bmua(user_id, answer_id):
    # Get the bmua requested for deletion
    bmua = BM_User_x_Answer.query.filter_by(user_id=user_id, answer_id=answer_id).first_or_404(
        description=f"Failure. Bookmark not found for user_id:{user_id} and answer_id:{answer_id}.")
    db.session.delete(bmua)
    db.session.commit()

    return make_response(jsonify({'message': 'Bookmarked answer deleted.'}), 200)
