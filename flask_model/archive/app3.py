from flask import Flask, request
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        file = request.files["file"]
        file.save(os.getcwd()+"/"+file.filename)
        # Do something with the file
        # ...
        return "File uploaded successfully"+str(os.getcwd())
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

