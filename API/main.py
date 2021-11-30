import os
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from flask_cors import CORS, cross_origin

# initialising the flask app
app = Flask(__name__)
cors = CORS(app)
app.config["DEBUG"] = True

# Creating the upload folder
upload_folder = "uploads/"
if not os.path.exists(upload_folder):
    os.mkdir(upload_folder)

app.config['UPLOAD_FOLDER'] = upload_folder
packages = [
    {
        'name': 'Lodash',
        'version': '1.1.0',
        'url': 'https://github.com/lodash/lodash',
        'id': 'lodash',
        'data': 'null'
    },
    {
        'name': 'Lodash1',
        'version': '1.1.1',
        'url': 'https://github.com/lodash/lodash1',
        'id': 'lodash1',
        'data': 'null1'
    },
    {
        'name': 'Lodash2',
        'version': '1.1.2',
        'url': 'https://github.com/lodash/lodash2',
        'id': 'lodash2',
        'data': 'null2'
    },
    {
        'name': 'Lodash3',
        'version': '1.1.3',
        'url': 'https://github.com/lodash/lodash3',
        'id': 'lodash3',
        'data': 'null3'
    },
]


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


@app.route('/package/<int:id>', methods=['GET'])
def getPackage(id):
    pass


@app.route('/')  # The path for uploading the file
def upload_file():
    return render_template('upload.html')


@app.route('/upload', methods=['GET', 'POST'])
def uploadfile():
    if request.method == 'POST':  # check if the method is post
        f = request.files['file']  # get the file from the files object
        # Saving the file in the required destination
        # this will secure the file
        f.save(os.path.join(
            app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
        return 'file uploaded successfully'  # Display thsi message after uploading


if __name__ == "__main__":
    app.run()
