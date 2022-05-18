"""
Dojot template

This class defines a Dojot Device object (from a template).

Dependencies: requests, paho-mqtt

Author: jpaulovf@gmail.com

"""

from .template import DojotTemplate


class DojotDevice:

    def __init__(self, label: str, templates: list = [], id: str = None):
        self._label = label
        self._templates = templates
        self._id = id

    def get_label(self):
        return self._label

    def get_templates(self):
        return self._templates

    def get_id(self):
        return self._id

    def set_id(self, id):
        self._id = id

    def add_template(self, template: DojotTemplate):
        if template.get_id() not in self._templates:
            self._templates.append(template.get_id())

    def remove_template(self, template: DojotTemplate):
        if template.get_id() in self._templates:
            self._templates.remove(template.get_id())

    def set_attrs(self, attrs: dict):
        self._attrs = attrs

    def get_attrs(self):
        return self._attrs

    def __str__(self):
        return (f"Dojot Device\n"
                f"Label: {self.get_label()}\n"
                f"Templates: {self.get_templates()}\n"
                f"ID: {self.get_id()}")
