from flask import Flask,render_template,request,flash,redirect,url_for
from werkzeug.utils import secure_filename 
import os
import cv2 

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'webp', 'png', 'jpg', 'jpeg', 'gif'}

def create_app():
    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.secret_key = 'super secret key'
    @app.route('/')
    def home():
        return render_template('index.html')

    @app.route('/about')
    def about():
        return render_template('about.html')

    @app.route('/edit', methods =["GET", "POST"])
    def edit():
        if request.method =="POST":
            # check if the post request has the file part
            operation = request.form.get('operation')
            if 'file' not in request.files:
                flash('No file part')
                return "error"
            file = request.files['file']
            # If the user does not select a file, the browser submits an
            # empty file without a filename.
            if file.filename == '':
                flash('No selected file')
                return "error no selected file"
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                new = processImage(filename,operation)
                flash(f"Your image has been processed and is available <a href='/{new}' target='_blank'> here</a>")
                return render_template('index.html')
    return app
# def processImage(filename,operation):
#     print(f"The file name is {filename} and the operation is {operation}")
#     img = cv2.imread(f"uploads/{filename}")
#     match operation:
#         case "cgray":
#             imgProccesed = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
#             newfilename = f"static/{filename}"
#             cv2.imwrite(newfilename,imgProccesed)
#             return newfilename
#         case "cpng":
#             newfilename = f"static/{filename.split('.')[0]}.png"
#             cv2.imwrite(newfilename,img)
#             return newfilename
#         case "cwebp":
#             newfilename = f"static/{filename.split('.')[0]}.webp"
#             cv2.imwrite(newfilename,img)
#             return newfilename
#         case "cjpg":
#             newfilename = f"static/{filename.split('.')[0]}.jpg"
#             cv2.imwrite(newfilename,img)
#             return newfilename
#     pass

def processImage(filename, operation):
    print(f"The file name is {filename} and the operation is {operation}")
    img = cv2.imread(f"uploads/{filename}")
    match operation:
        case "cgray":
            imgProcessed = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            newfilename = f"static/{filename}"
            cv2.imwrite(newfilename, imgProcessed)
            return newfilename
        case "cpng":
            newfilename = f"static/{filename.split('.')[0]}.png"
            cv2.imwrite(newfilename, img)
            return newfilename
        case "cwebp":
            newfilename = f"static/{filename.split('.')[0]}.webp"
            cv2.imwrite(newfilename, img)
            return newfilename
        case "cjpg":
            newfilename = f"static/{filename.split('.')[0]}.jpg"
            cv2.imwrite(newfilename, img)
            return newfilename
        case "invert":
            imgProcessed = cv2.bitwise_not(img)
            newfilename = f"static/{filename}"
            cv2.imwrite(newfilename, imgProcessed)
            return newfilename
    pass

def allowed_file(filename): 
    return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


app = create_app()
