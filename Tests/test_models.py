from datetime import datetime
from Main.Congregation.models import Congregation
from Main.Shift.models import Shift
from Main.User.models import User


def test_ping(client):
    response = client.get('/ping')
    assert b'Hello, World!' in response.data


def test_create_congregation(client):
    congregation = Congregation(
        name="Test Congregation"
    )
    assert congregation.name == "Test Congregation"
    congregation.save()
    assert (Congregation.objects().order_by('-id')
            .first().name == "Test Congregation")


def test_create_shift(client):
    shift = Shift(
        location="UConn",
        datetime=datetime.now
    )
    assert shift.location == "UConn"
    shift.save()
    assert (Shift.objects().order_by('-id').first()
            .location == "UConn")


def test_create_user(client):
    user = User(
        name="Spongebob",
        email="fake2@fakemail.com",
        password="password",
        congregation=(Congregation.objects().order_by('-id')
                      .first().to_dbref())
    )
    assert user.email == "fake2@fakemail.com"
    user.save()
    assert (User.objects().order_by('-id').first()
            .email == "fake2@fakemail.com")
    assert (User.objects().order_by('-id').first()
            .congregation.name == "English - Willimantic")
