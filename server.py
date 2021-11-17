from flask import Flask, render_template, request, redirect, url_for
import time, connection
import os
import data_manager


app = Flask(__name__)
pictures = ".\\static\\uploads_picture"
app.config["UPLOAD_PICTURE_FOLDER"] = pictures

pictures_answers = '.\\static\\upload_pictures_answers'
app.config["UPLOAD_PICTURE_FOLDER"] = pictures_answers


@app.route("/")
@app.route("/list")
def question_list():
    questions_list, table_headers = data_manager.prepare_table_to_display()
    return render_template("list.html", questions_list=questions_list, table_headers=table_headers)


@app.route("/add-question", methods=['GET', 'POST'])
def add_information_about_question():
    if request.method == "POST":
        ID = data_manager.ID_gen()
        unix_time = int(time.time())
        title = request.form["title"]
        question = request.form["question"]
        if request.files:
            image = request.files["image"]
            image.save(os.path.join(app.config["UPLOAD_PICTURE_FOLDER"], image.filename))
            dic = {"id": str(ID), "submission_time": str(unix_time), "view_number": "0", "vote_number": "0", "title": title, "message": question, "Image": "./static/uploads_picture/" + str(image.filename)}
            connection.export_data("./sample_data/question.csv", "a", dic)
            questions_list, table_headers = data_manager.prepare_table_to_display()
            return render_template("list.html", questions_list=questions_list, table_headers=table_headers)

    return render_template("add-question.html")


@app.route("/<value>/<descend>")
def prepare_sorted_table_to_display(descend, value):
    questions_list, table_headers = data_manager.prepare_table_to_display(int(descend), value)
    return render_template("list.html", questions_list=questions_list, table_headers=table_headers)


@app.route('/question')
@app.route('/question/<question_id>', methods=["POST", "GET"])
def question(question_id):
    if request.method == "POST":
      #  if request.form.get("add_na"):
        message = request.form.get("message")
       # data_manager.add_new_answer(int(question_id), message, "")
        if request.files:
            image = request.files["image"]
            image.save(os.path.join(app.config["UPLOAD_PICTURE_FOLDER"], image.filename))
        data_manager.add_new_answer(int(question_id), message, image.filename)
    try:
        title, message = data_manager.find_title_and_message(question_id)
        pack, answer_len = data_manager.find_all_answer_to_question(question_id)
    except UnboundLocalError:
        return "Page doesn't exist"
    except TypeError:
        return "Page doesn't exist"
    return render_template('question.html', head_title=title, title_message=message, package=pack, lenth=answer_len, question_id=question_id)


@app.route("/question/<question_id>/new-answer", methods=["POST", "GET"])
def add_new_answer(question_id):
    return render_template("new_answer.html", question_id=question_id)


@app.route("/answer/<answer_id>/delete", methods=["POST", "GET"])
def delete_answer(answer_id):
    if request.method == "POST":
        pass
    return render_template("question.html", answer_id=answer_id)


if __name__ == "__main__":
    app.run(debug=True)

