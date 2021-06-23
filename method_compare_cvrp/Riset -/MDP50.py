import xml.etree.ElementTree as ET
from xml.dom import minidom
# from ElementTree_pretty import prettify

tree = ET.parse('DataConvert.xml')
root = tree.getroot()
data = []
nama_file = ['MDP15','MDP25','MDP35','MDP50']
rute = []
rute0 = [
	[[0, 5], [5, 15], [15, 14], [14, 13], [13, 6], [6, 0]],
	[[0, 2], [2, 9], [9, 8], [8, 4], [4, 3], [3, 1], [1, 0]],
	[[0, 10], [10, 12], [12, 7], [7, 11], [11, 0]]
]
rute.append(rute0)
rute0 = [
	[[0, 20], [20, 4], [4, 8], [8, 3], [3, 1], [1, 0]],
	[[0, 17], [17, 16], [16, 18], [18, 19], [19, 14], [14, 0]],
	[[0, 15], [15, 5], [5, 9], [9, 24], [24, 21], [21, 0]],
	[[0, 12], [12, 7], [7, 13], [13, 25], [25, 6], [6, 11], [11, 0]],
	[[0, 2], [2, 23], [23, 22], [22, 10], [10, 0]]
]
rute.append(rute0)
rute1 = [
	[[0, 20], [20, 4], [4, 8], [8, 3], [3, 1], [1, 0]],
	[[0, 29], [29, 35], [35, 30], [30, 31], [31, 0]],
	[[0, 17], [17, 16], [16, 2], [2, 24], [24, 11], [11, 0]],
	[[0, 18], [18, 19], [19, 5], [5, 15], [15, 14], [14, 0]],
	[[0, 32], [32, 28], [28, 25], [25, 6], [6, 27], [27, 21], [21, 0]],
	[[0, 33], [33, 7], [7, 13], [13, 26], [26, 0]],
	[[0, 9], [9, 34], [34, 12], [12, 23], [23, 0]],
	[[0, 22], [22, 10], [10, 0]]
]
rute.append(rute1)
rute2 = [
	[[0, 42], [42, 45], [45, 31], [31, 0]],
	[[0, 44], [44, 47], [47, 29], [29, 48], [48, 0]],
	[[0, 36], [36, 35], [35, 17], [17, 0]],
	[[0, 38], [38, 37], [37, 39], [39, 14], [14, 0]],
	[[0, 49], [49, 16], [16, 20], [20, 0]],
	[[0, 5], [5, 15], [15, 3], [3, 8], [8, 24], [24, 0]],
	[[0, 4], [4, 40], [40, 18], [18, 1], [1, 11], [11, 0]],
	[[0, 43], [43, 46], [46, 21], [21, 0]],
	[[0, 41], [41, 33], [33, 25], [25, 0]],
	[[0, 32], [32, 28], [28, 6], [6, 27], [27, 0]],
	[[0, 50], [50, 7], [7, 13], [13, 26], [26, 2], [2, 0]],
	[[0, 9], [9, 19], [19, 30], [30, 0]],
	[[0, 12], [12, 34], [34, 22], [22, 23], [23, 10], [10, 0]]
]

rute.append(rute2)
for child in root:
	# print(child.tag, child.attrib)
	atr = child.attrib
	ids =  int(atr['id'].split("_")[1])
	lanes = atr['lane'].split("_")[0]
	# print(ids)
	data.append(lanes)

for i in range(4):
	root = ET.Element('trips')
	root.set('title', nama_file[i])
	crute = rute[i]
	for j in range(len(crute)):
		item_rute = crute[j]
		for k in range(len(item_rute)):
			crute_id = "veh"+str(j)+"_"+str(k)
			depart = "25"
			crute_from = data[item_rute[k][0]]
			crute_to = data[item_rute[k][1]]
			current_group = ET.SubElement(root, 'trip', {'id':crute_id,'depart':depart,
				'from':crute_from,'to':crute_to })
	xmlstr = minidom.parseString(ET.tostring(root)).toprettyxml(indent="   ")
	with open("TripsData-MDP.xml", "a") as f:
		f.write(xmlstr)


