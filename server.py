import os
from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for

import data_manager

app = Flask(__name__)
pictures_questions = ".\\static\\uploads_pictures_questions"
app.config["UPLOAD_PICTURE_FOLDER"] = pictures_questions
pictures_answers = '.\\static\\uploads_pictures_answers'
app.config["UPLOAD_PICTURE_ANSWERS"] = pictures_answers
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPG", "PNG"]


@app.route("/vote/<id>/<value>")
def list_voting(id, value):
    if value == "+":
        data_manager.add_vote_counter(id)
    elif value == "-":
        data_manager.substract_vote_counter(id)
    return redirect("/list")


@app.route("/question/vote/<question_id>/<answer_id>/<vote_number>")
def list_answer_voting(question_id, answer_id, vote_number):
    data_manager.vote_for_answers(answer_id, vote_number, question_id)
    return redirect(f"/question/{question_id}")


@app.route("/")
def main():
    questions = data_manager.get_data_to_main_list()
    return render_template("index.html", questions=questions, table_header=data_manager.TABLE_HEADERS)


@app.route("/list")
def question_list(order_direction):
    questions_list = data_manager.get_question_bd()
    return render_template("list.html", questions_list=questions_list, table_headers=data_manager.TABLE_HEADERS,
                           order_direction=order_direction)


@app.route("/<value>/<descend>")
def prepare_sorted_table_to_display(value,descend=1):
    questions_list = data_manager.sort_questions_by_column(value)
    table_headers = data_manager.TABLE_HEADERS
    return render_template("list.html", questions_list=questions_list, table_headers=table_headers)


@app.route('/question')
@app.route('/question/<int:question_id>')
def question(question_id):
    tags = data_manager.get_tags(question_id)
    question_data = data_manager.find_title_and_message(int(question_id))
    answer_data = data_manager.find_all_answer_to_question(question_id)
    comments_data = data_manager.search_comment_by_id(question_id)
    return render_template('question.html', question_data=question_data, question_id=question_id,
                           answer_data=answer_data, comments_data=comments_data, tags=tags)


@app.route('/new_answer/<question_id>')
def saving_new_answer(question_id):
    question_data = data_manager.get_question_db_by_question_id(int(question_id))
    return render_template("new_answer.html", question_data=question_data, question_id=question_id)


@app.route('/new_answer/<question_id>/new-answer', methods=["POST"])
def summary_new_answer(question_id):
    question_id = int(question_id)
    if request.method == "POST":
        message = request.form.get("message")
        image = request.files['image']
        if image.filename != "" and image.filename is not None:
            if not data_manager.allowed_image(image.filename):
                return redirect(request.url)
            image.save(os.path.join(app.config["UPLOAD_PICTURE_ANSWERS"], image.filename))
            data_manager.write_answer_to_db(question_id, message, "../static/uploads_pictures_answers/"+image.filename)
        else:
            data_manager.write_answer_to_db(question_id, message)
    return redirect(f'/question/{question_id}')


@app.route('/new_question')
def add_new_question():
    return render_template("add-question.html")


@app.route('/new_question/add_new_question', methods=["POST"])
def summary_new_question():
    if request.method == "POST":
        title = request.form.get("title")
        message = request.form.get("question")
        image = request.files['image']
        if image.filename != "" and image.filename is not None:
            if not data_manager.allowed_image(image.filename):
                return redirect(request.url)
            image.save(os.path.join(app.config["UPLOAD_PICTURE_FOLDER"], image.filename))
        else:
            data_manager.save_new_question(message, title)
    return redirect('/list')


@app.route('/edit_question/<question_id>')
def saving_edit_question(question_id):
    question_data = data_manager.get_question_db_by_question_id(question_id)
    return render_template("edit_question.html", question_data=question_data, question_id=question_id)


@app.route('/edit_question/<question_id>/edited_question', methods=["POST"])
def summary_edited_question(question_id):
    if request.method == "POST":
        title = request.form.get("title")
        message = request.form.get("question")
        # image = request.files['image']
        # if image.filename != "":
        #     if not data_manager.allowed_image(image.filename):
        #         return redirect(request.url)
        #     image.save(os.path.join(app.config["UPLOAD_PICTURE_FOLDER"], image.filename))
        # data_manager.save_edited_question(title, message, "../static/uploads_pictures_questions/"+image.filename, question_id)
        data_manager.save_edited_question(title, message, question_id)
    return redirect(f'/question/{question_id}')


