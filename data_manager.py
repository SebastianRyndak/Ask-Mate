import connection
from datetime import datetime
import time
import os
from operator import itemgetter
import datetime
import csv
from typing import List, Dict
from psycopg2 import sql
from psycopg2.extras import RealDictCursor
import database_common

ANSWER_DATA_PATH = os.getenv("ANSWER_DATA_PATH") if "ANSWER_DATA_PATH" in os.environ else "sample_data/answer.csv"
QUESTION_HEADERS = ["id", "submission_time", "view_number", "vote_number", "title", "message", "image"]
ANSWER_HEADERS = ["id", "submission_time", "vote_number", "question_id", "message", "image"]
TABLE_HEADERS = {"vote_number": "Votes", "title": "Title", "message": "Message", "submission_time": "Date",
                 "view_number": "Views"}
SORT_BY_INT = ["vote_number", "Published on", "view_number"]
file_extention = ["JPG", "PNG"]
reverse = 0  # global variable


@database_common.connection_handler
def get_question_bd(cursor):
    cursor.execute("""
        SELECT *
        FROM question
        """)
    return cursor.fetchall()


@database_common.connection_handler
def vote_for_answers(cursor, answer_id, vote_number, question_id):
    query = """
        UPDATE answer
        SET vote_number = %(vote_number)s,
            question_id = %(question_id)s
        WHERE id = %(answer_id)"""
    cursor.execute(query, {'vote_number': vote_number, 'answer_id': answer_id, 'question_id': question_id})
    return cursor.fetchall()


@database_common.connection_handler
def edit_answer(cursor, answer_id, edited_answer):
    query = sql.SQL("""
        UPDATE answer
        SET message = %(edited_answer)s
        WHERE id = %(answer_id)s
        """).format(
        answer_id=sql.Identifier('id'),
        edited_answer=sql.Identifier('message')
    )
    cursor.execute(query, {'answer_id': answer_id, 'edited_answer': edited_answer})


@database_common.connection_handler
def return_question_id_and_message(cursor, answer_id):
    query = """
        SELECT question_id, message
        FROM answer
        WHERE id = %(answer_id)s"""
    cursor.execute(query, {'answer_id': answer_id})
    return cursor.fetchall()

@database_common.connection_handler
def find_title_and_message(cursor, question_id):
    query = sql.SQL("""
        SELECT title, message, image
        FROM question
        WHERE id = %(question_id)s
        ORDER BY title""").format(
        question_id=sql.Identifier('question_id')
    )
    cursor.execute(query, {'question_id': question_id})
    return cursor.fetchall()

@database_common.connection_handler
def get_question_db_by_question_id(cursor, question_id):
    query = """
        SELECT *
        FROM question
        WHERE id = %(question_id)s
        """
    cursor.execute(query, {'question_id': question_id})
    return cursor.fetchall()

@database_common.connection_handler
def save_new_answer(cursor, message, question_id, vote_number, submission_time, image):
    query = """
        INSERT INTO answer
        (submission_time, vote_number, question_id, message, image)
        VALUES (%(submission_time)s, %(vote_number)s, %(question_id)s, %(message)s, %(image)s);"""

    cursor.execute(query, {'submission_time': submission_time, 'vote_number': vote_number,
                           'question_id': question_id, 'message': message, 'image': image})


@database_common.connection_handler
def save_new_question(cursor, message, vote_number, submission_time, image, title, view_number):
    query = """
        INSERT INTO question
        (submission_time, vote_number, message, image, title, view_number)
        VALUES (%(submission_time)s, %(vote_number)s, %(message)s, %(image)s, %(title)s, %(view_number)s);"""

    cursor.execute(query, {'submission_time': submission_time, 'vote_number': vote_number,
                           'view_number': view_number, 'message': message, 'image': image, 'title': title})


@database_common.connection_handler
def find_all_answer_to_question(cursor, question_id):
    query = sql.SQL("""
        SELECT message, question_id, vote_number, image, id
        FROM answer
        WHERE question_id = %(question_id)s""").format(
        question_id=sql.Identifier('question_id')
    )
    cursor.execute(query, {'question_id': question_id})
    return cursor.fetchall()

