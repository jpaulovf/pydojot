"""
pydojot: operating with existing templates/devices
"""

import random

from pydojot.session import DojotSession

# Open a new session
session = DojotSession("http://localhost:8000",
                       username="admin",
                       password="admin")

# Loading existing templates in the opened session
existing_templates = session.load_templates()

# Checking templates
for template in existing_templates:
    print(template)

# Loading existing devices in the opened session
existing_devices = session.load_devices()

# Checking devices
for device in existing_devices:
    print(device)

# Sending data to existing devices
for k in range(0, 100):
    for device in existing_devices:
        device.set_attrs({
            "MyString": f"test {k}",
            "MyInteger": random.randint(0, 10),
            "MyFloat": random.random()
        })
        session.publish_attrs(device)
