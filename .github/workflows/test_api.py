import requests

def test_getPackages_url_status():
    response = requests.get("https://ece-461-pyapi.ue.r.appspot.com/getPackages")
    assert response.status_code == 200

def test_getPackages_json():
    response = requests.get("https://ece-461-pyapi.ue.r.appspot.com/package/new")
    assert response.json()

def test_authenticate_status():
    response = requests.get("https://ece-461-pyapi.ue.r.appspot.com/authenticate")
    assert response.status_code == 200

def test_get_package_by_id():
    response = requests.get("https://ece-461-pyapi.ue.r.appspot.com/package/1")
    assert response.status_code == 200