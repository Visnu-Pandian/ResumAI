from flask import Flask, render_template, request, redirect, url_for, jsonify, send_from_directory
import os, shutil, json, webbrowser
from datetime import datetime
from google import gensai
from dotenv import load_dotenv

# Flask app configuration
app = Flask(__name__)

# Constants

app.config['DOWNLOAD_FOLDER'] = 'downloads'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'.pdf', '.doc', '.docx'}
app.config['JSON_FOLDER'] = 'json'

# URL of project
# URL = "http://resum.ai/"
URL = "http://127.0.0.1:5000/"

# Configure allowed filetypes
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Clear the contents of a folder
def clear_folder(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')

# Clear the contents of the upload, download and json folders
def clear_upload_folder():
    clear_folder(app.config['UPLOAD_FOLDER'])
    clear_folder(app.config['JSON_FOLDER'])
    clear_folder(app.config['DOWNLOAD_FOLDER'])

# Ensure that the upload, download and json folders exist, create them if needed
def ensure_folders_exist():
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    if not os.path.exists(app.config['JSON_FOLDER']):
        os.makedirs(app.config['JSON_FOLDER'])
    if not os.path.exists(app.config['DOWNLOAD_FOLDER']):
        os.makedirs(app.config['DOWNLOAD_FOLDER'])

# Add custom helpers here

# Render frontend html page
@app.route('/')
def index():
        return render_template('index.html')

# Validate and upload resume
@app.route('/')
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url) # return to prev page
    file = request.files['files']
    if file.filename == '':
        return redirect(request.url) # return to prev page
    
    # Validate resume format
    if file and allowed_file(file.filename):
        
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return filename # move to next page

    return redirect(request.url) # return to prev page

