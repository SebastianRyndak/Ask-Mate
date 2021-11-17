from flask import Flask, render_template, request, flash
import data_manager
import os

app = Flask(__name__)

pictures_answers = '.\\static\\upload_pictures_answers'
app.config["UPLOAD_PICTURE_FOLDER"] = pictures_answers


@app.route("/", methods=["POST", "GET"])
def hello():
    return "Hello World!"


@app.route("/question/<question_id>/new-answer", methods=["POST", "GET"])
def add_new_answer(question_id):
    return render_template("new_answer.html", question_id=question_id)


@app.route("/question/<question_id>/", methods=["POST", "GET"])
def list_new_answer(question_id):
    if request.method == "POST":
      #  if request.form.get("add_na"):
        message = request.form.get("message")
       # data_manager.add_new_answer(int(question_id), message, "")
        if request.files:
            image = request.files["image"]
            image.save(os.path.join(app.config["UPLOAD_PICTURE_FOLDER"], image.filename))
            data_manager.add_new_answer(int(question_id), message, image.filename)
    return render_template("questions_list.html", question_id=question_id)


@app.route("/answer/<answer_id>/delete", methods=["POST", "GET"])
def delete_answer(answer_id):
    if request.method == "POST":
        pass
    return render_template("questions_list.html", answer_id=answer_id)


if __name__ == "__main__":
    app.run(debug=True)
