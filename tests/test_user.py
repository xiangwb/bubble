import factory
from pytest_factoryboy import register

from bubble.models import User


@register
class UserFactory(factory.Factory):
    username = factory.Sequence(lambda n: "user{}".format(n))
    email = factory.Sequence(lambda n: "user{}@mail.com".format(n))
    password = "mypwd"

    class Meta:
        model = User


def test_get_one(client, admin_headers):
    _tmp = {'username': 'just_do_it', 'password': 'mypwd', 'active': True}
    rep = client.get("/api/v1/users/{}".format(_tmp['username']), headers=admin_headers)
    assert rep.status_code == 404
    User.objects.create(**_tmp)
    rep = client.get("/api/v1/users/{}".format(_tmp['username']), headers=admin_headers)
    assert rep.status_code == 200
    data = rep.json["user"]
    assert data["username"] == _tmp['username']


def test_put_user(client, user_factory, admin_headers):
    # test 404
    user = user_factory(username="998", password='mypwd', email='user998@mail.com')
    rep = client.put("/api/v1/users/{}".format(user.username), headers=admin_headers)
    assert rep.status_code == 404

    user.save()

    data = {"username": "updated"}

    # test update user
    rep = client.put("/api/v1/users/{}".format(user.username), json=data, headers=admin_headers)
    assert rep.status_code == 200

    data = rep.get_json()["user"]
    assert data["username"] == "updated"


def test_delete_user(client, user_factory, admin_headers):
    # test 404
    user = user_factory(username="999", password='mypwd', email='user998@mail.com')
    rep = client.delete("/api/v1/users/{}".format(user.username), headers=admin_headers)
    assert rep.status_code == 404

    user.save()

    # test get_user
    user_id = user.id
    rep = client.delete("/api/v1/users/{}".format(user.username), headers=admin_headers)
    assert rep.status_code == 200
    assert User.objects.filter(id=user_id).first() is None


def test_create_user(client, admin_headers):
    # test bad data
    data = {"username": "created"}
    rep = client.post("/api/v1/users", json=data, headers=admin_headers)
    assert rep.status_code == 400

    data["password"] = "admin"

    rep = client.post("/api/v1/users", json=data, headers=admin_headers)
    assert rep.status_code == 201

    data = rep.get_json()
    user = User.objects.filter(id=data["user"]["id"]).first()

    assert user.username == "created"


def test_get_all_user(client, user_factory, admin_headers):
    users = user_factory.create_batch(8)

    for user in users:
        user.save()

    rep = client.get("/api/v1/users", headers=admin_headers)
    assert rep.status_code == 200

    results = rep.json
    for user in users:
        assert any(u["username"] == user.username for u in results["response"])
