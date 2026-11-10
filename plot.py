from datetime   import datetime
from matplotlib import pyplot   as plt
from matplotlib import dates


def plot_throughput(nodes, ad_start_time, ef_start_time, ad_end_time, ef_end_time):
    '''
    This function plots the throughput data for each node
    '''
    
    figure, subplots = plt.subplots(3, 2, figsize=(16, 8))
    subplots         = subplots.flatten()
    
    figure.subplots_adjust(hspace=0.5)
    figure.canvas.manager.set_window_title('Throughput')
    
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
    

# MAIN

OUTPUT_FILE = "output.txt"

# this dictionary holds all throughput data
# organized into nodes and interfaces
nodes = {}

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

plot_throughput(nodes, ad_start_time, ef_start_time, ad_end_time, ef_end_time)
