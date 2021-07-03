import os, sys
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:   
    sys.exit("please declare environment variable 'SUMO_HOME'")

sumoBinary = "C:/Program Files (x86)/Eclipse/Sumo/bin/sumo-gui"
sumoConfig = ["-c", "map-bsd1.sumocfg", "-S"]
sumoCmd = [sumoBinary, sumoConfig[0], sumoConfig[1], sumoConfig[2]]

Traning = 50
hacklearn = [10,5]


import traci
import traci.constants as tc
import sumolib
import time
import json
import xml.etree.ElementTree as ET
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



bus_id = ['veh0','veh1','veh2']
miu = 0.05
diskon = 0.9
epsilon = 0.1
qdefault = 0
f =  open('DA/best-path.json')
best_path = json.load(f)
f =  open('DA/percobaan.json')
experiment = json.load(f)

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

def loadQ(name):
    f = open('node/'+name+'.json')
    data = json.load(f)
    df = pd.DataFrame(data)
    return df

def saveQ(name,df):    
    out = df.to_dict('records')
    with open('node/'+name+'.json', 'w') as outfile:
        json.dump(out, outfile)

def updateQ(qtable, currentNode, nextId, reward):
    i = currentNode['id']
    MaxQ = maxq(qtable,nextId)
    newQ = currentNode['Q'] + ( miu * ( reward + ( diskon * MaxQ ) - currentNode['Q'] ) )
    return newQ
    
def addNewNode(qtable,path,i,rw):
    id = len(qtable)
    if rw == 0:
        rw = qdefault
    qrow = {
        "id":id,
        "path":path.copy(),
        "Q":rw,
        "next":[],
        "lastval":i
    }
    qtable = qtable.append(qrow, ignore_index=True)
    return qtable,id

def getNodeId(qtable,currentNode,value):
    nextNode = currentNode['next']
    for i in nextNode :
        if(qtable.loc[i,'lastval'] == value):
            return i
    return -1

def updateNode(qtable, currentNode):
    indexNode = currentNode['id']
    qtable.loc[indexNode] = list(currentNode.values())
#     saveQ(qtable)
    return qtable
    
def getItem(df,index):
    return df.iloc[[index]].to_dict('records')[0]

#Fungsi MDP

def bestq(qtable, node, currentNode, s_time):
    nextNode = currentNode['next']
    if len(nextNode) == 0:
        return saving(distance,duration,node,currentNode['lastval'],s_time)
    nextNodeQ = qtable.loc[nextNode]
    maxQ = nextNodeQ['Q'].max()
    result = nextNodeQ[nextNodeQ['Q'] == nextNodeQ['Q'].max()]
    if(len(result) == 1):        
        return getItem(result,0)['lastval']
    else:
        return saving(distance,duration,node,currentNode['lastval'],s_time)

def maxq(qtable, nextId):
    nextNode = getItem(qtable,nextId)['next']
    if len(nextNode) == 0:
        return 0
    nextNodeQ = qtable.loc[nextNode]
    maxQ = nextNodeQ['Q'].max()
    return maxQ

def randomq(node,s_time,i):
    for i in range(10):
        result = random.randint(0,len(node)-1)
        if(serviceTimeChek(s_time,i,result)):
            break
    return node[result]

def randomNode(qtable, node, currentNode, s_time):
    nextNode = currentNode['next']
    if len(nextNode) == 0:
        return randomq(node,s_time,currentNode['lastval'])
    nextNodeQ = qtable.loc[nextNode]
    rnd = random.randint(0,len(nextNodeQ)-1)
    val = getItem(nextNodeQ,rnd)['lastval']    
    if len(nextNode) == 1 and val == 0:
        return saving(distance,duration,node,currentNode['lastval'],s_time)
    else:
        while val < 1:
            rnd = random.randint(0,len(nextNodeQ)-1)
            val = getItem(nextNodeQ,rnd)['lastval'] 
    return val

def getReward(name, total):
    DA = np.loadtxt('DA/'+name+'.txt')
    if DA == 0:
        DA = total
    if(DA>=total):
        r = 1
        DA = total
    else:
        r = 0
    np.savetxt('DA/'+name+'.txt', np.array([DA]))
    return r

