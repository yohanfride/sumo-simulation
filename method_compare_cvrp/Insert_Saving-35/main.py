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


bus_id = []
routes = ET.parse('Clark35-trips.xml')
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
laststop = ["0" for i in range(len(bus_id))];
start_time = [0 for i in range(len(bus_id))]
current_stopid = ["0" for i in range(len(bus_id))]
route = [[] for i in range(len(bus_id))]
tw = [[] for i in range(len(bus_id))]
leading = [[] for i in range(len(bus_id))]
delay = [[] for i in range(len(bus_id))]
steps = [[] for i in range(len(bus_id))]
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
            if laststop[i] != current_stopid[i]:
                x = laststop[i].replace("busStop_", "").replace("depot","0")
                y = current_stopid[i].replace("busStop_", "").replace("depot","0")
                
                laststop[i] = current_stopid[i]
                listtime[i].append(step - start_time[i])
                start_time[i] = step

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
        'rute':route[i],
        'time_window':tw[i],
        'leading':leading[i],
        'delay':delay[i],
        'step':steps[i],
        'time':total-listtime[i][0]
    }
    vehicle.append(v)


with open('waktu.json', 'w') as outfile:
    json.dump(vehicle, outfile)
