import xml.etree.ElementTree as ET
from xml.dom import minidom
# from ElementTree_pretty import prettify

nama_file = ['MDP25','MDP35','MDP50']
duration = 40

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

for n in range(3):
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