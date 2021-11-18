import csv


def import_data(file, mode="r", buffering=3, encoding="UTF-8"):
    with open(file, mode, buffering, encoding) as f:
        csv_file = csv.DictReader(f)
        csv_list = [dict(row) for row in csv_file]
    return csv_list
  

def export_data(name_file, mode="a", date={}):
    with open(name_file, mode) as f:
        question = list(date.values())
        record = ",".join(question)
        f.write(f"{record}\n")

def overwrite_csv(QUESTION_LIST):
    with open("sample_data/question.csv", "w", buffering=3, encoding="UTF-8") as f:
        keys = QUESTION_LIST[0].keys()
        writer = csv.DictWriter(f, keys)
        writer.writeheader()
        writer.writerows(QUESTION_LIST)
    
