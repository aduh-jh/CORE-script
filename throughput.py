from datetime             import datetime
from core.api.grpc.client import CoreGrpcClient


# Define interface and node names based on `topology.xml`
interface_names = {
    0: 'eth0',
    1: 'eth1',
    2: 'eth2'
}

node_names = {
    1: 'A',
    2: 'D',
    3: 'E',
    4: 'F',
    5: 'B',
    6: 'C'
}


# This function gets fed throughput events
def handler(event):
    for interface in event.iface_throughputs:
        throughput_kbps = interface.throughput/1000
        print(
            "throughput event",                                 "|",
            "time:",       datetime.now().strftime("%H:%M:%S"), "|",
            "node:",       node_names[interface.node_id],       "|",
            "interface:",  interface_names[interface.iface_id], "|",
            "throughput:", round(throughput_kbps, 3), "kbps",
        )


# Get the existing core session
client = CoreGrpcClient()
client.connect()
session = client.get_sessions()[0]

# Listen for throughput events and
# feed them into the handler function
# (see daemon/core/api/grpc/client.py)
throughputs = client.throughputs(session.id, handler)

while True:
    try:
        session = client.get_sessions()[0]
    except:
        # break if the session does not exist anymore
        break