@database_common.connection_handler
def delete_question(cursor, question_id):
    query = """
        DELETE FROM question
        WHERE id = %(question_id)s"""
    cursor.execute(query, {'question_id': question_id})


@database_common.connection_handler
def delete_answers_from_question(cursor, question_id):
    query = """
        DELETE FROM answer
        WHERE question_id = %(question_id)s"""
    cursor.execute(query, {'question_id': question_id})


@database_common.connection_handler
def delete_answers_from_comment(cursor, question_id):
    query = """
        DELETE FROM comment
        WHERE question_id = %(question_id)s"""
    cursor.execute(query, {'question_id': question_id})


@database_common.connection_handler
def delete_answers_from_question_tag(cursor, question_id):
    query = """
        DELETE FROM question_tag
        WHERE question_id = %(question_id)s"""
    cursor.execute(query, {'question_id': question_id})


@database_common.connection_handler
def delete_answer_from_db_by_id(cursor, answer_id):
    query = """
            DELETE FROM answer
            WHERE id = %(answer_id)s"""
    cursor.execute(query, {'answer_id': answer_id})


@database_common.connection_handler
def delete_answer_from_comment_by_id(cursor, answer_id):
    query = """
            DELETE FROM comment
            WHERE answer_id = %(answer_id)s"""
    cursor.execute(query, {'answer_id': answer_id})
=======
def save_new_answer(message, image, question_id):
        write_answer_to_db(datetime.datetime.now(), 0, question_id, message, image)


@database_common.connection_handler
def get_question_id_by_answer_id_db(cursor, answer_id):
    query = """
        SELECT question_id
        FROM answer
        WHERE id=%s
    """
    cursor.execute(query, (answer_id,))
    real_dict = cursor.fetchall()
    real_dict_to_list = []
    for item in real_dict:
        real_dict_to_list.append(dict(item))
    return real_dict_to_list[0]["question_id"]



@database_common.connection_handler
def write_answer_to_db(cursor, submission_time, vote_number, question_id, message, image):
    query = sql.SQL("""
    INSERT INTO answer (submission_time, vote_number, question_id, message, image) 
    VALUES (%(submission_time)s,%(vote_number)s,%(question_id)s,%(message)s,%(image)s)
    """).format(submission_time=sql.Identifier('submission_time'),
                vote_number=sql.Identifier('vote_number'),
                question_id=sql.Identifier('question_id'),
                message=sql.Identifier('message'),
                image=sql.Identifier('image'))
    cursor.execute(query, {'submission_time': submission_time, 'vote_number': vote_number,
                           "question_id": question_id, "message": message, "image": image})



@database_common.connection_handler
def delete_answer_from_cvs_by_id_db(cursor, id):
    query = sql.SQL("""
    DELETE FROM answer
    WHERE id = %(id)s""").format(id=sql.Identifier('id'))
    cursor.execute(query, {"id": id})



def allowed_image(filename):
    if not "." in filename:
        return False
    ext = filename.rsplit(".", 1)[1]
    if ext.upper() in file_extention:
        return True
    else:
        return False


@database_common.connection_handler
def delete_comment_by_question_id(cursor, question_id):
    query = sql.SQL("""
    DELETE FROM comment
    WHERE question_id = %(question_id)s""").format(id=sql.Identifier('question_id'))
    cursor.execute(query, {"question_id": question_id})


@database_common.connection_handler
def delete_comment_by_answer_id(cursor, answer_id):
    query = sql.SQL("""
    DELETE FROM comment
    WHERE answer_id = %(answer_id)s""").format(id=sql.Identifier('answer_id'))
    cursor.execute(query, {"answer_id": answer_id})

    
@database_common.connection_handler
def get_question_bd(cursor):
    cursor.execute("""
        SELECT *
        FROM question
        """)
    return cursor.fetchall()

