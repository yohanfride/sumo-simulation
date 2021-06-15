import xml.etree.ElementTree as ET
from xml.dom import minidom
# from ElementTree_pretty import prettify

tree = ET.parse('DataConvert.xml')
root = tree.getroot()
data = []
nama_file = ['MIP15','MIP25','MIP35','MIP50']
rute = []
rute0 = [
	[[0, 9], [9, 3], [3, 8], [8, 4], [4, 1], [1, 2], [2, 0]],
	[[0, 10], [10, 0]],
	[[0, 12], [12, 5], [5, 15], [15, 14], [14, 7], [7, 13], [13, 6], [6, 11], [11, 0]]
]
rute.append(rute0)
rute0 = [
	[[0, 9], [9, 3], [3, 8], [8, 4], [4, 2], [2, 24], [24, 0]],
	[[0, 12], [12, 5], [5, 15], [15, 14], [14, 7], [7, 13], [13, 25], [25, 6], [6, 0]],
	[[0, 16], [16, 17], [17, 18], [18, 19], [19, 20], [20, 1], [1, 0]],
	[[0, 21], [21, 11], [11, 10], [10, 23], [23, 22], [22, 0]]
]
rute.append(rute0)
rute1 = [
	[[0, 6], [6, 12], [12, 7], [7, 13], [13, 5], [5, 15], [15, 14], [14, 32], [32, 0]],
	[[0, 9], [9, 3], [3, 8], [8, 18], [18, 19], [19, 20], [20, 4], [4, 0]],
	[[0, 10], [10, 23], [23, 27], [27, 34], [34, 0]],
	[[0, 21], [21, 16], [16, 17], [17, 1], [1, 2], [2, 24], [24, 0]],
	[[0, 26], [26, 28], [28, 33], [33, 25], [25, 22], [22, 0]],
	[[0, 29], [29, 35], [35, 30], [30, 31], [31, 11], [11, 0]]
]
rute.append(rute1)
rute2 = [
	[[0, 1], [1, 2], [2, 10], [10, 23], [23, 27], [27, 34], [34, 0]],
	[[0, 9], [9, 3], [3, 8], [8, 18], [18, 19], [19, 20], [20, 0]],
	[[0, 16], [16, 49], [49, 17], [17, 4], [4, 24], [24, 0]],
	[[0, 26], [26, 21], [21, 11], [11, 0]],
	[[0, 28], [28, 12], [12, 7], [7, 13], [13, 6], [6, 22], [22, 0]],
	[[0, 40], [40, 38], [38, 37], [37, 39], [39, 5], [5, 15], [15, 14], [14, 32], [32, 0]],
	[[0, 42], [42, 36], [36, 35], [35, 46], [46, 45], [45, 30], [30, 31], [31, 0]],
	[[0, 43], [43, 44], [44, 47], [47, 29], [29, 48], [48, 0]],
	[[0, 50], [50, 33], [33, 41], [41, 25], [25, 0]]
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
	with open("TripsData-MIP.xml", "a") as f:
		f.write(xmlstr)


