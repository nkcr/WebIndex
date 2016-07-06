from flask import Flask, render_template, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
import os, shutil
import webindex as wi

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = set(['html'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY']    = 'dyf45hmlg350xykfh590ahfgsnek692d'
app.config['DEFAULT_QUANTITY'] = 100

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
    quantity = request.args.get("quantity")
    if(quantity is None):
        quantity = app.config['DEFAULT_QUANTITY']
    else:
        quantity = int(quantity)
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
    return render_template('index.html', best=best)
