from flask import Flask, request
from flask_cors import CORS, cross_origin
from db import *
import base64
from datetime import datetime


# initialising the flask app
app = Flask(__name__)
cors = CORS(app)
app.config["DEBUG"] = True


@app.route('/getPackages', methods=['GET'])
@cross_origin()
def home():
    return {
        1: {'name': 'Lodash', 'url': 'https://github.com/lodash/lodash', 'rating': 0.85},
        2: {'name': 'Test1', 'url': 'https://github.com/lodash/lodash', 'rating': 0.85},
        3: {'name': 'Test2', 'url': 'https://github.com/lodash/lodash', 'rating': 0.85},
        4: {'name': 'Test3', 'url': 'https://github.com/lodash/lodash', 'rating': 0.85},
        5: {'name': 'Test4', 'url': 'https://github.com/lodash/lodash', 'rating': 0.85},
        6: {'name': 'Test5', 'url': 'https://github.com/lodash/lodash', 'rating': 0.85},
        7: {'name': 'Test6', 'url': 'https://github.com/lodash/lodash', 'rating': 0.85},
        8: {'name': 'Test7', 'url': 'https://github.com/lodash/lodash', 'rating': 0.85},
    }


@app.route('/package/<string:id>', methods=['GET', 'PUT', 'DELETE'])
def getPackageById(id):
    if request.method == 'GET':
        query_response = run_select_query(
            f'select * from packages where id="{id}"')
        print(query_response)
        if (query_response != 'No response'):
            return {
                "metadata": {
                    "Name": query_response[0],
                    "Version": query_response[1],
                    "ID": query_response[2]
                },
                "data": {
                    "Content": query_response[4],
                    "URL": query_response[3],
                    "JSProgram": "if (process.argv.length === 7) {\nconsole.log('Success')\nprocess.exit(0)\n} else {\nconsole.log('Failed')\nprocess.exit(1)\n}\n"
                }
            }
        else:
            return {}, 404
    elif request.method == 'PUT':
        json_data = request.json
        query_response = run_update_query(
            f"UPDATE packages SET content=\'{json_data['data']['Content']}\' WHERE id=\'{id}\'")

        return {}, 200
    elif request.method == 'DELETE':
        query_response = run_delete_query(
            f"DELETE FROM packages WHERE id='{id}'")

        return {}, 200


@app.route('/package/<string:id>/rate', methods=['GET'])
def get_package_rating():
    pass


@app.route('/package/byName/<string:name>', methods=['GET', 'DELETE'])
def get_package_by_name(name):
    if request.method == 'GET':
        query_response = run_select_query(
            f"select * from packages where name='{name}'")

        resp_arr = []
        for package in query_response:
            package_resp = {
                "User": {
                    "name": "EMPTY FOR NOW NEED TO FIX",
                    "isAdmin": True
                },
                "Date": package[6],
                "PackageMetadata": {
                    "Name": package[0],
                    "Version": package[1],
                    "ID": package[2]
                },
                "Action": package[5]
            }

            resp_arr.append(package_resp)

        return {'result': resp_arr}, 200

    elif request.method == 'DELETE':
        query_response = run_delete_query(
            f"delete from packages where name='{name}'")

        return {}, 200


@app.route('/package', methods=['POST'])
def packageCreate():
    if request.is_json:

        package = request.json
        data = package['data']
        meta_data = package['metadata']

        if 'Content' in data:
            query_response = run_insert_query(
                f'insert into packages(name,version,id,url,content,action,actionTime) values ("{meta_data["Name"]}", "{meta_data["Version"]}", "{meta_data["ID"]}", "", "{data["Content"]}", "CREATE", "{datetime.now()}"");')
        elif 'URL' in data:
            # This is being called
            pass
        # content = package['data']['Content']
        # decoded_bytes = base64.b64decode(content)

        # import os
        # if not os.path.exists(package['metadata']['Name']+'.zip'):
        #     with open(package['metadata']['Name']+'.zip', 'w').close():
        #         pass
        # f = open(package['metadata']['Name']+'.zip', 'wb')
        # f.write(decoded_bytes)
        # f.close()

        # upload zip file to database

        return package["metadata"], 201
    # return {"error": "Malformed request"}, 400


@app.route('/packages', methods=['POST'])
def get_packages():
    pass


@app.route('/reset', methods=['DELETE'])
def registry_reset():
    pass


@app.route('/authenticate', methods=['PUT'])
def authenticate():
    pass


if __name__ == "__main__":

    # 127.0.0.1
    app.run(host='127.0.0.1', port=8080, debug=True)
