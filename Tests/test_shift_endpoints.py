from datetime import datetime
from Main.Congregation.models import Congregation
from Main.Shift.models import Shift
from Main.User.models import User


# Shift Endpoints
def test_get_shifts(client):
    congregation = Congregation.objects().first()
    cong_id = str(congregation.id)
    response = client.get(f'/congregations/{cong_id}/shifts/')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    assert data[0]["location"] == "UConn"


def test_post_shifts(client):
    congregation = Congregation.objects().first()
    cong_id = str(congregation.id)
    assert len(congregation.shifts) == 1
    payload = {
        "location": "Dam trail",
        "datetime": "2017-06-01T08:30"
    }
    response = client.post(f'/congregations/{cong_id}/shifts/',
                           json=payload)
    assert response.status_code == 200
    # Check that shift is created in db w appropriate associations
    shift = Shift.objects().order_by('-id').first()
    assert shift.location == "Dam trail"
    assert shift.congregation.name == "English - Willimantic"
    congregation = Congregation.objects().first()
    assert len(congregation.shifts) == 2
    assert congregation.shifts[1].location == "Dam trail"
    # Check that response contains correct shift data
    data = response.get_json()
    assert data["location"] == "Dam trail"
    assert len(data["volunteers"]) == 0
    assert len(data["requested_by"]) == 0


def test_get_shift(client):
    congregation = Congregation.objects().first()
    cong_id = str(congregation.id)
    shift = Shift.objects().first()
    shift_id = str(shift.id)
    response = client.get(f'/congregations/{cong_id}/shifts/{shift_id}')
    assert response.status_code == 200
    # Create a new congregation - should return 401
    # if shift doesn't belong to congregation
    congregation = Congregation(name="sneaky").save()
    cong_id = str(congregation.id)
    response = client.get(f'/congregations/{cong_id}/shifts/{shift_id}')
    assert response.status_code == 401


def test_put_shift(client):
    congregation = Congregation.objects().first()
    cong_id = str(congregation.id)
    shift = Shift.objects().first()
    shift_id = str(shift.id)
    response = client.put(f'/congregations/{cong_id}/shifts/{shift_id}',
                          json={"location": "Dam trail"})
    assert response.status_code == 200
    data = response.get_json()
    assert data["location"] == "Dam trail"


def test_delete_shift(client):
    congregation = Congregation.objects().first()
    cong_id = str(congregation.id)
    assert len(congregation.shifts) == 1
    shift = Shift.objects().first()
    shift_id = str(shift.id)
    response = client.delete(f'/congregations/{cong_id}/shifts/{shift_id}')
    assert response.status_code == 200
    congregation = Congregation.objects().first()
    assert len(congregation.shifts) == 0
    assert len(Shift.objects()) == 0