@app.route("/answer/<answer_id>/delete/<question_id>", methods=["POST", "GET"])
def delete_answer(answer_id, question_id):
    data_manager.delete_answer_from_comment_by_id(answer_id)
    data_manager.delete_answer_from_db_by_id(answer_id)
    return redirect(f"/question/{question_id}")


@app.route('/question/<question_id>/delete')
def delete_question(question_id):
    data_manager.delete_answers_from_comment(question_id)
    data_manager.delete_answers_from_question_tag(question_id)
    data_manager.delete_answers_from_question(question_id)
    data_manager.delete_question(question_id)
    questions_list = data_manager.get_question_bd()
    return render_template('list.html', questions_list=questions_list, table_headers=data_manager.TABLE_HEADERS)


@app.route('/edit_answer/<answer_id>')
def edit_answer(answer_id):
    answer_data = data_manager.return_question_id_and_message(answer_id)
    return render_template('edit_answer.html', answer_data=answer_data, answer_id=answer_id)


@app.route('/edit_answer/<answer_id>/edit/<question_id>', methods=["POST"])
def after_edit_answer(answer_id, question_id):
    if request.method == "POST":
        edited_answer = request.form.get('new-answer')
        data_manager.edit_answer(answer_id, edited_answer)
    return redirect(f'/question/{question_id}')


@app.route("/add_comment_to_answer/<question_id>/<answer_id>", methods=["POST", "GET"])
def comment_answer(question_id, answer_id):
    if request.method == "POST":
        comment = request.form["comment"]
        data_manager.add_comment(comment,question_id, answer_id)
        return redirect(f"/question/{question_id}")
    return render_template("Comment_Answer.html", question_id=question_id, answer_id=answer_id)


@app.route('/search')
def get_search():
    searching_phrase = request.args.get("q")
    questions = data_manager.search_user_phrase_question(searching_phrase)
    answers = data_manager.search_user_phrase_answer(searching_phrase)
    comments = data_manager.search_user_phrase_comment(searching_phrase)
    return render_template("search.html", questions=questions, answers=answers,
                           searching_phrase=searching_phrase, comments=comments)


@app.route('/edit_comment/<question_id>/<comment_id>')
def edit_comment(question_id, comment_id):
    comment_data = data_manager.get_comment_data_by_comment_id(comment_id)
    return render_template('edit_comment.html', comment_id=comment_id,
                           comment_data=comment_data, question_id=question_id)


@app.route('/edit_comment/<question_id>/<comment_id>/<edited_count>/edit', methods=["POST"])
def after_edit_comment(question_id, comment_id, edited_count):
    if request.method == "POST":
        message = request.form.get("message")
        edited_count = int(edited_count) + 1
        data_manager.edit_comment_by_comment_id(message, edited_count, comment_id)
    return redirect(f'/question/{question_id}')


@app.route("/add_comment_to_question/<question_id>", methods=["POST", "GET"])
def comment_questions(question_id):
    if request.method == "POST":
        comment = request.form["comment"]
        data_manager.add_comment(comment, question_id)
        return redirect(f"/question/{question_id}")
    return render_template("Comment_questions.html", question_id=question_id)



@app.route('/comments/<question_id>/<comment_id>/delete')
def delete_comment(question_id, comment_id):
    data_manager.delete_comment_from_database(comment_id)
    return redirect(f'/question/{question_id}')


@app.route("/question/<question_id>/new-tag", methods=["POST"])
def save_tags_to_a_question(question_id):
    tags_id = list(request.form)
    data_manager.delete_tag_list(question_id)
    if len(tags_id) > 0:
        for tag_id in tags_id:
            data_manager.save_tag_list(question_id, tag_id)
    return redirect(url_for("question", question_id=question_id))


@app.route("/question/<question_id>/new-tag")
def get_add_new_tag(question_id):
    question_data = data_manager.get_question_db_by_question_id(question_id)
    id_list = data_manager.get_id_list()
    return render_template("new_tag.html", question_id=question_id, question_data=question_data, id_list=id_list)


@app.route('/delete_question_comment/<question_id>/<comment_id>')
def delete_questions_comment(question_id, comment_id):
    data_manager.delete_comment_from_question(comment_id)
    return redirect(f'/question/{question_id}')


if __name__ == "__main__":
    app.run(debug=True,
            port=5001)
