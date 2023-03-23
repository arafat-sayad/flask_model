from flask import Flask, request
import os
from ultralytics import YOLO
import cv2
import csv
import mysql.connector



app = Flask(__name__)
model = YOLO(os.getcwd()+"/"+'best_21_01 (1).pt')


db = mysql.connector.connect(
  host="rm-l4v31h2zpcuizey20.mysql.me-central-1.rds.aliyuncs.com",
  port=3306,
  user="mlproject",
  password="Mlproject@#1234",
  database="file_database"
)

print(db.is_connected())

# Get cursor to execute SQL commands
cursor = db.cursor()


@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        file = request.files["file"]
        file.save(os.getcwd()+"/"+file.filename)
        sql = "INSERT INTO files_results (id, path, result) VALUES (%s, %s, %s)"
        val = (cursor.lastrowid,os.getcwd()+"/"+file.filename,"model text results or path")
        cursor.execute(sql,  (cursor.lastrowid,os.getcwd()+"/"+file.filename,"model text results or path"))
        db.commit()
        db.reset_session()

        # Do something with the file
        # ...
        return """File uploaded successfully
                   <table class="table-bordered text-light table-custom">
                   <tr>
                       <th>Rank</th>
                       <th>Class</th>
                       <th>Probability</th>
                   </tr>
                   <tr>
                       <td>1st</td>
                       <td>{{ predictions.class1 }}</td>
                       <td>{{ predictions.prob1 }} %</td>
                     </tr>
                     <tr>
                       <td>2nd</td>
                       <td>{{ predictions.class2 }}</td>                                                         
                       <td>{{ predictions.prob2 }} %</td>                                                      
                   </tr>                                                                                                               
                   <tr>
                       <td>3rd</td>
                       <td>{{ predictions.class3 }}</td>
                       <td>{{ predictions.prob3 }} %</td>
                     </tr>
               </table>

		"""
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
    


