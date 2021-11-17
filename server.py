from flask import Flask, render_template

import data_manager

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"


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


if __name__ == "__main__":
    app.run()