def countDistance(path):
    total = 0
    for path_item in path:
        for i in range(1,len(path_item)):
            x = int(path_item[i-1])
            y = int(path_item[i])
            total+=distance[x][y]
    return total

def start_action(qtable, currentNode, nodes, routes, path, nextCustomer):
    ## Chek node Tujuan
    routes.append([currentNode['lastval'],nextCustomer])
    path.append(str(nextCustomer))
    nextId = getNodeId(qtable,currentNode,nextCustomer)
    if(nextId == -1):
        qtable,nextId = addNewNode(qtable,path,nextCustomer,0)
        currentNode['next'].append(nextId)

    if(nextCustomer > 0):
        getindex = np.where(nodes == nextCustomer)[0]
        nodes = np.delete(nodes, [getindex])  

    nextNode = getItem(qtable,nextId)

    return qtable, nextNode, nodes, routes, path

def result_action(qtable, currentNode, nextNode, capacity, s_time, reward):
    nextCustomer = nextNode['lastval']
    nextId = nextNode['id']
    if(nextCustomer > 0):
        capacity -= demand[nextCustomer]
        if(data[nextCustomer]['best_arrive'] == 0 ):
            data[nextCustomer]['best_arrive'] = s_time
        else:
            if(s_time >= data[nextCustomer]['ready_time'] and s_time <= data[nextCustomer]['due_time']):
                if(s_time <= data[nextCustomer]['best_arrive'] ):
                    data[nextCustomer]['best_arrive'] = s_time
                    reward = 0.1
            else:
                if(s_time > data[nextCustomer]['best_arrive'] ):
                    data[nextCustomer]['best_arrive'] = s_time
    else:
        capacity = vehicle_capacity

    Qval = updateQ(qtable,currentNode,nextId, reward)
    ## Update Nodes
    currentNode['Q'] = Qval
    qtable = updateNode(qtable,currentNode)
    currentNode = nextNode
    return qtable,currentNode,capacity

def training_move(qtable, currentNode, nodes, routes, path, capacity, s_time):
    if len(nodes) > 1 :
        greed = random.random()
        if greed < epsilon :
            j = randomq(nodes,s_time,i)
        else:
            j = saving(distance,duration,nodes,i,s_time)

        if (capacity - demand[j] < 0) :
            j = 0
    else :
        j = nodes[0]


    qtable, nextNode, nodes, routes, path = start_action(qtable, currentNode, nodes, routes, path, j)
    return qtable, currentNode, nodes, routes, path, nextNode

def testing_move(qtable, currentNode, nodes, routes, path, capacity, s_time):
    if len(nodes) > 1 :
        greed = random.random()
        if greed < epsilon :
            j = randomNode(qtable, nodes, currentNode, s_time)
        else:
            j = bestq(qtable, nodes, currentNode, s_time)
        
        if (capacity - demand[j] < 0) :
            j = 0
    else :
        j = nodes[0]

    qtable, nextNode, nodes, routes, path = start_action(qtable, currentNode, nodes, routes, path, j)
    return qtable, currentNode, nodes, routes, path, nextNode

def hack_move(qtable, currentNode, nodes, routes, path, capacity, s_time, bestpath, hack_time):
    i = currentNode['lastval']
    j = int(bestpath[hack_time])    
    qtable, nextNode, nodes, routes, path = start_action(qtable, currentNode, nodes, routes, path, j)
    hack_time+=1
    return qtable, currentNode, nodes, routes, path, nextNode,hack_time

#### Jadi Update Reward diadakan ketika menghitung semua jarak, lalu akhirnya mengupdate nilai node terakhir.
def updateRewardLastNode(qtable, currentNode, reward):
    currentNode['Q'] = reward
    qtable = updateNode(qtable,currentNode)
    return qtable

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
#End Fungsi MDP


