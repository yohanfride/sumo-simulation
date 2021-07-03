import xml.etree.ElementTree as ET
from xml.dom import minidom
# from ElementTree_pretty import prettify

tree = ET.parse('DataConvert.xml')
root = tree.getroot()
data = []
nama_file = ['MDP15','MDP25','MDP35','MDP50']
rute = []
rute0 = [
	[[0, 9], [9, 5], [5, 15], [15, 14], [14, 13], [13, 7], [7, 6], [6, 0]],
	[[0, 8], [8, 4], [4, 3], [3, 1], [1, 2], [2, 12], [12, 11], [11, 0]],
	[[0, 10], [10, 0]]
]
rute.append(rute0)
rute0 = [
	[[0, 5], [5, 15], [15, 14], [14, 13], [13, 7], [7, 25], [25, 6], [6, 12], [12, 0]],
	[[0, 17], [17, 16], [16, 4], [4, 8], [8, 18], [18, 19], [19, 0]],
	[[0, 3], [3, 20], [20, 1], [1, 2], [2, 24], [24, 9], [9, 0]],
	[[0, 10], [10, 23], [23, 22], [22, 21], [21, 11], [11, 0]]
]
rute.append(rute0)
rute1 = [
	[[0, 5], [5, 15], [15, 14], [14, 17], [17, 16], [16, 4], [4, 8], [8, 18], [18, 0]],
	[[0, 19], [19, 20], [20, 3], [3, 1], [1, 2], [2, 24], [24, 0]],
	[[0, 29], [29, 35], [35, 30], [30, 31], [31, 11], [11, 6], [6, 0]],
	[[0, 28], [28, 25], [25, 7], [7, 13], [13, 32], [32, 12], [12, 34], [34, 0]],
	[[0, 23], [23, 27], [27, 22], [22, 9], [9, 10], [10, 21], [21, 26], [26, 0]],
	[[0, 33], [33, 0]]
]
rute.append(rute1)
rute2 = [
	[[0, 33], [33, 41], [41, 25], [25, 28], [28, 5], [5, 0]],
	[[0, 42], [42, 36], [36, 35], [35, 47], [47, 29], [29, 43], [43, 44], [44, 0]],
	[[0, 49], [49, 16], [16, 17], [17, 4], [4, 39], [39, 15], [15, 0]],
	[[0, 37], [37, 38], [38, 40], [40, 14], [14, 32], [32, 7], [7, 13], [13, 0]],
	[[0, 18], [18, 19], [19, 20], [20, 8], [8, 3], [3, 1], [1, 2], [2, 0]],
	[[0, 46], [46, 45], [45, 30], [30, 31], [31, 11], [11, 0]],
	[[0, 9], [9, 24], [24, 34], [34, 12], [12, 6], [6, 0]],
	[[0, 23], [23, 27], [27, 22], [22, 10], [10, 21], [21, 26], [26, 50], [50, 0]],
	[[0, 48], [48, 0]]
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


