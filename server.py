from flask import Flask, render_template, request, redirect, url_for
import time
import os

app = Flask(__name__)
ID = 0
pictures = ".\\static\\uploads_picture"
app.config["UPLOAD_PICTURE_FOLDER"] = pictures


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/add-question", methods=['GET', 'POST'])
def add_information_about_question():
    if request.method == "POST":
        global ID
        ID += 1
        unix_time = int(time.time())
        title = request.form["title"]
        question = request.form["question"]
        if request.files:
            image = request.files["image"]
            image.save(os.path.join(app.config["UPLOAD_PICTURE_FOLDER"], image.filename))
            dic = {"id": ID, "submission_time": unix_time, "view_number": 0, "vote_number": 0, "title": title, "message": question, "Image": "./static/uploads_picture/" + image.filename}
            return render_template("index.html")

    return render_template("add-question.html")


if __name__ == '__main__':
    app.run(debug=True)