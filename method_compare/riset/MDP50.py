import xml.etree.ElementTree as ET
from xml.dom import minidom
# from ElementTree_pretty import prettify

tree = ET.parse('DataConvert.xml')
root = tree.getroot()
data = []
nama_file = ['MDP25','MDP35','MDP50']
rute = []
rute0 = [
	[[0, 15], [15, 7], [7, 5], [5, 13], [13, 6], [6, 22], [22, 12], [12, 0]],
	[[0, 1], [1, 3], [3, 17], [17, 4], [4, 8], [8, 2], [2, 24], [24, 0]],
	[[0, 9], [9, 19], [19, 20], [20, 23], [23, 21], [21, 11], [11, 0]],
	[[0, 10], [10, 16], [16, 18], [18, 14], [14, 25], [25, 0]]
]
rute.append(rute0)
rute1 = [
	[[0, 33], [33, 13], [13, 24], [24, 14], [14, 29], [29, 0]],
	[[0, 28], [28, 18], [18, 17], [17, 23], [23, 2], [2, 31], [31, 21], [21, 0]],
	[[0, 26], [26, 20], [20, 10], [10, 34], [34, 7], [7, 30], [30, 22], [22, 0]],
	[[0, 4], [4, 3], [3, 15], [15, 9], [9, 32], [32, 6], [6, 0]],
	[[0, 1], [1, 8], [8, 12], [12, 27], [27, 16], [16, 19], [19, 0]],
	[[0, 25], [25, 11], [11, 5], [5, 35], [35, 0]]
]
rute.append(rute1)
rute2 = [
	[[0, 24], [24, 23], [23, 29], [29, 46], [46, 42], [42, 26], [26, 0]] ,
	[[0, 7], [7, 25], [25, 3], [3, 17], [17, 28], [28, 20], [20, 27], [27, 0]],
	[[0, 43], [43, 34], [34, 13], [13, 39], [39, 12], [12, 31], [31, 0]],
	[[0, 48], [48, 41], [41, 21], [21, 38], [38, 19], [19, 0]],
	[[0, 44], [44, 36], [36, 4], [4, 32], [32, 10], [10, 22], [22, 0]],
	[[0, 30], [30, 50], [50, 14], [14, 2], [2, 6], [6, 0]],
	[[0, 11], [11, 9], [9, 45], [45, 33], [33, 35], [35, 0]],
	[[0, 40], [40, 49], [49, 37], [37, 8], [8, 18], [18, 1], [1, 0]],
	[[0, 15], [15, 5], [5, 47], [47, 16], [16, 0]]
]
rute.append(rute2)
for child in root:
	# print(child.tag, child.attrib)
	atr = child.attrib
	ids =  int(atr['id'].split("_")[1])
	lanes = atr['lane'].split("_")[0]
	# print(ids)
	data.append(lanes)

for i in range(3):
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


