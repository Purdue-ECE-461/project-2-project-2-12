from flask import Flask, request
from flask_cors import CORS, cross_origin
from db import *
import base64
from datetime import datetime
from Scorer.main import Package
import semver
import requests

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
            f'select * from packages where id="{id}"')[0]

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
def get_package_rating(id):
    query_response = run_select_query(
        f'select url from packages where id="{id}"')

    url = query_response[0][0]
    pkg = Package(url)

    return {
        "RampUp": pkg.rampup,
        "Correctness": pkg.correctness,
        "BusFactor": pkg.bus_factor,
        "ResponsiveMaintainer": pkg.responsiveness,
        "LicenseScore": pkg.license_score,
        "GoodPinningPractice": pkg.good_pinning_practice
    }


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
            return package["metadata"], 201
        elif 'URL' in data:
            url = data['url']
            pkg = Package(url)
            score = pkg.total_score

            if score >= 0.5:
                """ Download the Github Repo as a .zip file """
                headers = {}
                branch = ''
                ext = 'zip'
                owner, repo = pkg.urlParse(pkg.url)
                url = f'https://api.github.com/repos/{owner}/{repo}/{ext}ball/{branch}'

                r = requests.get(url, headers=headers)
                if r.status_code == 200:
                    with open(f'repo.{ext}', 'wb') as f:
                        f.write(r.content)

                """ Encode the .zip file in base64 """
                with open("repo.zip", "rb") as f:
                    bytes = f.read()
                    content = base64.b64encode(bytes)

                """ Update package's content field with base64 encoding and upload to database """
                data["Content"] = content
                query_response = run_insert_query(
                    f'insert into packages(name,version,id,url,content,action,actionTime) values ("{meta_data["Name"]}", '
                    f'"{meta_data["Version"]}", "{meta_data["ID"]}", "", "{data["Content"]}", "INGEST", "{datetime.now()}"");')

                return meta_data, 201
            else:
                return {"warning": "Package is not a trustworthy module"}
        else:
            return {"Error": "Malformed request."}, 400

@app.route('/packages', methods=['POST'])
def get_packages():
    packages = request.json
    out_arr = []
    for package_info in packages:
        pkg_version = package_info['Version']
        pkg_name = package_info['Name']
        query_packages = run_select_query(
            f"SELECT name, version, id from packages WHERE name='{pkg_name}'")

        for pkg in query_packages:
            print(pkg)
            if '-' in pkg_version:
                # Version range
                lower_version, higher_version = pkg_version.split('-')

                within_range = (semver.compare(str(pkg[1]), str(lower_version)) == 1) and (
                        semver.compare(str(pkg[1]), str(higher_version)) == -1)

                is_range = (semver.compare(str(pkg[1]), str(lower_version)) == 0) or (
                        semver.compare(str(higher_version), str(pkg[1])) == 0)

                if within_range or is_range:
                    out_arr.append({
                        "Name": pkg[0],
                        "Version": pkg[1],
                        "ID": pkg[2]
                    })
            else:
                # Only one version
                if pkg_version == pkg[1]:
                    out_arr.append({
                        "Name": pkg[0],
                        "Version": pkg[1],
                        "ID": pkg[2]
                    })

    return {"result": out_arr}


@app.route('/reset', methods=['DELETE'])
def registry_reset():
    pass


@app.route('/authenticate', methods=['PUT'])
def authenticate():
    pass


if __name__ == "__main__":
    # 127.0.0.1
    app.run(host='127.0.0.1', port=8080, debug=True)
