"""
pydojot's example: creating and manipulating devices and templates

"""

import json
import random

import matplotlib.pyplot as plt

from pydojot.device import DojotDevice
from pydojot.session import DojotSession
from pydojot.template import DojotTemplate

# Opening a new Dojot session @ localhost, port 8000
session = DojotSession("http://localhost:8000",
                       username="admin",
                       password="admin")

# Creating a new template called 'Test Template'
template = DojotTemplate(label="Test Template")

# Adding some attributes to template
template.add_attribute(label="MyString", type="dynamic", value_type="string")
template.add_attribute(label="MyInteger", type="dynamic", value_type="integer")
template.add_attribute(label="MyFloat", type="dynamic", value_type="float")

# Commit the template to the opened session
session.commit_template(template)
print(
    f"Created template '{template.get_label()}' with id: {template.get_id()}")

# Creating various devices
devices = []
for k in range(0, 3):

    # Create a new device based on the template
    device = DojotDevice(label=f"Test Device {k}")
    device.add_template(template)

    # Commit the device to the opened session
    session.commit_device(device)
    print(f"Created device '{device.get_label()}' with id: {device.get_id()}")

    # Adding created device to a device list
    devices.append(device)

# Setting and sending devices' parameters
print("Sending data to devices...")
for k in range(0, 100):
    for dev in devices:
        dev.set_attrs({
            "MyString": f"test {k}",
            "MyInteger": random.randint(0, 10),
            "MyFloat": random.random()
        })
        session.publish_attrs(dev)
        print(f"Published message {json.dumps(dev.get_attrs())} "
              f"to device {dev.get_id()}")

# Getting and plotting data history
plt.figure(1)
for dev in devices:
    ts, data = session.get_history(dev, "MyInteger", n_to_read=100)
    plt.plot(ts, data, lw=0.5, label=f"Device {dev.get_id()}")
plt.legend()
plt.xlabel("Date/time")
plt.ylabel("MyInteger value")
plt.title("Data history")
plt.show()
