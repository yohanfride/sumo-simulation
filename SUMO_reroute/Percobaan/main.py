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


print("Starting the TraCI server...")
traci.start(sumoCmd) 

print("Subscribing to vehicle data...")
# traci.vehicle.subscribe(bus_id[0], (tc.VAR_COLOR, tc.VAR_SPEED, tc.VAR_ACCELERATION, tc.VAR_POSITION, tc.VAR_LANE_ID, tc.VAR_LANEPOSITION))
# traci.vehicle.subscribe(bus_id[1], (tc.VAR_COLOR, tc.VAR_SPEED, tc.VAR_ACCELERATION, tc.VAR_POSITION, tc.VAR_LANE_ID, tc.VAR_LANEPOSITION))
# traci.vehicle.subscribe(bus_id[2], (tc.VAR_COLOR, tc.VAR_SPEED, tc.VAR_ACCELERATION, tc.VAR_POSITION, tc.VAR_LANE_ID, tc.VAR_LANEPOSITION))
step = 0
bus_id = 'veh0'
route_id = "rute_2_9"
stop_id = "busStop_9"
current_stopid = ""
laststop = "0"
while step < 5000:
    # advance the simulation
    # print("\nsimulation step: %i" % step)
    traci.simulationStep()
    ids = traci.vehicle.getIDList()
    if bus_id in ids:
        stops = traci.vehicle.getNextStops(bus_id)
        if len(stops) > 0:
            next_stop = stops[0]
            current_stopid = next_stop[2]
        else:
           current_stopid = "" 
        if laststop != current_stopid:
            if(current_stopid == ""):
                traci.vehicle.setRouteID(bus_id, route_id)
                traci.vehicle.setBusStop(bus_id, stop_id,duration=240)

    step += 1
    # time.sleep(0.1)

