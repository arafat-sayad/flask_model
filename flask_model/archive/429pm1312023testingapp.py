from flask import Flask, request
import os
from ultralytics import YOLO
import cv2
import csv
from flask_sqlalchemy import SQLAlchemy
import oss2
import time

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = '''mysql://mlproject:Mlproject%40#1234@rm-l4v31h2zpcuizey20.mysql.me-central-1.rds.aliyuncs.com:3306/file_database'''

#model = YOLO(os.getcwd()+"/"+'best_21_01 (1).pt')

db = SQLAlchemy(app)


class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    path = db.Column(db.String(120), nullable=False)

#db.create_all()

with app.app_context():
    db.create_all()
    auth = oss2.Auth('LTAI5t8K32odhTLv7g2PZBfs', '2YZRyHMd1tDQaKXYWmsPGUWSIUZNKp')
    bucket = oss2.Bucket(auth, 'oss-me-central-1.aliyuncs.com', 'mlproject')
    model = YOLO(os.getcwd()+"/"+'best_21_01 (1).pt')




'''
db = mysql.connector.connect(
  host="rm-l4v31h2zpcuizey20.mysql.me-central-1.rds.aliyuncs.com",
  port=3306,
  user="mlproject",
  password="Mlproject@#1234",
  database="file_database"
)
'''
#print(db.is_connected())

# Get cursor to execute SQL commands
#cursor = db.cursor()


@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        file = request.files["file"]
        file_name_to_be_saved = str(time.time_ns())+file.filename
        file.save(os.getcwd()+"/"+file_name_to_be_saved)
        sfile = File(name=file_name_to_be_saved, path=os.getcwd()+"/"+file_name_to_be_saved )
        with open(os.getcwd()+"/"+file_name_to_be_saved,'rb') as fileobj:
                bucket.put_object(file_name_to_be_saved,fileobj )
        db.session.add(sfile)
        db.session.commit()

        # Do something with the file
        # ...
        return """File uploaded successfully"""
    return """
           <div style = "width : 100%; padding-top : 5%;">
            <div class = "header-content">
                 <h1 style = "text-align: center;color: black"><span class="header-content-text">Image Classification Model</span></h1>
            </div>
        </div>
            <div class = "header-content-sub">
            <p style = "text-align: center;color: black" class="header-content-info">Upload Images or Videos Here</p>
    </div>
    <form method="POST" enctype="multipart/form-data">
      <input type="file" name="file">
      <input type="submit">
    </form>
    """

if __name__ == "__main__":
    app.run(port=5000)
    


