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

print("Starting the TraCI server...")
traci.start(sumoCmd) 

print("Subscribing to vehicle data...")
bus_id = "veh0"
traci.vehicle.subscribe(bus_id, (tc.VAR_COLOR, tc.VAR_SPEED, tc.VAR_ACCELERATION, tc.VAR_POSITION, tc.VAR_LANE_ID, tc.VAR_LANEPOSITION))
listtime = []
step = 0
laststop = "";
start_time = 0
while step < 10000:
    # advance the simulation
    print("\nsimulation step: %i" % step)
    traci.simulationStep()
    ids = traci.vehicle.getIDList()
    if bus_id in ids:
        stops = traci.vehicle.getNextStops(bus_id)
        if len(stops) > 0:
            next_stop = stops[0]
            current_stopid = next_stop[2]
        
        if laststop != current_stopid:
            laststop = current_stopid
            listtime.append(step - start_time)
            start_time = step
            print(current_stopid)
            print(laststop)
            print(listtime)
            
    step += 1
    # time.sleep(0.1)