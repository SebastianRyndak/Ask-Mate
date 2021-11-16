from operator import itemgetter
import connection
import datetime

QUESTION_HEADERS = ["id", "submission_time", "view_number", "vote_number", "title", "message", "image"]
ANSWER_HEADERS = ["id", "submission_time", "vote_number", "question_id", "message", "image"]
TABLE_HEADERS = {"vote_number": "Votes", "title": "Title", "message": "Message", "submission_time": "Date", "view_number": "Views"}
SORT_BY_INT = ["vote_number", "Published on", "view_number"]
reverse = 0  #global variable


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

