import csv
import time
import os

ANSWER_DATA_PATH = os.getenv("ANSWER_DATA_PATH") if "ANSWER_DATA_PATH" in os.environ else "sample_data/answer.csv"
ANSWER_DATA_HEADERS = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']


def get_all_answers():
    answers_list = []
    with open(ANSWER_DATA_PATH, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            answers_list.append(row)
    return answers_list


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
        writer = csv.DictWriter(file, fieldnames=ANSWER_DATA_HEADERS)
        writer.writerow(
            {ANSWER_DATA_HEADERS[0]: id,
             ANSWER_DATA_HEADERS[1]: submission_time,
             ANSWER_DATA_HEADERS[2]: vote_number,
             ANSWER_DATA_HEADERS[3]: question_id,
             ANSWER_DATA_HEADERS[4]: message,
             ANSWER_DATA_HEADERS[5]: image}
        )
