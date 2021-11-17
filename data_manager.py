import connection
import time


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
