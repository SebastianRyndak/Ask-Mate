from flask import Flask, render_template
import data_manager

app = Flask(__name__)

@app.route("/")
@app.route("/list")
def question_list():
    questions_list, table_headers = data_manager.prepare_table_to_display()
    return render_template("list.html", questions_list=questions_list, table_headers=table_headers)


if __name__ == "__main__":
    app.run(debug=True)
