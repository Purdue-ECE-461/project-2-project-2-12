from flask import Flask, request
from flask_cors import CORS, cross_origin
from db import *


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


@app.route('/package/<string:id>', methods=['GET', 'PUT', 'DELETE'])
def getPackageById(id):
    if request.method == 'GET':
        query_response = run_select_query(
            f'select * from packages where id="{id}"')

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
        query_response = run_update_query(
            f"DELETE FROM packages WHERE id='{id}'")

        return {}, 200


@app.route('/package/<string:id>/rate', methods=['GET'])
def get_package_rating():
    pass


@app.route('/package/byName/<string:name>', methods=['GET'])
def get_package_by_name():
    pass

    @app.route('/package', methods=['POST'])
    def ingestPackage(id):



if __name__ == "__main__":

    # 127.0.0.1
    app.run(host='127.0.0.1', port=8080, debug=True)