MaxEpisode = 25
for episode in range(MaxEpisode):
    now = datetime.datetime.now()
    exp_time = now.strftime("%Y-%m-%d %H%M%S")

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
    hacktime = [1 for i in range(len(bus_id))]
    nodes = node[1:]
    nodes = np.array(nodes)
    pos = len(experiment)

    if pos % ( hacklearn[0]+hacklearn[1] ) > hacklearn[0] :
        status = "hack"
    elif Traning > pos :
        status = "training"
    else:
        status = "testing"

    print(status)
    if pos == 0 or pos > Traning :
        generateRandomVehicle()
    
    print("Starting the TraCI server...")
    traci.start(sumoCmd, label="sim"+str(episode)) 

    print("Subscribing to vehicle data...")
    print(nodes)


    Q = []
    currentNode = []
    routes = []
    path = []
    nextNode = []
    capacity = []

    

    ### First Route
    for i in range(len(bus_id)):
        qtable =  loadQ(bus_id[i])
        
        x = last_node[i]
        cNode = getItem(qtable,x)
        rt = []
        pth = ["0"]
        if status == "training":
            qtable, cNode, nodes, rt, pth, ntNode = training_move(qtable, cNode, nodes, rt, pth, vehicle_capacity, 0) 
        elif status == "hack":
            qtable, cNode, nodes, rt, pth, ntNode,hacktime[i] = hack_move(qtable, cNode, nodes, rt, pth, vehicle_capacity, 0, best_path[i], 1) 
        else :
            qtable, cNode, nodes, rt, pth, ntNode = testing_move(qtable, cNode, nodes, rt, pth, vehicle_capacity, 0) 

        y = ntNode['lastval']
        
        bstop = "busStop_"+str(y)
        srute = "rute_"+str(x)+"_"+str(y)
        
        traci.vehicle.add(bus_id[i], srute, depart="1.0")
        traci.vehicle.setColor(bus_id[i],(255,0,0))
        traci.vehicle.setBusStop(bus_id[i], bstop, duration=240)
        laststop[i] = bstop
        print(bus_id[i]+" --> "+srute+" --> "+bstop)
        lastrute[i] = srute
        Q.append(qtable)
        routes.append(rt)
        path.append(pth)
        nextNode.append(ntNode)
        capacity.append(vehicle_capacity)
        currentNode.append(cNode)


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

                        #### fungsi result action ####
                        Q[i], currentNode[i], capacity[i] = result_action(Q[i],  currentNode[i], nextNode[i], capacity[i], step - 240, 0)


                    if(len(nodes)>0):
                        ### fungsi move untuk strart action ####
                        if status == "training":
                            Q[i], currentNode[i], nodes, routes[i], path[i], nextNode[i] = training_move(Q[i],  currentNode[i], nodes, routes[i], path[i], capacity[i], step) 
                        elif status == "hack":
                            Q[i], currentNode[i], nodes, routes[i], path[i], nextNode[i], hacktime[i] = hack_move(Q[i],  currentNode[i], nodes, routes[i], path[i], capacity[i], step, best_path[i], hacktime[i]) 
                        else :
                            Q[i], currentNode[i], nodes, routes[i], path[i], nextNode[i] = testing_move(Q[i],  currentNode[i], nodes, routes[i], path[i], capacity[i], step) 

                        x = currentNode[i]['lastval']
                        y = nextNode[i]['lastval']
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
                    elif (currentNode[i]['lastval'] > 0 ) :
                        Q[i], nextNode[i], nodes, routes[i], path[i] = start_action(Q[i],  currentNode[i], nodes, routes[i], path[i], 0)
                        x = currentNode[i]['lastval']
                        y = nextNode[i]['lastval']
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

        step += 1   

    # traci.close()
    ##Ini Fungsi untuk menyimpan nilai Q,  Hitung Reward dan  Update Last Distance

    print(path)
    totalDistance = countDistance(path)
    reward = getReward(bus_id[0],totalDistance)
    experiment.append(totalDistance)

    if reward == 1 :
        best_path = path

    for i in range(len(bus_id)):
        qtable = updateRewardLastNode(Q[i],currentNode[i],reward)
        saveQ(bus_id[i],qtable)

    ###End Fungsi

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

    with open('hasil/waktu-'+str(pos+1)+' '+exp_time+'.json', 'w') as outfile:
        json.dump(vehicle, outfile)

    with open('DA/best-path.json', 'w') as outfile:
        json.dump(best_path, outfile)

    with open('DA/percobaan.json', 'w') as outfile:
        json.dump(experiment, outfile)

    with open('pelanggan4.json', 'w') as outfile:
        json.dump(data, outfile)