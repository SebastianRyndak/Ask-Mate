from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/question/<question_id>/new-answer", methods=["POST", "GET"])
def add_new_answer(question_id):
    return render_template("new_answer.html")


if __name__ == "__main__":
    app.run()
