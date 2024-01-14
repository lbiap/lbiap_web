from flask import Flask, request, jsonify, Response, send_file, send_from_directory
import os
import uuid
import zipfile
from flask_cors import CORS
import pandas as pd
import io
from Helpers import *
import nltk
import csv
import glob
import pandas
import random
from lbiap31 import *

def update_variable(value):
    global unzipped_dir
    unzipped_dir = value

UPLOAD_FOLDER = "/home/michael/uploaded_files"  # This sets the path to an 'uploads' directory in your current working directory
angular_src_folder = '/home/michael/Summer 2023/lbiap_web/lbiap_web/lbiap_web-1/uploads'

def countWords(tokens_ls):
	return len(tokens_ls)

def typeToken(tokens_ls):
	# get uniq tokens 
	try:
		unique_n = len( set( tokens_ls ) )
		total_n = countWords(tokens_ls)
		ttr_f = unique_n/total_n
	except:
		ttr_f = -99
	return ttr_f

def unzip_to_guid_directory(zip_filepath):
    # Generate a random UUID
    dir_name = str(uuid.uuid4())

    # Create a new directory with the UUID name
    new_dir_path = os.path.join(os.getcwd(), dir_name)
    os.makedirs(new_dir_path, exist_ok=True)
    csv_dir_path = os.path.join(os.getcwd(), dir_name, "csv")
    os.makedirs(csv_dir_path, exist_ok=True)
    # Unzip the files into the new directory
    with zipfile.ZipFile(zip_filepath, 'r') as zip_ref:
        zip_ref.extractall(new_dir_path)

    return new_dir_path  # Return the path to the created directory for reference



if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app = Flask(__name__)
CORS(app, resources={r"/upload": {"origins": "http://localhost:4200"}},
     allow_headers=["Content-Type", "Authorization", "Access-Control-Allow-Credentials"],
     supports_credentials=True)
global olddir
ALLOWED_EXTENSIONS = {'zip'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/<filename>.zip')
def download_file(filename):
    return send_from_directory(angular_src_folder, filename + '.zip', as_attachment=True)

@app.route('/upload', methods=['POST'])
def upload_file():
    # check if the post request has the file part
    if 'file' not in request.files:
        return jsonify(error="No file part"), 400

    file = request.files['file']

    # if user does not select file, browser also submits an empty part without filename
    if file.filename == '':
        return jsonify(error="No selected file"), 400

    if file and allowed_file(file.filename):
        app.config['UPLOAD_FOLDER'] = '/home/michael/uploaded_files'
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)
        unzipped_dir = unzip_to_guid_directory(filename)
        update_variable(unzipped_dir)
        global corpusfiles
        global olddir
        global df_results_cleaned
        corpusfiles = os.path.join(unzipped_dir, '*.txt')
        print(f"Files unzipped to: {unzipped_dir}")
        print(corpusfiles)
        print(corpusfiles)
        olddir = os.path.join(unzipped_dir)
        print(olddir)

        zip_buffer = lbiap_go(olddir)
        print("At what point does this happen", zip_buffer)
        zip_file_url = os.path.join(request.url_root, os.path.basename(zip_buffer))
        return jsonify({"download_url": zip_file_url})
    return jsonify(error="File type not allowed"), 400

if __name__ == '__main__':
    app.run(debug=True)
