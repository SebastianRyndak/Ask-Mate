import connection
from operator import itemgetter
import datetime


QUESTION_HEADERS = ["id", "submission_time", "view_number", "vote_number", "title", "message", "image"]
ANSWER_HEADERS = ["id", "submission_time", "vote_number", "question_id", "message", "image"]
TABLE_HEADERS = {"vote_number": "Votes", "title": "Title", "message": "Message", "submission_time": "Date", "view_number": "Views"}
SORT_BY_INT = ["vote_number", "Published on", "view_number"]
ANSWER_LIST = connection.import_data(file="sample_data/answer.csv")
QUESTION_LIST = connection.import_data(file="sample_data/question.csv")
reverse = 0  #global variable


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
                else:
                    pass
        else:
            pass
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


