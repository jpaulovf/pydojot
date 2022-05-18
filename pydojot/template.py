"""
Dojot template

This class defines a Dojot Template object.

Dependencies: requests

Author: jpaulovf@gmail.com

"""


class DojotTemplate:

    _available_vtypes = ("string", "float", "integer", "geo")
    _available_types = ("static", "dynamic", "actuator")

    def __init__(self, label: str, attrs: list = [], id: str = None):
        self._label = label
        self._attrs = attrs
        self._id = id

    def get_label(self):
        return self._label

    def get_attrs(self):
        return self._attrs

    def get_id(self):
        return self._id

    def set_id(self, id):
        self._id = id

    def add_attribute(self, label: str, type: str, value_type: str):
        if type not in self._available_types:
            raise ValueError(f"Invalid argument type '{type}'.")
        if value_type not in self._available_vtypes:
            raise ValueError(f"Invalid argument type '{value_type}'.")
        self._attrs.append({
            'label': str(label),
            'type': type,
            'value_type': value_type
        })

    def remove_attribute(self, label: str):
        to_remove = next(
            (i for i, x in enumerate(self._attrs) if x['label'] == label),
            None)
        if to_remove != None:
            self._attrs.pop(to_remove)

    def __str__(self):
        return (f"Dojot Template\n"
                f"Label: {self.get_label()}\n"
                f"Attrs: {self.get_attrs()}\n"
                f"ID: {self.get_id()}")

    def __len__(self):
        return len(self._attrs)

    def __getitem__(self, item):
        return self._attrs[item]
