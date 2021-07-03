import os, sys
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:   
    sys.exit("please declare environment variable 'SUMO_HOME'")

sumoBinary = "C:/Program Files (x86)/Eclipse/Sumo/bin/sumo-gui"
sumoConfig = ["-c", "map-bsd1.sumocfg", "-S"]
sumoCmd = [sumoBinary, sumoConfig[0], sumoConfig[1], sumoConfig[2]]

import traci
import traci.constants as tc
import sumolib
import time
import json
import xml.etree.ElementTree as ET
from xml.dom import minidom
import numpy as np
import pandas as pd
import random
import warnings
import datetime
warnings.filterwarnings('ignore')



# get customer demand and location data
n = 15
customer = [i for i in range(1, n + 1)]
node = [0] + customer
arcos = [(i,j) for i in node for j in node if i != j]
f = open('pelanggan4.json')
data = json.load(f)
df = pd.DataFrame(data)
distance = np.loadtxt('distance.txt')
vehicle_capacity = 250
demand = df.demand
duration = np.loadtxt('duration.txt')
# Service time
ser = [df['service_time'][i] for i in range(n + 1)]
ser[0] = 0
# Start time
e = [df['ready_time'][i] for i in range(n + 1)]
e[0] = 0
# Due time
l = [df['due_time'][i] for i in range(n + 1)]


def serviceTimeChek(s_time,i,j):
    cekData =  data[j]
    cekTime = s_time + duration[i][j]
    if cekTime >= cekData["ready_time"] and cekTime <= cekData["due_time"] :
        return True
    else:
        return False

def serviceTimeChek2(s_time,i,j):
    cekData =  data[j]
    cekTime = s_time + duration[i][j]
    if cekTime <= cekData["due_time"] :
        return True
    else:
        return False

def saving(data_distance,data_duration,node,i,s_time):
    if i == 0:
        [i,j] = savingFirst(data_distance, data_duration, node, s_time)
        res = i
        return res
    max_saving = 0
    max_saving2 = 0
    res = 0
    res2 = 0
    for j in range(1,n+1):
        if (j in node) and (j != i):
            S1 = data_distance[i][0] + data_distance[0][j] - data_distance[i][j]
            if(max_saving<S1):
                if(serviceTimeChek(s_time,i,j)):
                    max_saving = S1
                    res = j
            if(max_saving2<S1):
                if(serviceTimeChek2(s_time,i,j)):
                    max_saving2 = S1
                    res2 = j
    if(res == 0):
        res = res2
    return res

def savingFirst(data_distance, data_duration, node, s_time):
    max_saving = 0
    res = [0,0]
    max_saving2= 0
    res2= [0,0]
    for i in range(1,n+1):
        for j in range(1,n+1):
            if (j in node) and (i in node) and (j != i):
                S1 = data_distance[i][0] + data_distance[0][j] - data_distance[i][j]
                if(max_saving<S1):
                    if(serviceTimeChek(s_time,i,j)):
                        max_saving = S1
                        res = [i,j]
                if(max_saving2<S1):
                    if(serviceTimeChek2(s_time,i,j)):
                        max_saving2 = S1
                        res2 = [i,j]
                    
    if(res == [0,0]):
        res = res2
    return res

def action(nodes, capacity, s_time, i):
    if i == 0 :
        capacity = vehicle_capacity
    else:
        capacity-=df.demand[i]

    j = saving(distance,duration,nodes,i,s_time)
    if (capacity - demand[j] > 0) and (j > 0) :
        nodes.remove(j)
    else: 
        j = 0
    i = j    
    return nodes, capacity, i


def generateRandomVehicle():
    cmd = "python D:/PASCA/Thesis-kerja/sumo/tools/randomTrips.py -n BSD.net.xml -r bsd.rou.xml -e 500 -l"
    returned_value = os.system(cmd)  # returns the exit code in unix

    import xml.etree.ElementTree as ET
    from xml.dom import minidom

    our_route = ET.parse('list.rou.xml')
    random_route = ET.parse('bsd.rou.xml')
    root_our_route = our_route.getroot()
    root_random_route = random_route.getroot()
    for child in root_our_route:
        atr_child = child.attrib
        current_group = ET.Element('route', {'id':atr_child['id'],'edges':atr_child['edges']})
        root_random_route.insert(0,current_group)

    xmlst = minidom.parseString(ET.tostring(root_random_route)).toprettyxml(indent="   ")
    with open("bsd.rou.xml", "w") as f:
        f.write(xmlst)

    with open("save_route/"+exp_time+".rou.xml", "w") as f:
        f.write(xmlst)


