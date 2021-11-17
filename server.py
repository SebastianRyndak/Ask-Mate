from flask import Flask, render_template, request, flash
import data_manager

app = Flask(__name__)


@app.route("/", methods=["POST", "GET"])
def hello():
    return "Hello World!"


@app.route("/question/<question_id>/new-answer", methods=["POST", "GET"])
def add_new_answer(question_id):
    return render_template("new_answer.html", question_id=question_id)


@app.route("/question/<question_id>/", methods=["POST", "GET"])
def list_new_answer(question_id):
    if request.method == "POST":
        if request.form.get("add_na"):
            message = request.form.get("message")
            data_manager.add_new_answer(int(question_id), message, "")
        elif request.form.get("upload_na"):
            print("test")
    return render_template("new_answer.html", question_id=question_id)


if __name__ == "__main__":
    app.run(debug=True)
