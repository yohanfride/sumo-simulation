import numpy as np
import pandas as pd
import json
import random
import warnings
warnings.filterwarnings('ignore')

def saveQ(name,df):    
    out = df.to_dict('records')
    with open('node/'+name+'.json', 'w') as outfile:
        json.dump(out, outfile)

bus_id = ['veh0','veh1','veh2']
qdefault = 0
f = open('pelanggan4.json')
data = json.load(f)
adf = []
i = 0

for name in bus_id:
    DA = np.array([0])
    np.savetxt('DA/'+name+'.txt',DA)
    Q = [{
            "id":0,
            "path":[0],
            "Q":qdefault,
            "next":[],
            "lastval":0
        }]
    df = pd.DataFrame(Q)
    saveQ(name,df)
    for j in range(1, len(data)):
        data[j]['best_arrive'] = 0
    adf.append(df)
    i+=1

with open('pelanggan4.json', 'w') as outfile:
    json.dump(data, outfile)

percobaan = []
with open('DA/percobaan.json', 'w') as outfile:
    json.dump(percobaan, outfile)