"""
Dojot session

This class defines a Dojot Session object.
Methods for connecting to a Dojot server are defined.

Dependencies: requests

Author: jpaulovf@gmail.com

"""

import json
from datetime import datetime, timezone

import requests
from paho.mqtt import publish

from device import DojotDevice
from exceptions import RequestException
from template import DojotTemplate


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
        payload = {
            'username': self.get_username(),
            'passwd': self.get_password()
        }
        resp = requests.post(url, json=payload)
        if resp.status_code >= 400:
            raise RequestException(resp.status_code,
                                   resp.content.decode("utf-8"))
        self._jwt = resp.json()['jwt']

    def load_devices(self):
        url = f"{self.get_url()}/device"
        headers = {'Authorization': f"Bearer {self.get_jwt()}"}
        resp = requests.get(url, headers=headers)
        if resp.status_code >= 400:
            raise RequestException(resp.status_code,
                                   resp.content.decode("utf-8"))

        devices = []
        for dev in resp.json()['devices']:
            devices.append(
                DojotDevice(dev['label'], dev['templates'], dev['id']))

        return devices

    def load_templates(self):
        url = f"{self.get_url()}/template"
        headers = {'Authorization': f"Bearer {self.get_jwt()}"}
        resp = requests.get(url, headers=headers)
        if resp.status_code >= 400:
            raise RequestException(resp.status_code,
                                   resp.content.decode("utf-8"))

        templates = []
        for temp in resp.json()['templates']:
            attrs = []
            for attr in temp['attrs']:
                attrs.append({
                    'label': attr['label'],
                    'type': attr['type'],
                    'value_type': attr['value_type']
                })
            templates.append(DojotTemplate(temp['label'], attrs, temp['id']))

        return templates

    def commit_template(self, template: DojotTemplate):
        url = f"{self.get_url()}/template"
        headers = {'Authorization': f"Bearer {self.get_jwt()}"}
        payload = {
            'label': template.get_label(),
            'attrs': template.get_attrs()
        }
        resp = requests.post(url, headers=headers, json=payload)
        if resp.status_code >= 400:
            raise RequestException(resp.status_code,
                                   resp.content.decode("utf-8"))
        template.set_id(resp.json()['template']['id'])
        return resp.json()

    def commit_device(self, device: DojotDevice):
        url = f"{self.get_url()}/device"
        headers = {'Authorization': f"Bearer {self.get_jwt()}"}
        payload = {
            'label': device.get_label(),
            'templates': device.get_templates()
        }
        resp = requests.post(url, headers=headers, json=payload)
        if resp.status_code >= 400:
            raise RequestException(resp.status_code,
                                   resp.content.decode("utf-8"))
        device.set_id(resp.json()['devices'][0]['id'])
        return resp.json()

    def publish_attrs(self, device: DojotDevice):
        hostname = self.get_url().replace("/", "").split(":")[1]
        topic = f"{self.get_username()}:{device.get_id()}/attrs"
        auth = {
            'username': f"{self.get_username()}:{device.get_id()}",
            'password': f"{self.get_password()}"
        }
        msg = json.dumps(device.get_attrs())
        publish.single(topic=topic, payload=msg, auth=auth, hostname=hostname)

    def get_history(self,
                    device: DojotDevice,
                    attr_name: str,
                    n_to_read: int = 1):
        url = f"{self.get_url()}/history/device/{device.get_id()}/"
        url_params = f"history?lastN={n_to_read}&attr={attr_name}"
        headers = {'Authorization': f"Bearer {self.get_jwt()}"}

        resp = requests.get(url + url_params, headers=headers)
        if resp.status_code >= 400:
            raise RequestException(resp.status_code,
                                   resp.content.decode("utf-8"))
        ts = [
            datetime.strptime(attr['ts'], "%Y-%m-%dT%H:%M:%S.%fZ")
            for attr in resp.json()
        ]
        ts = [t.replace(tzinfo=timezone.utc).astimezone(tz=None) for t in ts]
        val = [attr['value'] for attr in resp.json()]
        return ts, val
