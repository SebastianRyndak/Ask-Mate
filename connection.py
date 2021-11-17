import csv


def create_list(file, mode="r", buffering=3, encoding="UTF-8"):
    with open(file, mode, buffering, encoding) as f:
        csv_file = csv.DictReader(f)
        csv_list = [dict(row) for row in csv_file]
    return csv_list
