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

f = open('pelanggan4.json')
data = json.load(f)

rute = [
    [0, 5, 15, 14, 13, 6, 0],
    [0, 2, 9, 8, 4, 3, 1, 0],
    [0, 10, 7, 12, 11, 0] 
]


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
pos = [0 for i in range(len(bus_id))]
cek = [True for i in range(len(bus_id))]
cek2 = [0 for i in range(len(bus_id))]
lastrute = ["" for i in range(len(bus_id))]

print("Starting the TraCI server...")
traci.start(sumoCmd) 

print("Subscribing to vehicle data...")


### First Route
for i in range(len(bus_id)): 
    bstop = "busStop_"+str(rute[i][1])
    srute = "rute_"+str(rute[i][0])+"_"+str(rute[i][1])
    pos[i] = 1
    traci.vehicle.add(bus_id[i], srute, depart="1.0")
    traci.vehicle.setColor(bus_id[i],(255,0,0))
    traci.vehicle.setBusStop(bus_id[i], bstop, duration=40)
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
                if(pos[i] < len(rute[i])):
                    rts = lastrute[i].replace("rute_","").split("_")
                    x = rts[0]
                    y = rts[1]
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

                pos[i]+=1
                if(pos[i] < len(rute[i])):                                        
                    route_id = "rute_"+str(rute[i][pos[i]-1])+"_"+str(rute[i][pos[i]])
                    stop_id = "busStop_"+str(rute[i][pos[i]])
                    if( rute[i][pos[i]] == 0 ):
                        stop_id = "depot"
                    traci.vehicle.setRouteID(bus_id[i], route_id)
                    traci.vehicle.setBusStop(bus_id[i], stop_id, duration=40)
                    print(bus_id[i]+" --> "+route_id+" --> "+stop_id+" --> "+str(pos[i])+" --> "+str(len(rute[i])))                    
                    print("Next Stop Vehicle "+str(i)+" --> "+stop_id)
                    laststop[i] = stop_id
                    lastrute[i] = route_id
                    cek[i] = True
                else:
                    if(cek2[i] == 0):
                        cek[i] = True
                    else:
                        cek[i] = False
                    cek2[i]+=1 
                
                if cek[i] :    
                    listtime[i].append(step - start_time[i])
                    start_time[i] = step
    step += 1   

vehicle = []
for i in range(len(bus_id)):
    total = 0
    for n in range(len(listtime[i])):
        total+=listtime[i][n]
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


with open('waktu-algo.json', 'w') as outfile:
    json.dump(vehicle, outfile)
