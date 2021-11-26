import requests

from auth import AuthFedex


def renew_access_token(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except requests.ConnectionError:
            AuthFedex.getting_a_token()
            return func(*args, **kwargs)

    return wrapper
