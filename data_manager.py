import connection
import time
import os
from operator import itemgetter
import datetime
import csv


ANSWER_DATA_PATH = os.getenv("ANSWER_DATA_PATH") if "ANSWER_DATA_PATH" in os.environ else "sample_data/answer.csv"
QUESTION_HEADERS = ["id", "submission_time", "view_number", "vote_number", "title", "message", "image"]
ANSWER_HEADERS = ["id", "submission_time", "vote_number", "question_id", "message", "image"]
TABLE_HEADERS = {"vote_number": "Votes", "title": "Title", "message": "Message", "submission_time": "Date",
                 "view_number": "Views"}
SORT_BY_INT = ["vote_number", "Published on", "view_number"]
#ANSWER_LIST = connection.import_data(file="./sample_data/answer.csv")
#QUESTION_LIST = connection.import_data(file="./sample_data/question.csv")
file_extention = ["JPG", "PNG"]
reverse = 0  # global variable


def save_new_answer(message, image, question_id):
    if image.filename != "":
        image.save(os.path.join('.\\static\\uploads_pictures_answers', image.filename))
        add_new_answer(int(question_id), message, "../static/uploads_pictures_answers/" + image.filename)
    else:
        add_new_answer(int(question_id), message, image="")


def add_new_answer(question_id, message, image):
    answer_id = ID_gen("./sample_data/answer.csv")
    submission_time = int(time.time())
    write_answer_to_csv(answer_id, submission_time, 0, question_id, message, image)


def find_title_and_message(question_id):
    data = connection.import_data(file="./sample_data/question.csv")
    for i in data:
        if i["id"] == str(question_id):
            title = i["title"]
            message = i["message"]
            image = i["image"]
            return title, message, image


def find_all_answer_to_question(question_id):
    answer = []
    vote = []
    id_list = []
    image = []
    x = connection.import_data(file="./sample_data/question.csv")
    for i in x:
        if i["id"] == str(question_id):
            y = connection.import_data(file="./sample_data/answer.csv")
            for j in y:
                if j["question_id"] == str(question_id):
                    answer.append(j.get("message"))
                    vote.append(j.get("vote_number"))
                    id_list.append(j.get("id"))
                    image.append(j.get("image"))
                else:
                    pass
        else:
            pass
    answer_len = len(answer)
    pack = list(zip(answer, vote, id_list, image))
    return pack, answer_len


def prepare_table_to_display(descend=0, sort_value="submission_time"):
    data = connection.import_data("./sample_data/question.csv")
    data = dictionaries_sort(data, descend, sort_value)
    change_date_format(data)
    return data, TABLE_HEADERS


def switch_value_type(data, type):
    for dic in data:
        for key, value in dic.items():
            if key in SORT_BY_INT:
                dic[key] = type(value)
    return data


def dictionaries_sort(data, descend, sort_value):
    global reverse
    reverse = (reverse + int(descend)) % 2
    if sort_value in SORT_BY_INT:
        data = switch_value_type(data, int)
        sorted_data = sorted(data, key=itemgetter(sort_value), reverse=reverse)
        return switch_value_type(sorted_data, str)
    return sorted(data, key=itemgetter(sort_value), reverse=reverse)


def change_date_format(data):
    for record in data:
        for key, value in record.items():
            if key == "submission_time":
                date_time = datetime.datetime.fromtimestamp(int(value))
                record[key] = date_time.strftime('%Y-%m-%d %H:%M:%S')


def ID_gen(path="./sample_data/question.csv"):
    date = connection.import_data(path)
    id_list = []
    for dic in date:
        id_list.append(int(dic["id"]))
    return max(id_list) + 1


def get_answer_by_id(answer_id):
    answer_dict = {}
    with open(ANSWER_DATA_PATH, 'r') as file:
        reader = file.DictReader(file)
        for row in reader:
            if row['id'] == answer_id:
                answer_dict = row
    return answer_dict


#Witold
def get_question_id_by_answer_id(answer_id):
    question_id = 0
    for item in connection.import_data(file="./sample_data/answer.csv"):
        if item["id"] == answer_id:
            question_id = item["question_id"]
    return question_id


def get_max_answer_id():
    id_list = []
    with open(ANSWER_DATA_PATH, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            id_list.append(row['id'])
    return max(id_list)


def write_answer_to_csv(id, submission_time, vote_number, question_id, message, image):
    with open(ANSWER_DATA_PATH, 'a', newline='', encoding="UTF-8") as file:
        writer = csv.DictWriter(file, fieldnames=ANSWER_HEADERS)
        writer.writerow(
            {ANSWER_HEADERS[0]: id,
             ANSWER_HEADERS[1]: submission_time,
             ANSWER_HEADERS[2]: vote_number,
             ANSWER_HEADERS[3]: question_id,
             ANSWER_HEADERS[4]: message,
             ANSWER_HEADERS[5]: image})


def delete_answer_from_csv_by_id(answer_id):
    answer_list_after_deletion = []
    with open(ANSWER_DATA_PATH, "r") as read_file:
        reader = csv.DictReader(read_file)
        for row in reader:
            if row['id'] != answer_id:
                answer_list_after_deletion.append(row)
    with open(ANSWER_DATA_PATH, 'w', encoding="UTF-8", newline='') as write_file:
        writer = csv.DictWriter(write_file, fieldnames=ANSWER_HEADERS)
        writer.writeheader()
        writer.writerows(answer_list_after_deletion)


def delete_question(question_id):
    que_list = connection.import_data(file="./sample_data/question.csv")
    ans_list = connection.import_data(file="./sample_data/answer.csv")
    for i in que_list:
        if i["id"] == str(question_id):
            que_list.remove(i)
    connection.overwrite_csv("sample_data/question.csv", que_list)
    for i in ans_list:
        if i["question_id"] == str(question_id):
            ans_list.remove(i)
    connection.overwrite_csv("sample_data/answer.csv", ans_list)


def vote_counter(id, value, path="./sample_data/question.csv", key_name="id"):
    data = connection.import_data(path)
    for dic in data:
        if dic[key_name] == id:
            if value == "+":
                votes = int(dic["vote_number"]) + 1
                dic["vote_number"] = str(votes)
            elif int(dic["vote_number"]) > 0:
                votes = int(dic["vote_number"]) - 1
                dic["vote_number"] = str(votes)
    return data

def vote_for_answers(answer_id, value, question_id):
    ans_list = connection.import_data(file="./sample_data/answer.csv")
    for i in ans_list:
        if i["id"] == str(answer_id) and i["question_id"] == str(question_id):
            if value == "👍":
                votes = int(i["vote_number"]) + 1
                i["vote_number"] = votes
            elif value == "👎":
                if int(i["vote_number"]) > 0:
                    votes = int(i["vote_number"]) - 1
                    i["vote_number"] = votes
                else:
                    i["vote_number"] = 0
    return ans_list

def allowed_image(filename):
    if not "." in filename:
        return False
    ext = filename.rsplit(".", 1)[1]
    if ext.upper() in file_extention:
        return True
    else:
        return False