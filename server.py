from flask import Flask, render_template, request, redirect, url_for
import time, connection
import os
import data_manager


app = Flask(__name__)
pictures_questions = ".\\static\\uploads_picture_questions"
app.config["UPLOAD_PICTURE_FOLDER"] = pictures_questions
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPG", "PNG"]


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
            if image.filename != "":
                if not allowed_image(image.filename):
                    return redirect(request.url)
                image.save(os.path.join(app.config["UPLOAD_PICTURE_FOLDER"], image.filename))
                dic = {"id": str(ID), "submission_time": str(unix_time), "view_number": "0", "vote_number": "0", "title": title, "message": question, "Image": "./static/uploads_picture_questions/" + str(image.filename)}
            else:
                image = ""
                dic = {"id": str(ID), "submission_time": str(unix_time), "view_number": "0", "vote_number": "0", "title": title, "message": question, "Image": str(image)}
            connection.export_data("./sample_data/question.csv", "a", dic)
            questions_list, table_headers = data_manager.prepare_table_to_display()
            return render_template("list.html", questions_list=questions_list, table_headers=table_headers)

    return render_template("add-question.html")


@app.route("/<value>/<descend>")
def prepare_sorted_table_to_display(descend, value):
    questions_list, table_headers = data_manager.prepare_table_to_display(int(descend), value)
    return render_template("list.html", questions_list=questions_list, table_headers=table_headers)


@app.route('/question')
@app.route('/question/<int:question_id>')
def question(question_id):
    try:
        title, message = data_manager.find_title_and_message(question_id)
        pack, answer_len = data_manager.find_all_answer_to_question(question_id)
    except UnboundLocalError:
        return "Page doesn't exist"
    except TypeError:
        return "Page doesn't exist"
    return render_template('question.html', head_title=title, title_message=message, package=pack, lenth=answer_len)


def allowed_image(filename):
    if not "." in filename:
        return False
    ext = filename.rsplit(".", 1)[1]
    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False


if __name__ == "__main__":
    app.run(debug=True)

