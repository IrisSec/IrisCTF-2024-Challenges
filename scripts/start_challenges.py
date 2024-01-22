import json
import os

with open("./challenges.json") as f:
    challenges = json.load(f)

ports = {}

for challenge, props in challenges.items():
    # TODO R3

    if props["server"] == "none":
        continue # static

    os.chdir(challenge)
    with open("challenge.yaml") as f:
        yaml = f.read()
    if props["started"]:
        yaml = yaml.replace("deployed: false", "deployed: true")
        if props["server"] == "tcp":
            ports[challenge] = props["port"]
            yaml = yaml.replace("public: true", "public: false")
        elif props["server"] == "https":
            yaml = yaml.replace("public: false", "public: true")
    else:
        yaml = yaml.replace("deployed: true", "deployed: false")

    with open("challenge.yaml", "w") as f:
        f.write(yaml)

    os.chdir("..")

with open("nginx.yaml.base", "r") as f:
    base = f.read()

data1 = "\n".join(f"  {port}: \"default/{challenge}:1337\"" for challenge, port in ports.items())
ports = {k.replace("_", "-")[:15] : v for k, v in ports.items()}
data2 = "\n".join(f"  - appProtocol: tcp\n    name: {challenge}\n    port: {port}\n    protocol: TCP\n    targetPort: {challenge}" for challenge, port in ports.items())
data3 = "\n".join(f"        - containerPort: {port}\n          name: {challenge}\n          protocol: TCP" for challenge, port in ports.items())

with open("nginx.yaml", "w") as f:
    f.write(base.replace("{data1}", data1).replace("{data2}", data2).replace("{data3}", data3))

