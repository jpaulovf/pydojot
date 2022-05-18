"""
Custom exceptions

"""


class RequestException(Exception):

    def __init__(self, status_code, body):
        super().__init__(f"Status code = {status_code}, Body = {body}")
