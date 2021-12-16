import bcrypt

import data_manager

file_extention = ["JPG", "PNG"]
RANK_CALC = {'question_up': 5, 'question_down': -2, 'answer_up': 10, 'answer_down': -2, 'answer_accept': 15}
RANKS = {'clone': [-10000, 1], 'padawan': [1, 201], 'jedi': [201, 1001], 'jedi master': [1001, 2001],
         'jedi council': [2000, 10000]}

INVALID_LOGIN_ATTEMPT = """
                            <script>
                            alert('Invalid login attempt')
                            window.location='/login'
                            </script>
                            """

ENTER_ALL_VALUES = """
                <script>
                alert('Enter all values!!!')
                window.location='/login'
                </script>
                """

YOU_ARE_LOGGED_IN = """"
                <script>
                    alert("You are logged in")
                    window.location= "/"
                </script>    
                """


def hash_password(plain_text_password):
    hashed_bytes = bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt())
    return hashed_bytes.decode('utf-8')


def verify_password(plain_text_password, hashed_password):
    hashed_bytes_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_bytes_password)


def allowed_image(filename):
    if not "." in filename:
        return False
    ext = filename.rsplit(".", 1)[1]
    if ext.upper() in file_extention:
        return True
    else:
        return False


def get_user_points():
    all_users = data_manager.get_all_usersnames()
    all_points = {}
    for user in all_users:
        z = user.get('id')
        points = data_manager.count_rank_points(user.get('id'))
        if points == None:
            all_points[user.get('username')] = 0
        else:
            all_points[user.get('username')] = points.get('votes')
    return all_points


def get_user_rank():
    user_points = get_user_points()
    user_rank = {}
    for user_id, points in user_points.items():
        for rank, points_range in RANKS.items():
            if points in range(points_range[0], points_range[1]):
                user_rank[user_id] = rank
    return user_rank
