from datetime   import datetime
from matplotlib import pyplot   as plt
from matplotlib import dates
from re         import match


def plot_throughput(nodes, ad_start_time, ef_start_time, ad_end_time, ef_end_time):
    '''
    This function plots the throughput data for each node
    '''
    
    figure, subplots = plt.subplots(3, 2, figsize=(16, 8))
    subplots         = subplots.flatten()
    
    figure.subplots_adjust(hspace=0.5)
    figure.canvas.manager.set_window_title('Throughput Plots')
    
    colors = ['red', 'green', 'blue']
    
    for i, node in enumerate(nodes):
        subplots[i].set_title('Node ' + node)
        
        color_index = 0 
        
        for interface in nodes[node]:
            times       = []
            throughputs = []
            
            for time in nodes[node][interface]:
                times.append(datetime.strptime(time, '%H:%M:%S'))
                throughputs.append(float(nodes[node][interface][time]))
            
            subplots[i].plot(times, throughputs, label=interface, linewidth=1, color=colors[color_index])
            subplots[i].set_xlabel('Time')
            subplots[i].xaxis.set_major_locator(dates.MinuteLocator(interval=2))
            subplots[i].xaxis.set_major_formatter(dates.DateFormatter('%H:%M:%S'))
            subplots[i].set_ylabel('Throughput (kbps)')
            subplots[i].legend()
            
            color_index += 1
            
        subplots[i].axvline(
            x=datetime.strptime(ad_start_time.strip(), '%H:%M:%S'),
            linestyle='--',
            color='magenta',
            linewidth=1,
            alpha=0.6
        )
        
        subplots[i].axvline(
            x=datetime.strptime(ad_end_time.strip(), '%H:%M:%S'),
            linestyle='--',
            color='magenta',
            linewidth=1,
            alpha=0.6
        )
        
        subplots[i].axvline(
            x=datetime.strptime(ef_start_time.strip(), '%H:%M:%S'),
            linestyle='--',
            color='orange',
            linewidth=1
        )
        
        subplots[i].axvline(
            x=datetime.strptime(ef_end_time.strip(), '%H:%M:%S'),
            linestyle='--',
            color='orange',
            linewidth=1
        )
            
    plt.show()       
    

def plot_delay(nodes_ping, ad_start_time, ef_start_time, ad_end_time, ef_end_time):
    '''
    This function plots the round trip delay
    data from the `ping` utility
    '''
    
    times_D  = []
    delays_D = []
    
    times_F  = []
    delays_F = []
    
    for time in nodes_ping['D']:
        times_D.append(datetime.strptime(time, '%H:%M:%S'))
        delays_D.append(nodes_ping['D'][time])
        
    for time in nodes_ping['F']:
        times_F.append(datetime.strptime(time, '%H:%M:%S'))
        delays_F.append(nodes_ping['F'][time])
        
    figure, subplots = plt.subplots(1, 2, figsize=(16, 4))
    subplots         = subplots.flatten()
    
    figure.canvas.manager.set_window_title('Round-Trip Delay Plots')
    subplots[0].set_title('A to D Round-Trip Delay')
    subplots[1].set_title('E to F Round-Trip Delay')
    
    subplots[0].plot(times_D, delays_D, linewidth=1)
    subplots[0].set_xlabel('Time')
    subplots[0].set_ylabel('Delay (ms)')
    
    subplots[1].plot(times_F, delays_F, linewidth=1)
    subplots[1].set_xlabel('Time')
    subplots[1].set_ylabel('Delay (ms)')
    
    for i in range(0, 2):
        subplots[i].axvline(
            x=datetime.strptime(ad_start_time.strip(), '%H:%M:%S'),
            linestyle='--',
            color='magenta',
            linewidth=1,
            alpha=0.6
        )
        
        subplots[i].axvline(
            x=datetime.strptime(ad_end_time.strip(), '%H:%M:%S'),
            linestyle='--',
            color='magenta',
            linewidth=1,
            alpha=0.6
        )
        
        subplots[i].axvline(
            x=datetime.strptime(ef_start_time.strip(), '%H:%M:%S'),
            linestyle='--',
            color='orange',
            linewidth=1
        )
        
        subplots[i].axvline(
            x=datetime.strptime(ef_end_time.strip(), '%H:%M:%S'),
            linestyle='--',
            color='orange',
            linewidth=1
        )
        
        subplots[i].xaxis.set_major_formatter(dates.DateFormatter('%H:%M:%S'))
        
    plt.show()


# MAIN

OUTPUT_FILE = 'output.txt'
NODE_D_IP   = '10.0.2.20'
NODE_F_IP   = '10.0.4.20'

# this dictionary holds all throughput data
# organized into nodes and interfaces
nodes = {}

# this dictionary holds the round trip
# delay data
nodes_ping = {'D': {}, 'F': {}}

# read the output file and extract the data
with open(OUTPUT_FILE, "r") as output_file:
    for line in output_file:
        if 'Starting packet delivery from node A to node D' in line:
            ad_start_time = line.replace('Starting packet delivery from node A to node D at ', '')
            
        if 'Starting packet delivery from node E to node F' in line:
            ef_start_time = line.replace('Starting packet delivery from node E to node F at ', '')
            
        if 'E to F packet delivery finished' in line:
            ef_end_time = line.replace('E to F packet delivery finished at ', '')
            
        if 'A to D packet delivery finished' in line:
            ad_end_time = line.replace('A to D packet delivery finished at ', '')
            
        if "throughput event" in line:
            line_content = line.split(' | ')
            time         = line_content[1].replace('time: ', '')
            node         = line_content[2].replace('node: ', '')
            interface    = line_content[3].replace('interface: ', '')
            throughput   = line_content[4].replace('throughput: ', '').replace(' kbps\n', '')
            
            if node not in nodes:
                nodes[node] = {}
            
            if interface not in nodes[node]:
                nodes[node][interface] = {}
                
            nodes[node][interface][time] = throughput
        
        # if the line starts with "b...1000"
        if match(r"^b.*1000", line):
            ping_output      = line[2:-2].split(' ')
            time             = ping_output[0]
            ip               = ping_output[4][:-1]
            round_trip_delay = float(ping_output[7].replace('time=', ''))
            
            if ip == NODE_D_IP:
                nodes_ping['D'][time] = round_trip_delay
            elif ip == NODE_F_IP:
                nodes_ping['F'][time] = round_trip_delay
                    

plot_throughput(nodes, ad_start_time, ef_start_time, ad_end_time, ef_end_time)
plot_delay(nodes_ping, ad_start_time, ef_start_time, ad_end_time, ef_end_time)
