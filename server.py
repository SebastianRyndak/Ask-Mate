from flask import Flask, render_template, request, flash
import data_manager

app = Flask(__name__)


@app.route("/", methods=["POST", "GET"])
def hello():
    return "Hello World!"


@app.route("/question/<question_id>/new-answer", methods=["POST", "GET"])
def add_new_answer(question_id):
    if request.method == 'POST':
        if request.form.action == 'Post':
            message = request.form.get("message")
            data_manager.add_new_answer(question_id, message, "")
    return render_template("new_answer.html")


if __name__ == "__main__":
    app.run()
