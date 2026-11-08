This scenario emulates the network topology shown below in CORE:

![topology](topology.png)

# Prerequisites

Install the CORE Docker container:
```
docker pull ghcr.io/coreemu/core-ubuntu:v9.2.1
```

# How to run scenario
1. Run `core-cleanup`.
2. Run the CORE GUI (`core-gui`), open `topology.xml` and start the session.
3. Run `/opt/core/venv/bin/python3 -u scenario.py > output.txt`
4. Stop the session.

This will dump the terminal output to `output.txt`.
