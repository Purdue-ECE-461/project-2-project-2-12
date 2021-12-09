import re
from flask import request, jsonify, make_response
from flask_cors import cross_origin
import base64
from datetime import datetime
from Scorer.main import Package
import semver
import jwt
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
import requests
from datetime import datetime, timedelta
from models import app, db
from models import UserModel, PackageModel


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        if 'X-Authorization' in request.headers:
            token = request.headers['X-Authorization']
        # return 401 if token is not passed
        if not token:
            return jsonify({'message': 'Token is missing !!'}), 401

        try:
            # decoding the payload to fetch the stored details
            data = jwt.decode(token, app.config['SECRET_KEY'])

            curr_user = UserModel.query.filter_by(name=data['name']).first()
        except:

            return jsonify({
                'message': 'Token is invalid !!'
            }), 401
        # returns the current logged in users contex to the routes
        return f(curr_user, *args, **kwargs)

    return decorated


@app.route('/package/<string:id>', methods=['GET', 'PUT', 'DELETE'])
@token_required
def getPackageById(curr_user, id):
    if request.method == 'GET':
        package = PackageModel.query.filter_by(id=id).first()

        if (package):
            return {
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
        else:
            return {}, 404
    elif request.method == 'PUT':
        json_data = request.json

        package = PackageModel.query.filter_by(id=id).first()
        package.content = json_data['data']['Content']
        db.session.commit()

        return {}, 200
    elif request.method == 'DELETE':
        PackageModel.query.filter_by(id=id).delete()
        db.session.commit()

        return {}, 200


@app.route('/package/<string:id>/rate', methods=['GET'])
@token_required
def get_package_rating(curr_user, id):
    package = PackageModel.query.filter_by(id=id).first()

    if package:
        pkg = Package(package.url)
    else:
        return make_response("No such Package", 400)

    return {
        "RampUp": pkg.rampup,
        "Correctness": pkg.correctness,
        "BusFactor": pkg.bus_factor,
        "ResponsiveMaintainer": pkg.responsiveness,
        "LicenseScore": pkg.license_score,
        "GoodPinningPractice": pkg.good_pinning_practice
    }


@app.route('/package/byName/<string:name>', methods=['GET', 'DELETE'])
@token_required
def get_package_by_name(curr_user, name):
    if request.method == 'GET':
        packages = PackageModel.query.filter_by(name=name).all()

        resp_arr = []
        for package in packages:
            package_resp = {
                "User": {
                    "name": curr_user.name,
                    "isAdmin": True if curr_user.isAdmin else False
                },
                "Date": package.actionTime,
                "PackageMetadata": {
                    "Name": package.name,
                    "Version": package.version,
                    "ID": package.id
                },
                "Action": package.action
            }

            resp_arr.append(package_resp)

        return {'result': resp_arr}, 200

    elif request.method == 'DELETE':
        PackageModel.query.filter_by(name=name).delete()
        db.session.commit()

        return {}, 200


@app.route('/package', methods=['POST'])
@token_required
def packageCreate(curr_user):
    if request.is_json:
        package = request.json
        data = package['data']
        meta_data = package['metadata']

        if 'Content' in data:
            package_insert = PackageModel(name=meta_data["Name"], version=meta_data["Version"], id=meta_data["ID"],
                                          url="", content=data["Content"], action="CREATE", actionTime=str(datetime.now()))
            db.session.add(package_insert)
            db.session.commit()

            return package["metadata"], 201
        elif 'URL' in data:
            url = data['URL']
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
                package_insert = PackageModel(name=meta_data["Name"], version=meta_data["Version"], id=meta_data["ID"],
                                              url="", content=data["Content"], action="INGEST", actionTime=str(datetime.now()))
                db.session.add(package_insert)
                db.session.commit()

                return meta_data, 201
            else:
                return {"warning": "Package is not a trustworthy module"}
        else:
            return {"Error": "Malformed request."}, 400


@app.route('/packages', methods=['POST'])
@token_required
def get_packages():
    offset = int(request.args.get('offset', 1)[0])

    packages = request.json
    out_arr = []
    for package_info in packages:
        pkg_version = package_info['Version']
        pkg_name = package_info['Name']

        packages = PackageModel.query.filter_by(name=pkg_name).all()
        print(packages)

        if offset > 1:
            packages = packages[offset*10:(offset*10)+10]

        for pkg in packages:
            if '-' in pkg_version:
                # Version range
                lower_version, higher_version = pkg_version.split('-')

                within_range = (semver.compare(pkg.version, str(lower_version)) == 1) and (
                    semver.compare(pkg.version, str(higher_version)) == -1)

                is_range = (semver.compare(pkg.version, str(lower_version)) == 0) or (
                    semver.compare(str(higher_version), pkg.version) == 0)

                if within_range or is_range:
                    out_arr.append({
                        "Name": pkg.name,
                        "Version": pkg.version,
                        "ID": pkg.id
                    })
            else:
                # Only one version
                if pkg_version == pkg.version:
                    out_arr.append({
                        "Name": pkg.name,
                        "Version": pkg.version,
                        "ID": pkg.id
                    })

    return {"result": out_arr}


@app.route('/reset', methods=['DELETE'])
@token_required
def registry_reset(curr_user):
    packages = PackageModel.query.delete()
    users = UserModel.query.delete()

    defaultAdminUser = UserModel(
        name='ece461defaultadmin', password=generate_password_hash('correcthorsebatterystaple123(!__+@**(A'), isAdmin=True)

    db.session.add(defaultAdminUser)
    db.session.commit()

    return {}, 200


@app.route('/authenticate', methods=['PUT'])
def authenticate():
    # creates dictionary of form data
    auth = request.json

    if not auth or not auth['User']['name'] or not auth['Secret']['password']:
        # returns 401 if any email or / and password is missing
        return make_response(
            'Could not verify',
            401,
            {'WWW-Authenticate': 'Basic realm ="Login required !!"'}
        )

    user = UserModel.query.filter_by(name=auth['User']['name']).first()

    if not user:
        return make_response(
            'Could not verify',
            401,
            {'WWW-Authenticate': 'Basic realm ="User does not exist !!"'}
        )

    if check_password_hash(user.password, auth['Secret']['password']):
        # generates the JWT Token
        token = jwt.encode({
            'name': user.name,
            'exp': datetime.utcnow() + timedelta(minutes=600)
        }, app.config['SECRET_KEY'])

        return make_response(jsonify({'token': token.decode('UTF-8')}), 201)
    # returns 403 if password is wrong

    return make_response(
        'Could not verify',
        403,
        {'WWW-Authenticate': 'Basic realm ="Wrong Password !!"'}
    )


@app.route('/adduser', methods=['POST'])
@token_required
def add_user(curr_user):
    if not curr_user:
        return make_response('Must be admin to create user', 401)

    if curr_user.isAdmin:
        # creates a dictionary of the form data
        data = request.json

        # gets name, email and password
        name = data['name']
        password = data['password']

        # checking for existing user
        user = UserModel.query.filter_by(name=name).first()

        if user:
            # returns 202 if user already exists
            return make_response('User already exists. Please Log in.', 202)
        else:
            # database ORM object
            user = UserModel(name=name, password=generate_password_hash(
                password), isAdmin=False)
            db.session.add(user)
            db.session.commit()

    return make_response('Successfully registered.', 201)


@app.route('/removeuser', methods=['POST'])
@token_required
def remove_user(curr_user):
    name = request.json['name']

    if name == curr_user.name:
        user = UserModel.query.filter_by(name=name).first()
        db.session.delete(user)
        db.session.commit()

        return make_response("Account deleted!", 200)
    else:
        return make_response("You can only delete your own account", 400)


@app.route('/getPackageList', methods=['GET'])
def get_package_list():
    packages = PackageModel.query.all()

    out_arr = []
    for pkg in packages:
        package_item = {
            "name": pkg.name,
            "url": pkg.url,
            "version": pkg.version
        }
        out_arr.append(package_item)

    return {"items": out_arr}, 200


if __name__ == "__main__":
    # 127.0.0.1
    app.run(host='127.0.0.1', port=8080, debug=True)
