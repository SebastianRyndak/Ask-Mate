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
ANSWER_LIST = connection.import_data(file="./sample_data/answer.csv")
QUESTION_LIST = connection.import_data(file="./sample_data/question.csv")
reverse = 0  # global variable


def add_new_answer(question_id, message, image):
    answer_id = int(connection.get_max_answer_id()) + 1
    submission_time = int(time.time())
    connection.write_answer_to_csv(answer_id, submission_time, 0, question_id, message, image)


def delete_answer_by_id(answer_id):
    answers_list = connection.get_all_answers()
    for answer in answers_list:
        if answer['id'] == answer_id:
            answers_list.remove(answer)
    return answers_list


def find_title_and_message(question_id):
    for i in QUESTION_LIST:
        if i["id"] == str(question_id):
            title = i["title"]
            message = i["message"]
            return title, message


def find_all_answer_to_question(question_id):
    answer = []
    vote = []
    for i in QUESTION_LIST:
        if i["id"] == str(question_id):
            for j in ANSWER_LIST:
                if j["question_id"] == str(question_id):
                    answer.append(j.get("message"))
                    vote.append(j.get("vote_number"))
 

    answer_len = len(answer)
    pack = list(zip(answer, vote))
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


def ID_gen():
    date = connection.import_data("./sample_data/question.csv")
    id_list = []
    for dic in date:
        id_list.append(int(dic["id"]))
    return max(id_list) + 1


def get_answer_by_id(answer_id):
    answer_dict = {}
    with open(ANSWER_DATA_PATH, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['id'] == answer_id:
                answer_dict = row
    return answer_dict


def get_max_answer_id():
    id_list = []
    with open(ANSWER_DATA_PATH, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            id_list.append(row['id'])
    return max(id_list)


def write_answer_to_csv(id, submission_time, vote_number, question_id, message, image):
    with open(ANSWER_DATA_PATH, 'a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=ANSWER_HEADERS)
        writer.writerow(
            {ANSWER_DATA_HEADERS[0]: id,
             ANSWER_DATA_HEADERS[1]: submission_time,
             ANSWER_DATA_HEADERS[2]: vote_number,
             ANSWER_DATA_HEADERS[3]: question_id,
             ANSWER_DATA_HEADERS[4]: message,
             ANSWER_DATA_HEADERS[5]: image}
        )


def delete_answer_from_csv_by_id(answer_id):
    answer_list_after_deletion = []
    with open(ANSWER_DATA_PATH, "r") as read_file:
        reader = csv.DictReader(read_file)
        for row in reader:
            if row['id'] != answer_id:
                answer_list_after_deletion.append(row)
    print(answer_list_after_deletion)
    with open(ANSWER_DATA_PATH, 'w') as write_file:
        writer = csv.DictWriter(write_file, fieldnames=ANSWER_DATA_HEADERS)
        writer.writerows(answer_list_after_deletion)


def delete_question(question_id):
    for i in QUESTION_LIST:
        if i["id"] == str(question_id):
            QUESTION_LIST.remove(i)
    connection.overwrite_csv(QUESTION_LIST)
