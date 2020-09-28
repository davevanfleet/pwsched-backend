from datetime import datetime
from Main.Congregation.models import Congregation
from Main.Shift.models import Shift
from Main.User.models import User


# Congreagtion Endpoints
def test_get_congregations(client):
    response = client.get('/congregations/')
    assert response.status_code == 200
    data = response.get_json()
    assert data[0]['name'] == "English - Willimantic"


def test_post_congregations(client):
    payload = {"name": "Columbia"}
    response = client.post('/congregations/',
                           json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert data['name'] == "Columbia"
    response = client.get('/congregations/')
    data = response.get_json()
    assert len(data) == 2
    assert data[1]["name"] == "Columbia"


def test_get_congregation(client):
    cong_id = str(Congregation.objects().first().id)
    response = client.get(f'/congregations/{cong_id}')
    assert response.status_code == 200
    data = response.get_json()
    assert data["name"] == "English - Willimantic"


def test_put_congregation(client):
    payload = {"name": "Not Willimantic"}
    cong_id = str(Congregation.objects().first().id)
    response = client.put(f'/congregations/{cong_id}',
                          json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert data["name"] == "Not Willimantic"


def test_delete_congregation(client):
    cong_id = str(Congregation.objects().first().id)
    response = client.delete(f'/congregations/{cong_id}')
    assert response.status_code == 200
    assert len(Congregation.objects()) == 0


# Shift Endpoints
