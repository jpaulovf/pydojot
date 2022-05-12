"""
Dojot template

This class defines a Dojot Template object.

Dependencies: requests

Author: jpaulovf@gmail.com

"""

from .session import DojotSession
from .exceptions import RequestException
import requests

class DojotTemplate:

    _available_vtypes = ("string", "float", "integer", "geo")
    _available_types = ("static", "dynamic", "actuator")

    def __init__(self, label):
        self._label = label
        self._attrs = []
        self._id = None

    def get_label(self):
        return self._label

    def get_attrs(self):
        return self._attrs

    def get_id(self):
        return self._id

    def add_attribute(self, label: str, type: str, value_type: str):
        if type not in self._available_types:
            raise ValueError(f"Invalid argument type '{type}'.")
        if value_type not in self._available_vtypes:
            raise ValueError(f"Invalid argument type '{value_type}'.")
        self._attrs.append({'label': str(label), 'type': type, 'value_type': value_type})

    def remove_attribute(self, label: str):
        to_remove = next((i for i, x in enumerate(self._attrs) if x['label'] == label), None)
        if to_remove != None:
            self._attrs.pop(to_remove)

    def commit(self, session: DojotSession):
        url = f"{session.get_url()}/template"
        headers = {'Authorization': f"Bearer {session.get_jwt()}"}
        payload = {'label': self.get_label(), 'attrs': self.get_attrs()}
        resp = requests.post(url, headers=headers, json=payload)
        if resp.status_code >= 400:
            raise RequestException(resp.status_code, resp.content.decode("utf-8"))
        self._id = resp.json()['template']['id']
        return resp.json()

    def __str__(self):
        return f"Label: {self._label}\nAttrs: {self._attrs}"

    def __len__(self):
        return len(self._attrs)

    def __getitem__(self, item):
        return self._attrs[item]

