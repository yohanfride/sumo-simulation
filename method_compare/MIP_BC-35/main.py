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


bus_id = []
routes = ET.parse('MIP35-trips.xml')
root = routes.getroot()
for child in root:
    atr_child = child.attrib
    vehid = atr_child['id']
    bus_id.append(vehid)

print(bus_id)
print("Starting the TraCI server...")
traci.start(sumoCmd) 

print("Subscribing to vehicle data...")
# traci.vehicle.subscribe(bus_id[0], (tc.VAR_COLOR, tc.VAR_SPEED, tc.VAR_ACCELERATION, tc.VAR_POSITION, tc.VAR_LANE_ID, tc.VAR_LANEPOSITION))
# traci.vehicle.subscribe(bus_id[1], (tc.VAR_COLOR, tc.VAR_SPEED, tc.VAR_ACCELERATION, tc.VAR_POSITION, tc.VAR_LANE_ID, tc.VAR_LANEPOSITION))
# traci.vehicle.subscribe(bus_id[2], (tc.VAR_COLOR, tc.VAR_SPEED, tc.VAR_ACCELERATION, tc.VAR_POSITION, tc.VAR_LANE_ID, tc.VAR_LANEPOSITION))

listtime = [[] for i in range(len(bus_id))]
step = 0
laststop = ["" for i in range(len(bus_id))];
start_time = [0 for i in range(len(bus_id))]
current_stopid = ["" for i in range(len(bus_id))]
while step < 3500:
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
            if laststop[i] != current_stopid[i]:
                laststop[i] = current_stopid[i]
                listtime[i].append(step - start_time[i])
                start_time[i] = step
                print("Next Stop Vehicle "+str(i)+" --> "+current_stopid[i])
            
    step += 1
    # time.sleep(0.1)

vehicle = []
for i in range(len(bus_id)):
    total = 0
    for n in range(len(listtime[i])):
        total+=listtime[i][n]
    v = {
        'vehicle':"Vehicle "+str(i),
        'listtime':listtime[i],
        'time':total
    }
    vehicle.append(v)


with open('waktu.json', 'w') as outfile:
    json.dump(vehicle, outfile)
