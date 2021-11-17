import csv


def import_data(name_file, mode="r", buffering=3, encoding="UTF-8"):
    with open(name_file, mode, buffering, encoding) as f:
        all_data = csv.DictReader(f)
        dictionary_lists = []
        for dictionary in all_data:
            dictionary_lists.append(dictionary)
        return dictionary_lists


def export_data(name_file, mode="a", date={}):
    with open(name_file, mode) as f:
        question = list(date.values())
        print(question)
        record = ",".join(question)
        print(record)
        f.write(f"{record}\n")