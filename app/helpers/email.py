import re

def check(email):
    return re.fullmatch("[a-zA-Z0-9.]+@[a-zA-Z0-9]+.[a-zA-Z0-9]+", email)