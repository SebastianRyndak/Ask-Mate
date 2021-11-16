from flask import Flask, render_template, request
import time


app = Flask(__name__)
ID = 0


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/add-question")
def add():
    return render_template("add-question.html")


@app.route("/add-question", methods=['POST'])
def add_question():
    global ID
    ID += 1
    unix_time = int(time.time())
    title = request.form["title"]
    question = request.form["question"]
    image = request.form["image"]
    dic = {"ID": ID, "Time": unix_time, "Title": title, "Question": question, "Image": image}
    print(dic)
    if image is not None:
        with open("images.txt", "w") as file:
            file.write(image)
    return render_template("add-question.html", dic=dic)


if __name__ == "__main__":
    app.run()
