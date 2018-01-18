from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename
from models import db
from models import FaceEncoding
import random
import os
from datetime import datetime
import face_recognition
from PIL import Image
import face_recognition


app = Flask(__name__)

POSTGRES = {
    'user': 'postgres',
    'pw': 'postgres',
    'db': 'face_recognition',
    'host': 'localhost',
    'port': '5432',
}

dir_path = os.path.dirname(os.path.realpath(__file__))
UPLOAD_FOLDER = dir_path + '/pictures'

ALLOWED_EXTENSIONS = set(['jpg'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
db.init_app(app)

@app.route("/")
def main():
    return  "Hello world"


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/add",methods=['GET','POST'])
def add():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file and allowed_file(file.filename):
            currenttime = datetime.now().strftime('%Y%m%d%H%M%S')
            name = request.form.get("name")
            filename = name+"_"+currenttime+".jpg"
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            image = face_recognition.load_image_file(file)
            encoding = face_recognition.face_encodings(image)[0]
            face_encoding = FaceEncoding(filename,encoding)
            db.session.add(face_encoding)
            db.session.commit()
            return "success"
    else:
        return "Hello"

@app.route("/recognize",methods=['GET','POST'])
def recognize():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file and allowed_file(file.filename):
            unknown_image = face_recognition.load_image_file(file)
            unknown_face_encoding = face_recognition.face_encodings(unknown_image)[0]
            known_faces = [instance[0] for instance in db.session.query(FaceEncoding.encoding).all()]
            results = face_recognition.compare_faces(known_faces, unknown_face_encoding,tolerance=0.5)
            face_index = [index for index,val in enumerate(results) if val==True]
            print(face_index)
            if len(face_index) == 0:
                return "unknown"
            faces = [instance[0] for instance in db.session.query(FaceEncoding.file_name).all()]
            faces[face_index[0]]
            return faces[face_index[0]].split('_')[0]
    else:
        return "Hello"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port= 5000)