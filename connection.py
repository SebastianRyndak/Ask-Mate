
import csv

QUESTION_HEADERS = ["id", "submission_time", "view_number", "vote_number", "title", "message", "image"]
ANSWER_HEADERS = ["id", "submission_time", "vote_number", "question_id", "message", "image"]


def import_data(file, mode="r", buffering=3, encoding="UTF-8"):
    with open(file, mode, buffering, encoding) as f:
        csv_file = csv.DictReader(f)
        csv_list = [dict(row) for row in csv_file]
    return csv_list


def export_data(name_file, data, headers, mode="a"):
    if mode == "a":
        with open(name_file, mode, encoding="UTF-8") as f:
            question = list(data.values())
            record = ",".join(question)
            f.write(f"{record}\n")
    if mode == "w":
        with open(name_file, mode, encoding="UTF-8") as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(data)