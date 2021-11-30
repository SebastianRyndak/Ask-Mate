from flask import Flask, render_template, request, redirect, url_for
import time, connection
import os
import data_manager

app = Flask(__name__)
pictures_questions = ".\\static\\uploads_pictures_questions"
app.config["UPLOAD_PICTURE_FOLDER"] = pictures_questions
pictures_answers = '.\\static\\uploads_pictures_answers'
app.config["UPLOAD_PICTURE_ANSWERS"] = pictures_answers
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPG", "PNG"]


@app.route("/vote/<id>/<value>")
def list_voting(id, value):
    data = data_manager.vote_counter(id, value)
    connection.export_data("./sample_data/question.csv", data, data_manager.QUESTION_HEADERS, "w")
    return redirect("/")


@app.route("/question/vote/<question_id>/<answer_id>/<value>")
def list_answer_voting(question_id, answer_id, value):
    ans_list = data_manager.vote_for_answers(answer_id, value, question_id)
    connection.export_data("sample_data/answer.csv", ans_list, data_manager.ANSWER_HEADERS, "w")
    return redirect(f"/question/{question_id}")

 
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
        image = request.files["image"]
        if image.filename != "":
            if not data_manager.allowed_image(image.filename):
                return redirect(request.url)
            image.save(os.path.join(app.config["UPLOAD_PICTURE_FOLDER"], image.filename))

            dic = {"id": str(ID), "submission_time": str(unix_time), "view_number": "0", "vote_number": "0", "title": title, "message": question, "Image": "../static/uploads_pictures_questions/" + str(image.filename)}
        else:
            dic = {"id": str(ID), "submission_time": str(unix_time), "view_number": "0", "vote_number": "0", "title": title, "message": question, "Image": ""}
        connection.export_data("./sample_data/question.csv", dic, data_manager.QUESTION_HEADERS, "a")
        return redirect("/")
    return render_template("add-question.html")


@app.route("/<value>/<descend>")
def prepare_sorted_table_to_display(descend, value):
    questions_list, table_headers = data_manager.prepare_table_to_display(int(descend), value)
    return render_template("list.html", questions_list=questions_list, table_headers=table_headers)


@app.route('/question')
@app.route('/question/<question_id>', methods=["POST", "GET"])
def question(question_id):
    if request.method == "POST":
        data_manager.save_new_answer(request.form.get("message"), request.files["image"], question_id)
    title, message, image = data_manager.find_title_and_message(question_id)
    pack, answer_len = data_manager.find_all_answer_to_question(question_id)
    return render_template('question.html', head_title=title, title_message=message, package=pack, lenth=answer_len, question_id=question_id, image=image)


@app.route("/question/<question_id>/new-answer", methods=["POST", "GET"])
def add_new_answer(question_id):
    question = data_manager.find_title_and_message(question_id)[0]
    return render_template("new_answer.html", question_id=question_id, question=question)


@app.route("/answer/<answer_id>/delete", methods=["POST", "GET"])
def delete_answer(answer_id):
    question_id = data_manager.get_question_id_by_answer_id_db(answer_id)
    data_manager.delete_answer_from_cvs_by_id_db(answer_id)
    return redirect(f"../../question/{question_id}")


@app.route('/question/<int:question_id>/delete', methods=["POST"])
def delete_question(question_id):
    data_manager.delete_question(question_id)
    questions_list, table_headers = data_manager.prepare_table_to_display()
    return render_template('list.html', questions_list=questions_list, table_headers=table_headers)


@app.route('/question/<int:question_id>/edit', methods=["GET", "POST"])
def edit_questions(question_id):
    if request.method == "POST":
        question_record = data_manager.find_question(question_id)
        question_record['submission_time'] = str(int(time.time()))
        question_record['title'] = request.form["title"]
        question_record['message'] = request.form["question"]
        image = request.files["image"]
        if image.filename != "":
            if not data_manager.allowed_image(image.filename):
                return redirect(request.url)
            image.save(os.path.join(app.config["UPLOAD_PICTURE_FOLDER"], image.filename))
            question_record['image'] = "../static/uploads_pictures_questions/" + str(image.filename)
        data_manager.overwrite(question_id, question_record)
        return redirect(f'/question/{question_id}')
    title, message, image = data_manager.find_title_and_message(question_id)
    return render_template('edit_questions.html', title=title, message=message, image=image)

  
if __name__ == "__main__":
    app.run(debug=True)
