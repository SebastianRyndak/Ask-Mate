import csv
QUESTION_HEADERS = ["id", "submission_time", "view_number", "vote_number", "title", "message", "image"]
ANSWER_HEADERS = ["id", "submission_time", "vote_number", "question_id", "message", "image"]

def import_data(file, mode="r", buffering=3, encoding="UTF-8"):
    with open(file, mode, buffering, encoding) as f:
        csv_file = csv.DictReader(f)
        csv_list = [dict(row) for row in csv_file]
    return csv_list
  

def export_data(name_file, mode="a", data={}):
    with open(name_file, mode, encoding="UTF-8") as f:
        dic_list=list(data[0].keys())
        writer = csv.DictWriter(f, fieldnames=dic_list)
        writer.writeheader()
        writer.writerows(data)

""" if mode == "w":
    record = ",".join(data[0].keys())
    f.write(f"{record}\n")
for dic in data:
    question = list(dic.values())
    record = ",".join(question)
    f.write(f"{record}\n")
    
 writer = csv.DictWriter(write_file, fieldnames=ANSWER_DATA_HEADERS)
        writer.writerows(answer_list_after_deletion)"""

