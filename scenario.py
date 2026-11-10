# CORE repository: https://github.com/coreemu/core

import subprocess
import time

from datetime import datetime


NODE_A = '/tmp/pycore.1/A'
NODE_E = '/tmp/pycore.1/E'

NODE_D_IP = '10.0.2.20'
NODE_F_IP = '10.0.4.20'

DELAY_1 = 300 # 5-minute delay for A to D delivery
DELAY_2 = 60  # an extra minute delay for E to F delivery

DURATION_1 = 300 # 5-minute time window for A to D delivery
DURATION_2 = 180 # 3-minute time window for E to F delivery

PACKET_SIZE = 992 # 8 bytes for ICMP header (1000 bytes total)

# Define command to send a 1000 byte packet every second from A to D
A2D_CMD = f"ping -i 1 -s {PACKET_SIZE} -w {DURATION_1} {NODE_D_IP}"
A2D_CMD = ['vcmd', '-c', NODE_A, '--', 'bash', '-c', A2D_CMD]

# Define command to send a 1000 byte packet every 2 seconds from E to F
E2F_CMD = f"ping -i 2 -s {PACKET_SIZE} -w {DURATION_2} {NODE_F_IP}"
E2F_CMD = ['vcmd', '-c', NODE_E, '--', 'bash', '-c', E2F_CMD]

# Define command to output throughput data
THROUGHPUT_CMD = ['/opt/core/venv/bin/python3', '-u', 'throughput.py']

print('\nCurrent time: ' + datetime.now().strftime('%H:%M:%S'))

# Run throughput script
throughput_process = subprocess.Popen(THROUGHPUT_CMD, stdin=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

time.sleep(DELAY_1)

print('\nStarting packet delivery from node A to node D at ' + datetime.now().strftime('%H:%M:%S'))
print()

# start packet delivery from A to D
process_1 = subprocess.Popen(A2D_CMD, stdin=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

time.sleep(DELAY_2)

print('\nStarting packet delivery from node E to node F at ' + datetime.now().strftime('%H:%M:%S'))
print()

# start packet delivery from E to F
process_2 = subprocess.Popen(E2F_CMD, stdin=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# print packet delivery completion times
while process_1.returncode is None or process_2.returncode is None:
    if process_1.returncode is None and process_1.poll() is not None:
        print("\nA to D packet delivery finished at " + datetime.now().strftime('%H:%M:%S'))

    if process_2.returncode is None and process_2.poll() is not None:
        print("\nE to F packet delivery finished at " + datetime.now().strftime('%H:%M:%S'))

# Terminate throughput script
throughput_process.terminate()

print('DONE!')
