from flask import Flask, render_template, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
import os, shutil
import webindex as wi

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['html'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'bad_secret'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def clean_folder(path):
    for the_file in os.listdir(path):
        file_path = os.path.join(path, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            #elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            print(e)

@app.route('/', methods=['GET', 'POST'])
def index():
    webindex = wi.Webindex()
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        files = request.files.getlist("file")
        print('Files are: ', request.files)
        # if user does not select file, browser also
        # submit a empty part without filename
        if not files:
            flash('No selected files')
            return redirect(request.url)
        clean_folder(app.config['UPLOAD_FOLDER'])
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                webindex.handlefile(filepath)
            else:
                flash('Found unallowed file extension: ' + file.filename)
        best = webindex.mostranked()
        webindex.saveii()
        webindex.saverepo()
    return render_template('index.html', best=best)
