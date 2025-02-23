'''This module provides a minimalist interface using Flask webserver.

Author: Noémien Kocher
Licence: MIT
Date: july 2016
'''

from flask import Flask, render_template, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
import os, shutil
import webindex as wi

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads' # default uplad folder
ALLOWED_EXTENSIONS = set(['html']) # file extension allowed
MAX_HIST = 100 # default number of keywords to display

# Set Flask variables
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY']    = 'dyf45hmlg350xykfh590ahfgsnek692d'
app.config['DEFAULT_QUANTITY'] = 100

def display_filter(s):
    '''This is a jinja filter. It returns a value for the histogram.
    '''
    res = round(s,2)
    if(res > MAX_HIST):
        return MAX_HIST
    return round(s,2)
app.jinja_env.filters['hist'] = display_filter

def cut_filter(s):
    '''This is a jinja filter. It removes extra digits on a float
    '''
    return round(s,2)
app.jinja_env.filters['cut'] = cut_filter

def allowed_file(filename):
    '''Check if a filename has the good extension (ie .html)
    '''
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def clean_folder(path):
    '''Removes the content of a folder.
    '''
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
    '''This is our main and only entry. It can display keywords based
    on data found in 'data' folder or read html files from a folder and
    creating the datastructures that will be saved in 'data' folder.
    '''
    webindex = wi.Webindex()

    # Quantity param
    quantity = request.args.get("quantity")
    if(quantity is None):
        quantity = app.config['DEFAULT_QUANTITY']
    else:
        quantity = int(quantity)

    # bias param
    if(request.args.get("word") is not None and
            request.args.get("bias") is not None):
        try:
            webindex.bias(request.args.get("word"), float(request.args.get("bias")))
        except BaseException as e:
            flash("Failed to bias. ", str(e))

    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        files = request.files.getlist("file")
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
        best = webindex.mostranked(quantity)
        webindex.saveii()
        webindex.saverepo()
    else:
        best = webindex.read_mostranked(quantity)
    words = webindex.get_words()
    return render_template('index.html', best=best, words=words)
