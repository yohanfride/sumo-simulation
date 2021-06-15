import xml.etree.ElementTree as ET
from xml.dom import minidom
# from ElementTree_pretty import prettify

tree = ET.parse('DataConvert.xml')
root = tree.getroot()
data = []
nama_file = ['Clark25','Clark35','Clark50']
rute = []
rute0 = [
	[[0, 9], [9, 3], [3, 8], [8, 4], [4, 2], [2, 24], [24, 0]],
	[[0, 12], [12, 5], [5, 15], [15, 14], [14, 7], [7, 13], [13, 25], [25, 6], [6, 0]],
	[[0, 16], [16, 17], [17, 18], [18, 19], [19, 20], [20, 1], [1, 0]],
	[[0, 21], [21, 11], [11, 10], [10, 23], [23, 22], [22, 0]]
]
rute.append(rute0)
rute1 = [
	[[0, 9], [9, 3], [3, 8], [8, 1], [1, 2], [2, 24], [24, 0]],
	[[0, 10], [10, 23], [23, 12], [12, 7], [7, 13], [13, 25], [25, 0]],
	[[0, 18], [18, 19], [19, 20], [20, 4], [4, 5], [5, 15], [15, 14], [14, 0]],
	[[0, 28], [28, 27], [27, 29], [29, 30], [30, 31], [31, 32], [32, 0]],
	[[0, 33], [33, 26], [26, 6], [6, 22], [22, 21], [21, 0]],
	[[0, 34], [34, 35], [35, 16], [16, 17], [17, 11], [11, 0]]
]
rute.append(rute1)
rute2 = [
	[[0, 1], [1, 2], [2, 24], [24, 9], [9, 3], [3, 8], [8, 0]],
	[[0, 10], [10, 23], [23, 6], [6, 22], [22, 0]],
	[[0, 16], [16, 17], [17, 18], [18, 19], [19, 20], [20, 4], [4, 40], [40, 0]],
	[[0, 21], [21, 11], [11, 50], [50, 25], [25, 26], [26, 0]],
	[[0, 31], [31, 32], [32, 42], [42, 41], [41, 30], [30, 0]],
	[[0, 34], [34, 48], [48, 43], [43, 44], [44, 36], [36, 47], [47, 0]],
	[[0, 35], [35, 46], [46, 45], [45, 12], [12, 7], [7, 13], [13, 0]],
	[[0, 38], [38, 37], [37, 39], [39, 5], [5, 15], [15, 14], [14, 0]],
	[[0, 49], [49, 33], [33, 27], [27, 29], [29, 28], [28, 0]]
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
	with open("TripsData-MIP.xml", "a") as f:
		f.write(xmlstr)


