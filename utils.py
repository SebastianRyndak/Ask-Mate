import bcrypt
file_extention = ["JPG", "PNG"]
INVALID_LOGIN_ATTEMPT="""
                            <script>
                            alert('Invalid login attempt')
                            window.location='/login'
                            </script>
                            """


ENTER_ALL_VALUES="""
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


def get_user_id(question_data):
    for data in question_data:
        return data.get('user_id')