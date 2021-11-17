import csv


def import_data(name_file, mode="r", buffering=3, encoding="UTF-8"):
    with open(name_file, mode, buffering, encoding) as f:
        all_data = csv.DictReader(f)
        dictionary_lists = []
        for dictionary in all_data:
            dictionary_lists.append(dictionary)
        return dictionary_lists

