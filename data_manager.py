from operator import itemgetter
import connection

QUESTION_HEADERS = ["id", "submission_time", "view_number", "vote_number", "title", "message", "image"]
ANSWER_HEADERS = ["id", "submission_time", "vote_number", "question_id", "message", "image"]
TABLE_HEADERS = {"vote_number": "Votes", "title": "Title", "message": "Message", "view_number": "Views"}
SORT_BY_INT = ["vote_number", "view_number"]
reverse = 0  #global variable


def prepare_table_to_display(descend=0, sort_value="submission_time"):
    data = connection.import_data("./sample_data/question.csv")
    return dictionaries_sort(data, descend, sort_value), TABLE_HEADERS


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
