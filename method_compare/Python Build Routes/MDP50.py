import xml.etree.ElementTree as ET
from xml.dom import minidom
# from ElementTree_pretty import prettify

nama_file = ['MDP15','MDP25','MDP35','MDP50']
duration = 40

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

for n in range(4):
	routes = ET.parse(nama_file[n]+'-rute.xml')
	root = routes.getroot()
	edges = ''
	list_edges = []
	list_veh = []
	last_veh = 'veh0'
	for child in root:
		atr_child = child.attrib
		vehid = atr_child['id']
		vehname = vehid.split("_")[0]
		if last_veh != vehname :
			edges +=" "+last_item
			list_edges.append(edges)
			list_veh.append(last_veh)
			last_veh = vehname
			edges = ""

		for item_child in child:
			atr_item =  item_child.attrib
			edges_item = atr_item['edges']
			edges_item_array = edges_item.split()
			last_item = edges_item_array[len(edges_item_array) - 1]
			del edges_item_array[len(edges_item_array) - 1]
			edges_item =' '.join(edges_item_array)
			edges += " "+edges_item

	edges +=" "+last_item
	list_edges.append(edges)
	list_veh.append(last_veh)

	roots = ET.Element('routes')
	x=0
	for veh in list_veh:
		vehicle =  ET.SubElement(roots, 'vehicle', {'id':veh,'depart':"1.0",'color':"1,0,0"})
		route =  ET.SubElement(vehicle, 'route', {'edges':list_edges[x]})
		for i in range(1,len(rute[n][x])):
			if(rute[n][x][i][0] > 0):
				busStop =  ET.SubElement(vehicle, 'stop', {'busStop':"busStop_"+str(rute[n][x][i][0]),'duration':str(duration)})

		depot =  ET.SubElement(vehicle, 'stop', {'busStop':"depot",'duration':str(duration)})
		x+=1

	xmlstr = minidom.parseString(ET.tostring(roots)).toprettyxml(indent="   ")
	with open(nama_file[n]+'-trips.xml', "w") as f:
		f.write(xmlstr)