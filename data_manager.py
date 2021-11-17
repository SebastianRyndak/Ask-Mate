import connection

ANSWER_LIST = connection.create_list(file="sample_data/answer.csv")
QUESTION_LIST = connection.create_list(file="sample_data/question.csv")


def find_title_and_message(question_id):
    for i in QUESTION_LIST:
        if i["id"] == str(question_id):
            title = i["title"]
            message = i["message"]
            return title, message


def find_all_answer_to_question(question_id):
    answer = []
    vote = []
    for i in QUESTION_LIST:
        if i["id"] == str(question_id):
            for j in ANSWER_LIST:
                if j["question_id"] == str(question_id):
                    answer.append(j.get("message"))
                    vote.append(j.get("vote_number"))
                else:
                    pass
        else:
            pass

    answer_len = len(answer)
    pack = list(zip(answer, vote))
    return pack, answer_len
