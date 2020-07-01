import json
import pytest

from bubble.models import User
from bubble.app import create_app


@pytest.fixture(scope='module')
def app():
    app = create_app(testing=True, cli=True)
    with app.app_context():
        pass
    yield app

    # 删除建的临时库
    from pymongo import MongoClient
    client = MongoClient('localhost', 27017)
    client.drop_database('bubble_tmp')


@pytest.fixture
def admin_user(app):
    _admin = {'username': 'admin', 'email': 'admin@admin.com', 'password': 'admin'}
    user = User.objects.filter(username=_admin['username']).first()
    if not user:
        user = User.objects.create(**_admin)
    return user


@pytest.fixture
def admin_headers(admin_user, client):
    data = {
        'username': admin_user.username,
        'password': 'admin'
    }
    rep = client.post(
        '/auth/login',
        data=json.dumps(data),
        headers={'content-type': 'application/json'}
    )

    tokens = json.loads(rep.get_data(as_text=True))
    return {
        'content-type': 'application/json',
        'authorization': 'Bearer %s' % tokens['access_token']
    }


@pytest.fixture
def admin_refresh_headers(admin_user, client):
    data = {
        'username': admin_user.username,
        'password': 'admin'
    }
    rep = client.post(
        '/auth/login',
        data=json.dumps(data),
        headers={'content-type': 'application/json'}
    )

    tokens = json.loads(rep.get_data(as_text=True))
    return {
        'content-type': 'application/json',
        'authorization': 'Bearer %s' % tokens['refresh_token']
    }
