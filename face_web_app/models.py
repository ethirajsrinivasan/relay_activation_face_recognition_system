from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects import postgresql
import datetime

db = SQLAlchemy()

class FaceEncoding(db.Model):
    __tablename__ = 'face_encodings'

    id = db.Column(db.Integer, primary_key = True)
    file_name = db.Column(db.String)
    encoding = db.Column(postgresql.ARRAY(db.Float))


    def __init__(self, file_name,encoding):
        self.file_name = file_name
        self.encoding = encoding