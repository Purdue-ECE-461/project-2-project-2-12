# this file uses pytest to test very basic api functions

import requests
from requests.structures import CaseInsensitiveDict

base_url = "https://ece-461-pyapi.ue.r.appspot.com/"
# base_url = "https://f790d989-aec9-4c93-b260-3e206f2559d4.mock.pstmn.io/"

def get_token():
    url = base_url + "authenticate"
    headers = {'Content-type': 'application/json'}
    raw_data = '{ "User": { "name": "ece461defaultadmin", "isAdmin": true }, "Secret": { "password": "correcthorsebatterystaple123(!__+@**(A" } }'
    response = requests.put(url, data=raw_data, headers=headers)
    assert response.text
    token = response.text
    i = 14 
    new_token = ''
    while (len(new_token) < 143):
        new_token = new_token + token[i]
        i += 1
    return new_token

def test_put_create_auth_token(): #1
    headers = {'Content-type': 'application/json'}
    raw_data = '{ "User": { "name": "ece461defaultadmin", "isAdmin": true }, "Secret": { "password": "correcthorsebatterystaple123(!__+@**(A" } }'
    url = base_url + "authenticate"
    response = requests.put(url, data=raw_data, headers=headers)
    assert response.status_code == 201

def test_getPackages_url_status(): #2
    response = requests.get(base_url + "getPackages")
    assert response.status_code == 200

def test_post_package_create(): #3
    token = get_token()
    # token = 'bearer '+token
    url = base_url + "package"
    raw_data = '{ "metadata": { "Name": express, "Version": 1, "ID": express }, "data": { "Content": express, "URL": https://github.com/expressjs/express, "JSProgram": "if (process.argv.length === 7) {\nconsole.log("Success")\nprocess.exit(0)\n} else {\nconsole.log("Failed")\nprocess.exit(1)\n}\n" } }'
    # raw_data = '{"metadata": { "Name": "Underscore", "Version": "1.0.0", "ID": "underscore" }, "data": { "URL": "https://github.com/jashkenas/underscore", "JSProgram": "if (process.argv.length === 7) {\nconsole.log("\""Success"\"")\nprocess.exit(0)\n} else {\nconsole.log("\""Failed"\"")\nprocess.exit(1)\n}\n" } }'
    headers = {'X-Authorization': token}
    response = requests.post(url, headers=headers, data=raw_data)
    assert response.status_code == 200 #500

def test_get_package(): 
    token = get_token()
    headers = {'X-Authorization': token}
    response = requests.get(base_url + "package/express", headers=headers)
    assert response.status_code == 200

def test_get_package_rate():
    token = get_token()
    headers = {'X-Authorization': token}
    url = base_url + "package/express/rate"
    response = requests.get(url, headers=headers)
    assert response.headers.get('content-type').startswith('application/json')

def test_get_package_byName():
    token = get_token()
    headers = {'X-Authorization': token}
    url = base_url + "package/express/underscore"
    response = requests.get(url, headers=headers)
    assert response.headers.get('content-type').startswith('application/json')

def test_delete_package():
    token = get_token()
    headers = {'X-Authorization': token}
    url = base_url + "package/express"
    response = requests.delete(url, headers=headers)
    assert response.status_code == 200

def test_put_package(): 
    url = base_url + "package/express"
    token = get_token()
    headers = {'X-Authorization': token, 'Content-type': 'application/json'}
    raw_data = '{ "metadata": { "Name": express, "Version": 1, "ID": express }, "data": { "Content": express, "URL": https://github.com/expressjs/express, "JSProgram": "if (process.argv.length === 7) {\nconsole.log("Success")\nprocess.exit(0)\n} else {\nconsole.log("Failed")\nprocess.exit(1)\n}\n" } }'
    response = requests.put(url, data=raw_data, headers=headers)
    assert response.status_code == 200
        
def test_post_get_packages():
    url = base_url + "packages?offset=2"
    token = get_token()
    headers = {'X-Authorization' : token}
    response = requests.post(url, headers=headers)
    assert response.status_code == 200

def test_del_package_byName():
    token = get_token()
    headers = {'X-Authorization': token}
    url = base_url + "package/byName/express"
    response = requests.delete(url, headers=headers)
    assert response.status_code == 200

def test_post_package_ingest():
    token = get_token()
    url = base_url + "package"
    raw_data = '{ "metadata": { "Name": express, "Version": 1, "ID": express }, "data": { "Content": express, "URL": https://github.com/expressjs/express, "JSProgram": "if (process.argv.length === 7) {\nconsole.log("Success")\nprocess.exit(0)\n} else {\nconsole.log("Failed")\nprocess.exit(1)\n}\n" } }'
    headers = {'X-Authorization' : token}
    response = requests.post(url, data=raw_data, headers=headers)
    assert response.status_code == 200

def test_del_reg_reset():
    url = base_url + "reset"
    token = get_token()
    headers = {'X-Authorization': token}
    response = requests.delete(url, headers=headers)
    assert response.status_code == 200

'''
unused debugging functions
token = get_token()
token = 'bearer '+token
print(token)
'{ "metadata": { "Name": "express", "Version": "4.17.1", "ID": "express" }, "data": { "Content": "test", "URL": "https://github.com/expressjs/express.git", "JSProgram": "if (process.argv.length === 7) {\nconsole.log("Success")\nprocess.exit(0)\n} else {\nconsole.log("Failed")\nprocess.exit(1)\n}\n" } }'
{
    "metadata": {
        "Name": package.name,
        "Version": package.version,
        "ID": package.id
    },
    "data": {
        "Content": package.content,
        "URL": package.url,
        "JSProgram": "if (process.argv.length === 7) {\nconsole.log('Success')\nprocess.exit(0)\n} else {\nconsole.log('Failed')\nprocess.exit(1)\n}\n"
    }
}

'{ "metadata": { "Name": express, "Version": 1, "ID": express }, "data": { "Content": express, "URL": https://github.com/expressjs/express, "JSProgram": "if (process.argv.length === 7) {\nconsole.log("Success")\nprocess.exit(0)\n} else {\nconsole.log("Failed")\nprocess.exit(1)\n}\n" } }'
'{ "metadata": { "Name": package.name, "Version": package.version, "ID": package.id }, "data": { "Content": package.content, "URL": package.url, "JSProgram": "if (process.argv.length === 7) {\nconsole.log("Success")\nprocess.exit(0)\n} else {\nconsole.log("Failed")\nprocess.exit(1)\n}\n" } }'
'''