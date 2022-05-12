"""
Dojot session

This class defines a Dojot Session object.
Methods for connecting to a Dojot server are defined.

Dependencies: requests

Author: jpaulovf@gmail.com

"""

import requests
from .exceptions import RequestException

class DojotSession:

    def __init__(self, url, username, password):
        self._url = url
        self._username = username
        self._password = password
        self.generate_jwt()

    def get_url(self):
        return self._url
    
    def get_username(self):
        return self._username

    def get_password(self):
        return self._password

    def get_jwt(self):
        return self._jwt

    def generate_jwt(self):
        url = f"{self.get_url()}/auth"
        payload = {'username': self.get_username(), 'passwd' : self.get_password()}
        resp = requests.post(url, json=payload)
        if resp.status_code >= 400:
            raise RequestException(resp.status_code, resp.content.decode("utf-8"))
        self._jwt = resp.json()['jwt']
