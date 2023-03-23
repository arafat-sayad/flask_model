from flask import Flask, request,render_template 
import os
from ultralytics import YOLO
import cv2
import csv
from flask_sqlalchemy import SQLAlchemy
import oss2
import time

css_file = "static\style.css"


app = Flask(__name__, static_folder='.\\static')


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = '''mysql://mlproject:Mlproject%40#1234@rm-l4v31h2zpcuizey20.mysql.me-central-1.rds.aliyuncs.com:3306/file_database'''
db = SQLAlchemy(app)
class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500), nullable=False)
    path = db.Column(db.String(500), nullable=False)
    result = db.Column(db.Text)
with app.app_context():
    db.create_all()
    auth = oss2.Auth('LTAI5t8K32odhTLv7g2PZBfs', '2YZRyHMd1tDQaKXYWmsPGUWSIUZNKp')
    bucket = oss2.Bucket(auth, 'oss-me-central-1.aliyuncs.com', 'mlproject')
    model = YOLO(os.getcwd()+"/"+'best_21_01 (1).pt')
    cls_name = ["GARBAGE", "CLUTTER SIDEWALK", "CONSTRUCTION ROAD", "GRAFFITI", "POTHOLES", "UNKEPT FACADE", "SAND ON ROAD", "BROKEN SIGNAGE", "FADED SIGNAGE", "BAD BILLBOARD", "BAD STREETLIGHT"]


@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        file = request.files["file"]
        print(file.filename.split('.')[1])
        result_path=''
        results= ''
        file_name_to_be_saved = str(time.time_ns())+file.filename
        file.save(os.getcwd()+"/"+file_name_to_be_saved)

        with open(os.getcwd()+"/"+file_name_to_be_saved,'rb') as fileobj:
                bucket.put_object(file_name_to_be_saved,fileobj )
        img_path =os.getcwd()+"/"+file_name_to_be_saved 
        tmp = img_path
        img = cv2.imread(img_path)
        if file.filename.split('.')[-1]!='mp4':
               print("IN IMAGE FLOW")
               print(file_name_to_be_saved)
               results = model.predict(source=tmp, conf=0.25) 
               sfile = File(name=file_name_to_be_saved, path=os.getcwd()+"/"+file_name_to_be_saved ,result=str(results))
               db.session.add(sfile)
               db.session.commit()
        
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

               cv2.imwrite(os.getcwd()+"/"+"final"+file_name_to_be_saved,img)
               result_path = os.getcwd()+"/"+"final"+file_name_to_be_saved
               #result_path = "/"+"final"+file_name_to_be_saved
               with open(result_path,'rb') as result_fileobj:
                   bucket.put_object("final"+file_name_to_be_saved,result_fileobj )
                   file_img =  "https://mlproject.oss-me-central-1.aliyuncs.com/"+"final"+file_name_to_be_saved
               return  render_template('result.html', results=results,result_path = file_img)

        if file.filename.split('.')[-1]=='mp4':
               print("IN VIDEO FLOW")
               print(file_name_to_be_saved)
               results = os.system("yolo task=detect mode=predict model=best_21_01.pt conf=0.25 source="+file_name_to_be_saved)
               sfile = File(name=file_name_to_be_saved, path=os.getcwd()+"/"+file_name_to_be_saved ,result=str(results))
               db.session.add(sfile)
               db.session.commit()
               all_subdirs = [d for d in os.listdir(os.getcwd()+"/runs/detect") ]
               latest_subdir = max( [os.getcwd()+"/runs/detect/" +s for s in all_subdirs] , key=os.path.getmtime)
               print(latest_subdir)
               with open(latest_subdir+"/"+file_name_to_be_saved,'rb') as result_fileobj:
                           bucket.put_object("final"+file_name_to_be_saved,result_fileobj ) 
               #bucket.put_object("final"+file_name_to_be_saved,latest_subdir+"/"+file_name_to_be_saved )              
               file_img =  "https://mlproject.oss-me-central-1.aliyuncs.com/"+"final"+file_name_to_be_saved
               
               print(file_img)
               return  render_template('result_video.html', results=results, url = file_img, url_link = file_img)


        

    return render_template('index.html', css_link = css_file)

if __name__ == "__main__":
    app.run(port=5000,host='0.0.0.0')



