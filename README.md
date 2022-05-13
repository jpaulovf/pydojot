# pydojot - Dojot module for Python

Under development!

See the Dojot's API documentation [here](https://dojotdocs.readthedocs.io/en/latest/)

---

## Dependencies

. [paho-mqtt](https://pypi.org/project/paho-mqtt/)

## Examples

### Opening a Dojot session
For this example, consider a Dojot server running on 'localhost' at port 8000.

```python

from pydojot.session import DojotSession

# Creating a new session. Logging in as "admin" with password "admin"
session = DojotSession("http://localhost:8000", username="admin", password="admin")

```

### Creating a template
Consider that we already opened a session by instancing a *DojotSession* object, as shown in the previous example.
```python

from pydojot.template import DojotTemplate

# Creating an empty template
template = DojotTemplate("My Template")

# Adding some attributes to template
template.add_attribute(label="MyString", type="dynamic", value_type="string")
template.add_attribute(label="MyInteger", type="dynamic", value_type="integer")
template.add_attribute(label="MyFloat", type="dynamic", value_type="float")

# Uploading the template to the server (opened session)
session.commit_template(template)

# The line above will generate an ID for the template.
# You can print the template to check its parameters.
print(template)
```

### Creating a device from a template
For this next example, let's consider the session and template shown above.
```python

from pydojot.device import DojotDevice

# Creating an empty device
device = DojotDevice("My Device")

# Adding a template to this device
device.add_template(template)

# Uploading the device to the server (opened session)
session.commit_device(device)

# The line above will generate an ID for the device.
# You can print the device to check its parameters.
print(device)
```

### Sending MQTT data
In order to send a device MQTT data to the creted session, you'll need a two-step proccess:
1. Set the value for device's attributes;
2. Publish.

In the example below, let's send some random data.
```python

import random

for k in range(0,100):
    device.set_attrs({"MyString": f"test {k}",
                      "MyInteger": random.randint(0,10),
                      "MyFloat": random.random()})

    session.publish_attrs(device)
```

### Get a list of existing templates/devices in a session
You can get a list of the available templates and devices in an opened session.

```python

from pydojot.session import DojotSession

session = DojotSession("http://localhost:8000", username="admin", password="admin")

# This method returns a list of templates
templates = session.load_templates()

# This method returns a list of devices
devices = session.load_devices()
```
With a list of loaded devices, you can send data to any of the devices in the session.

```python

my_device = devices[2]

my_device.set_attrs({"MyString": "Hello",
                     "MyInteger": random.randint(0,10),
                     "MyFloat": random.random()})

session.publish_attrs(my_device)
```