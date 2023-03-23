from flask import Flask, request,render_template 
import os
from ultralytics import YOLO
import cv2
import csv
from flask_sqlalchemy import SQLAlchemy
import oss2
import time


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = '''mysql://mlproject:Mlproject%40#1234@rm-l4v31h2zpcuizey20.mysql.me-central-1.rds.aliyuncs.com:3306/file_database'''

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
    cls_name = ["GARBAGE", "CLUTTER SIDEWALK", "CONSTRUCTION ROAD", "GRAFFITI", "POTHOLES", "UNKEPT FACADE", "SAND ON ROAD", "BROKEN SIGNAGE", "FADED SIGNAGE", "BAD BILLBOARD", "BAD STREETLIGHT"]





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
        img_path =os.getcwd()+"/"+file_name_to_be_saved 
        tmp = img_path
        img = cv2.imread(img_path)
        results = model.predict(source=tmp, conf=0.25)
        for i in range(len(results[0].boxes.xyxy)):
        
                    #print(results[0].boxes)                        
                    cv2.rectangle(img, 
                                  (int(float(results[0].boxes.xyxy[i][0])), 
                                   int(float(results[0].boxes.xyxy[i][1]))), 
                                  (int(float(results[0].boxes.xyxy[i][2])), 
                                   int(float(results[0].boxes.xyxy[i][3]))), 
                                  (255,0,0), 2)
                    cv2.putText(img,
                                cls_name[int(results[0].boxes.cls[i])], 
                                (int(float(results[0].boxes.xyxy[i][0])), 
                                 int(float(results[0].boxes.xyxy[i][1]))), 
                                cv2.FONT_HERSHEY_SIMPLEX, .5, (0,255,0))
        
        if file.filename.split('.')[1]!='mp4':
               cv2.imwrite(os.getcwd()+"/"+"final"+file_name_to_be_saved,img)
               result_path = os.getcwd()+"/"+"final"+file_name_to_be_saved
               #result_path = "/"+"final"+file_name_to_be_saved
               with open(result_path,'rb') as result_fileobj:
                   bucket.put_object("final"+file_name_to_be_saved,result_fileobj )
                   file_img =  "https://mlproject.oss-me-central-1.aliyuncs.com/"+"final"+file_name_to_be_saved

        final_return  = """
        """
        return  render_template('result.html', results=results,result_path = file_img)

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
    app.run(port=5000,host='0.0.0.0')
    #http_server = WSGIServer(("127.0.0.1", 5000), app, handler_class=WSGIRequestHandler)
    #http_server.serve_forever()
    #server = make_server("127.0.0.1", 5000, app)
    #server.serve_forever()


