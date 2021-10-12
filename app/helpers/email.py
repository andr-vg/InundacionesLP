import re

def check(email):
    return re.fullmatch("^[^@]+@[^@]+\.[^@]+$", email)