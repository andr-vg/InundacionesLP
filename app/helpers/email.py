import re


def check(email):
    """
    retorna si el email dado corresponde a un email valido sintacticamente
    """
    return re.fullmatch("^[^@]+@[^@]+\.[^@]+$", email)
