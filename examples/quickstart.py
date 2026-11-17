import os
from uptimescout import Client
client=Client(os.environ["UPTIMESCOUT_LICENSE_KEY"])
print(client.status("github"))
print(client.statuses(["github","telegram"]))
print(client.history("github",hours=24))
