from app import app
from flask import render_template, request, redirect
import os
from werkzeug.utils import secure_filename
from app import process_res

app.config["IMAGE_UPLOADS"] = "app/static/img/uploads"
app.config["ALLOWED_IMAGE_EXTENSIONS"] = set(["JPEG", "JPG", "PNG", "GIF"])
app.config["MAX_IMAGE_FILESIZE"] = 0.5 * 1024 * 1024

@app.route("/")
def index():
    return render_template("public/base.html")

def allowed_image(filename):

    if not "." in filename:
        return False

    ext = filename.rsplit(".", 1)[1]

    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False

def allowed_image_filesize(filesize):

    if int(filesize) <= app.config["MAX_IMAGE_FILESIZE"]:
        return True
    else:
        return False

@app.route("/upload-image", methods=["GET", "POST"])
def upload_image():
    
    if request.method == "POST":
        
        if request.files:

            image = request.files["image"]

            if image.filename == "":
                print("No filename")
                return redirect(request.url)

            if allowed_image(image.filename):
                filename = secure_filename(image.filename)
                
                image.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))
                #image.save(filename)

                print("Image saved")

                return redirect(request.url)

            else:
                print("That file extension is not allowed")
                return redirect(request.url)

    return render_template("public/upload_image.html")

@app.route("/results")
def result():
    captions = process_res.get_result();
    images = os.listdir("app/static/img/uploads")
    #hists = ['uploads/' + file for file in images]
    return render_template('public/results.html', images = images, captions = captions, len = len(captions))