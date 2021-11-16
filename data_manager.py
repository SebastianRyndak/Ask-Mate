from operator import itemgetter
import connection

QUESTION_HEADERS = ["id", "submission_time", "view_number", "vote_number", "title", "message", "image"]
ANSWER_HEADERS = ["id", "submission_time", "vote_number", "question_id", "message", "image"]
TABLE_HEADERS = {"vote_number": "Votes", "title": "Title", "message": "Message", "view_number": "Views"}


def dictionaries_sort(data, sort_value="submission_time", reverse=True):
    return sorted(data, key=itemgetter(sort_value), reverse=reverse)


def prepare_table_to_display():
    data = connection.import_data("./sample_data/question.csv")
    return dictionaries_sort(data), TABLE_HEADERS
