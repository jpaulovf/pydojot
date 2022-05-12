"""
Dojot template

This class defines a Dojot Device object (from a template).

Dependencies: requests, paho-mqtt

Author: jpaulovf@gmail.com

"""

from .session import DojotSession
from .template import DojotTemplate
from .exceptions import RequestException
import requests
from paho.mqtt import publish
import json
from datetime import datetime, timezone

class DojotDevice:

    def __init__(self, label):
        self._label = label
        self._templates = []
        self._id = None

    def get_label(self):
        return self._label

    def get_templates(self):
        return self._templates

    def get_id(self):
        return self._id

    def add_template(self, template: DojotTemplate):
        if template.get_id() not in self._templates:
            self._templates.append(template.get_id())

    def remove_template(self, template: DojotTemplate):
        if template.get_id() in self._templates:
            self._templates.remove(template.get_id())

    def commit(self, session: DojotSession):
        url = f"{session.get_url()}/device"
        headers = {'Authorization': f"Bearer {session.get_jwt()}"}
        payload = {'label': self.get_label(), 'templates': self.get_templates()}
        resp = requests.post(url, headers=headers, json=payload)
        if resp.status_code >= 400:
            raise RequestException(resp.status_code, resp.content.decode("utf-8"))
        self._id = resp.json()['devices'][0]['id']

        return resp.json()

    def set_attrs(self, attrs: dict):
        self._attrs = attrs

    def get_attrs(self):
        return self._attrs

    def publish_attrs(self, session: DojotSession):
        hostname = session.get_url().replace("/","").split(":")[1]
        topic = f"{session.get_username()}:{self.get_id()}/attrs"
        auth = {
                'username': f"{session.get_username()}:{self.get_id()}",
                'password': f"{session.get_password()}"
               }
        msg = json.dumps(self.get_attrs())
        publish.single(topic=topic, payload=msg, auth=auth, hostname=hostname)

    def get_history(self, session: DojotSession, attr_name: str, n_to_read: int = 1):
        url = f"{session.get_url()}/history/device/{self.get_id()}/"
        url_params=f"history?lastN={n_to_read}&attr={attr_name}"
        headers = {'Authorization': f"Bearer {session.get_jwt()}"}
        
        resp = requests.get(url + url_params, headers=headers)
        if resp.status_code >= 400:
            raise RequestException(resp.status_code, resp.content.decode("utf-8"))
        
        ts = [datetime.strptime(attr['ts'], "%Y-%m-%dT%H:%M:%S.%fZ") for attr in resp.json()]
        ts = [t.replace(tzinfo=timezone.utc).astimezone(tz=None) for t in ts]
        val = [attr['value'] for attr in resp.json()]

        return ts, val