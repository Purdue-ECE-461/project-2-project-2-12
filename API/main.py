from flask import Flask, request
from flask_cors import CORS, cross_origin
from db import *
import base64


# initialising the flask app
app = Flask(__name__)
cors = CORS(app)
app.config["DEBUG"] = True


# @app.route('/')
# def main():
#     # When deployed to App Engine, the `GAE_ENV` environment variable will be
#     # set to `standard`

# with cnx.cursor() as cursor:
#     cursor.execute('select * from packages;')
#     result = cursor.fetchall()
#     current_msg = result[0][0]
# cnx.close()

#     return str(current_msg)
# # [END gae_python37_cloudsql_mysql]


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


@app.route('/package/<string:id>', methods=['GET', 'POST'])
def getPackageById(id):
    if request.method == 'GET':
        query_response = run_select_query(
            f'select * from packages where id="{id}"')

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
    elif request.method == 'POST':
        json_data = request.json
        print(json_data['data']['Content'])
        print(
            f"UPDATE packages SET content=\'{json_data['data']['Content']}\' WHERE id=\'{id}\'")
        query_response = run_update_query(
            f"UPDATE packages SET content=\'{json_data['data']['Content']}\' WHERE id=\'{id}\'")

        return {}, 200

    @app.route('/package', methods=['POST'])
    def packageCreate():
        if request.is_json:
            package = request.get_json()
            content = package['data']['content']
            decoded_bytes = base64.b64decode(content)

            import os
            if not os.path.exists(package['metadata']['name']+'.zip'):
                with open(package['metadata']['name']+'.zip', 'w').close():
                    pass
            f = open(package['metadata']['name']+'.zip', 'wb')
            f.write(decoded_bytes)
            f.close()

            # upload zip file to database

            return package["metadata"], 201
        # return {"error": "Malformed request"}, 400


if __name__ == "__main__":

    # 127.0.0.1
    app.run(host='127.0.0.1', port=8080, debug=True)
