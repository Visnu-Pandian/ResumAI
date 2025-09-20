
from flask import Flask, render_template, request, redirect, url_for, jsonify, send_from_directory
import os, shutil, json, webbrowser, requests
from datetime import datetime
from google import genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Flask app configuration
app = Flask(__name__)

# Constants

app.config['DOWNLOAD_FOLDER'] = 'downloads'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'doc', 'docx'}
app.config['JSON_FOLDER'] = 'json'
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

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

# --- Routes ---

# Render frontend html page
@app.route('/')
def index():
    """Renders the main webpage."""
    return render_template('index.html')

@app.route('/chat')
def char():
    """Renders the Gemini chat page."""
    resume_uploaded = request.args.get('resume', 'false')
    return render_template('chat.html', resume=resume_uploaded)

# Validate and upload resume
@app.route('/upload', methods=['POST'])
def upload_file():
    """Handles the file upload."""
    if 'file' not in request.files:
        return jsonify({'success': False, 'error':'No file part in the request.'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'success': False, 'error':'No file selected'}), 400
    
    # Validate resume format
    if file and allowed_file(file.filename):
        
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return jsonify({'success':True})
    else:
        return jsonify({'success': False, 'error': 'File type not allowed'}), 400

# --- Main Execution ---

if __name__ == '__main__':
    ensure_folders_exist()
    clear_upload_folder()
    
    webbrowser.open(URL)
    app.run(debug=True, host="0.0.0.0")
