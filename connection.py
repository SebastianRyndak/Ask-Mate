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


