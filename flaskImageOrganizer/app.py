# Imports
from flask import Flask, render_template, flash, Response, request, redirect, url_for
from werkzeug.utils import secure_filename
from PIL import Image, ImageChops, ImageStat
import os
from operator import itemgetter
import numpy as np
import secrets
from shutil import copyfile
import glob

UPLOAD_FOLDER_TARGET = 'static/target/'
UPLOAD_FOLDER_IMAGES = 'static/images/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER_TARGET'] = UPLOAD_FOLDER_TARGET
secret = secrets.token_urlsafe(32)
app.secret_key = secret

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def compare_images(target, img):
    # Generate diff image in memory.
    diff_img = ImageChops.difference(target, img)
    # Calculate difference as a ratio.
    stat = ImageStat.Stat(diff_img)
    diff_ratio = sum(stat.mean) / (len(stat.mean) * 255)
    return diff_ratio * 100

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/target/', methods=['GET', 'POST'])
def upload_target():
    targetUpload = ''
    if request.method == 'POST':
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return render_template('index.html')
        if file and allowed_file(file.filename):
            cleanFolderTarget= glob.glob(UPLOAD_FOLDER_TARGET+'*')
            for item in cleanFolderTarget:
                os.remove(item)
            targetUpload = ' Upload successfully'
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER_TARGET'], filename))
        else:
            targetUpload = 'Upload fail'
    return render_template('index.html', targetUpload=targetUpload)

@app.route('/images/', methods=['GET', 'POST'])
def upload_images():
    imagesUpload = ''
    if request.method == 'POST':
        images = request.form.get("directory")
        imagesDirectory = os.listdir(images)        
        cleanFolderImages = glob.glob(UPLOAD_FOLDER_IMAGES+'*')
        for file in cleanFolderImages:
            os.remove(file)
        for file in imagesDirectory:
            if file and allowed_file(file):
                copyfile(images+'/'+file, UPLOAD_FOLDER_IMAGES+file)
        imagesUpload = ' Upload successfully'
    else:
        imagesUpload = 'Upload fail'
    return render_template('index.html', imagesUpload=imagesUpload)

@app.route("/organize/", methods=['POST'])
def organize():
    target = ""
    targetFile = os.listdir('static/target/')               
    targetFileList=[]
    for file in targetFile:
        imageName = file
        target = Image.open("static/target/"+ file)
        targetFileList.append([imageName])
    targetFileArray = np.asarray(targetFileList)
    filesToOrganize = os.listdir('static/images/')               
    filesToOrganizeList=[]
    for file in filesToOrganize:
        imageName = file
        img = Image.open("static/images/"+ file)
        ratio = compare_images(target, img)
        filesToOrganizeList.append([ratio,imageName])
    filesToOrganizeList = sorted(filesToOrganizeList, key=itemgetter(0))
    filesOrganized = np.asarray(filesToOrganizeList)
    print(filesOrganized)
    return render_template('index.html', targetFileArray=targetFileArray[0], filesOrganized=filesOrganized[:,1])

if __name__ == "__main__":
    app.run(debug=True)