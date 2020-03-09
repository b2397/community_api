import pytest
import json
import os
from application import create_app
from application.models import db


@pytest.fixture
def client():
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    DATABASE_NAME = 'test1.db'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, DATABASE_NAME)
    app = create_app({'SQLALCHEMY_DATABASE_URI' : SQLALCHEMY_DATABASE_URI})
    # app.app_context().push()
    # db.drop_all()
    # db.create_all()
    client = app.test_client()
    yield client


####################################################################
# Test POSTs / Creates
####################################################################

def test_post_user(client):
    user_name = 'user_test_1'
    url = '/users/'
    mock_request_data = {'user_name': user_name}
    request_data = json.dumps(mock_request_data)
    response = client.post(url, data=request_data, content_type='application/json')
    assert response.status_code == 201

def test_post_question(client):
    user_id = 1
    question_title = 'Test question 1 title?'
    question_text = 'Test question 1 text...'
    url = '/questions/'
    mock_request_data = {'user_id': user_id,
                         'question_title': question_title,
                         'question_text': question_text}
    request_data = json.dumps(mock_request_data)
    response = client.post(url, data=request_data, content_type='application/json')
    assert response.status_code == 201

def test_post_answer(client):
    user_id = 1
    question_id = 1
    answer_text = 'Answer text 1'
    url = '/answers/'
    mock_request_data = {'user_id': user_id,
                         'question_id': question_id,
                         'answer_text': answer_text}
    request_data = json.dumps(mock_request_data)
    response = client.post(url, data=request_data, content_type='application/json')
    assert response.status_code == 201

def test_post_bookmarked_question(client):
    user_id = 1
    question_id = 1
    url = f'/bmuqs/'
    mock_request_data = {'user_id': user_id,
                         'question_id': question_id}
    request_data = json.dumps(mock_request_data)
    response = client.post(url, data=request_data, content_type='application/json')
    assert response.status_code == 201

def test_post_bookmarked_answer(client):
    user_id = 1
    answer_id = 1
    url = f'/bmuas/'
    mock_request_data = {'user_id': user_id,
                         'answer_id': answer_id}
    request_data = json.dumps(mock_request_data)
    response = client.post(url, data=request_data, content_type='application/json')
    assert response.status_code == 201

####################################################################
# Test PUTs / Updates
####################################################################

def test_update_user(client):
    user_id = 1
    user_name = 'user_test_1_updated'
    url = f'/users/{user_id}'
    mock_request_data = {'user_name': user_name}
    request_data = json.dumps(mock_request_data)
    response = client.put(url, data=request_data, content_type='application/json')
    assert response.status_code == 200

def test_update_question(client):
    question_title = 'Updated title'
    question_text = 'Updated text'
    question_id = 1
    url = f'/questions/{question_id}'
    mock_request_data = {'question_id': question_id,
                         'question_title': question_title,
                         'question_text': question_text}
    request_data = json.dumps(mock_request_data)
    response = client.put(url, data=request_data, content_type='application/json')
    assert response.status_code == 200

def test_update_answer(client):
    answer_text = 'Updated answer text'
    answer_id = 1
    url = f'/answers/{answer_id}'
    mock_request_data = {'answer_text': answer_text}
    request_data = json.dumps(mock_request_data)
    response = client.put(url, data=request_data, content_type='application/json')
    assert response.status_code == 200

####################################################################
# Test GETs
####################################################################

def test_get_users(client):
    url = '/users/'
    response = client.get(url)
    assert response.status_code == 200

def test_get_user(client):
    user_id = 1
    url = f'/users/{user_id}'
    response = client.get(url)
    assert response.status_code == 200

def test_get_user_questions(client):
    user_id = 1
    url = f'/users/{user_id}/questions'
    response = client.get(url)
    assert response.status_code == 200

def test_get_question_answers(client):
    question_id = 1
    url = f'/questions/{question_id}/answers'
    response = client.get(url)
    assert response.status_code == 200

def test_get_user_bookmarked_questions(client):
    user_id = 1
    url = f'/users/{user_id}/bmuqs'
    response = client.get(url)
    assert response.status_code == 200

def test_get_user_bookmarked_answers(client):
    user_id = 1
    url = f'/users/{user_id}/bmuas'
    response = client.get(url)
    assert response.status_code == 200


def test_get_user_fail(client):
    user_id = 2
    url = f'/users/{user_id}'
    response = client.get(url)
    assert response.status_code == 404

def test_get_question_fail(client):
    question_id = 2
    url = f'/questions/{question_id}'
    response = client.get(url)
    assert response.status_code == 404

def test_get_answer_fail(client):
    answer_id = 2
    url = f'/answers/{answer_id}'
    response = client.get(url)
    assert response.status_code == 404

def test_post_duplicate_user_fail(client):
    user_name = 'user_test_1_updated'
    url = '/users/'
    mock_request_data = {'user_name': user_name}
    request_data = json.dumps(mock_request_data)
    response = client.post(url, data=request_data, content_type='application/json')
    assert response.status_code == 409


####################################################################
# Test DELETEs
####################################################################
def test_delete_bookmarked_answer(client):
    user_id = 1
    answer_id = 1
    url = f'/users/{user_id}/bmuas/{answer_id}'
    response = client.delete(url)
    assert response.status_code == 200

def test_delete_bookmarked_question(client):
    user_id = 1
    question_id = 1
    url = f'/users/{user_id}/bmuqs/{question_id}'
    response = client.delete(url)
    assert response.status_code == 200

def test_delete_answer(client):
    answer_id = 1
    url = f'/answers/{answer_id}'
    response = client.delete(url)
    assert response.status_code == 200

def test_delete_question(client):
    question_id = 1
    url = f'/questions/{question_id}'
    response = client.delete(url)
    assert response.status_code == 200

def test_delete_user(client):
    user_id = 1
    url = f'/users/{user_id}'
    response = client.delete(url)
    assert response.status_code == 200