MaxEpisode = 22
for episode in range(MaxEpisode):
    now = datetime.datetime.now()
    exp_time = now.strftime("%Y-%m-%d %H%M%S")

    bus_id = ['veh0','veh1','veh2']
    listtime = [[] for i in range(len(bus_id))]
    step = 0
    laststop = ["0" for i in range(len(bus_id))];
    start_time = [0 for i in range(len(bus_id))]
    current_stopid = ["0" for i in range(len(bus_id))]
    route = [[] for i in range(len(bus_id))]
    tw = [[] for i in range(len(bus_id))]
    leading = [[] for i in range(len(bus_id))]
    delay = [[] for i in range(len(bus_id))]
    steps = [[] for i in range(len(bus_id))]
    cek = [True for i in range(len(bus_id))]
    cek2 = [0 for i in range(len(bus_id))]
    v_capacity = [vehicle_capacity for i in range(len(bus_id))]
    last_node = [0 for i in range(len(bus_id))]
    lastrute = ["" for i in range(len(bus_id))]
    nodes = node[1:]


    generateRandomVehicle()

    print("Starting the TraCI server...")
    traci.start(sumoCmd, label="sim"+exp_time) 

    print("Subscribing to vehicle data...")


    ### First Route
    for i in range(len(bus_id)): 
        x = last_node[i]
        nodes,v_capacity[i],y = action(nodes,v_capacity[i],0,0)
        bstop = "busStop_"+str(y)
        srute = "rute_"+str(x)+"_"+str(y)
        last_node[i] = y
        traci.vehicle.add(bus_id[i], srute, depart="1.0")
        traci.vehicle.setColor(bus_id[i],(255,0,0))
        traci.vehicle.setBusStop(bus_id[i], bstop, duration=240)
        laststop[i] = bstop
        print(bus_id[i]+" --> "+srute+" --> "+bstop)
        lastrute[i] = srute

    while step < 5000:
        # advance the simulation
        # print("\nsimulation step: %i" % step)
        traci.simulationStep()   
        ids = traci.vehicle.getIDList()
        for i in range(len(bus_id)):                
            if bus_id[i] in ids:
                stops = traci.vehicle.getNextStops(bus_id[i])
                if len(stops) > 0:
                    next_stop = stops[0]
                    current_stopid[i] = next_stop[2]
                else:
                    current_stopid[i] = "" 
                    if lastrute[i] != "":
                        rts = lastrute[i].replace("rute_","").split("_")
                        x = rts[0]
                        y = rts[1]
                        lastrute[i] = ""
                        if(y != ''):
                            x = int(x)
                            y = int(y)
                            route[i].append((x,y))
                            tw[i].append(str(data[x]['ready_time'])+" --- "+str(data[x]['due_time']))        
                            dl = step - data[x]['due_time']
                            if dl < 0:
                                dl = 0
                            ld = data[x]['ready_time'] - step
                            if ld < 0:
                                ld = 0
                            leading[i].append(ld)
                            delay[i].append(dl)
                            steps[i].append(step)
                            listtime[i].append(step - start_time[i])
                            start_time[i] = step


                    if(len(nodes)>0):
                        x = last_node[i]
                        nodes,v_capacity[i],y = action(nodes,v_capacity[i],step,x)
                        last_node[i] = y
                        if(x != y):
                            stop_id = "busStop_"+str(y)
                            route_id = "rute_"+str(x)+"_"+str(y)
                            if( y == 0 ):
                                stop_id = "depot"
                            traci.vehicle.setRouteID(bus_id[i], route_id)
                            traci.vehicle.setBusStop(bus_id[i], stop_id, duration=240)
                            print(bus_id[i]+" --> "+route_id+" --> "+stop_id)
                            
                            laststop[i] = stop_id
                            lastrute[i] = route_id                       
                            print("Next Stop Vehicle "+str(i)+" --> "+stop_id)
                            cek[i] = True
        step += 1   

    vehicle = []
    for i in range(len(bus_id)):
        total = 0
        for j in range(len(listtime[i])):
            total+=listtime[i][j]
        v = {
            'vehicle':"Vehicle "+str(i),
            'listtime':listtime[i],
            'rute':route[i],
            'time_window':tw[i],
            'leading':leading[i],
            'delay':delay[i],
            'step':steps[i],
            'time':total
        }
        vehicle.append(v)


    with open('hasil/waktu-'+exp_time+'.json', 'w') as outfile:
        json.dump(vehicle, outfile)
