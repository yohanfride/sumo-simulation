import xml.etree.ElementTree as ET
from xml.dom import minidom
# from ElementTree_pretty import prettify

nama_file = ['MIP15','MIP25','MIP35','MIP50']
duration = 240

rute = []
rute0 = [
	[[0, 2], [2, 9], [9, 8], [8, 4], [4, 3], [3, 1], [1, 0]],
	[[0, 10], [10, 6], [6, 11], [11, 0]],
	[[0, 12], [12, 7], [7, 13], [13, 5], [5, 15], [15, 14], [14, 0]]
]
rute.append(rute0)
rute0 = [
	[[0, 2], [2, 24], [24, 11], [11, 0]],
	[[0, 9], [9, 3], [3, 8], [8, 16], [16, 17], [17, 0]],
	[[0, 10], [10, 23], [23, 22], [22, 25], [25, 6], [6, 0]],
	[[0, 12], [12, 7], [7, 13], [13, 5], [5, 15], [15, 14], [14, 0]],
	[[0, 18], [18, 19], [19, 20], [20, 4], [4, 1], [1, 21], [21, 0]]
]
rute.append(rute0)
rute1 = [
	[[0, 6], [6, 22], [22, 11], [11, 0]],
	[[0, 7], [7, 5], [5, 15], [15, 14], [14, 13], [13, 26], [26, 0]],
	[[0, 9], [9, 1], [1, 2], [2, 24], [24, 0]],
	[[0, 10], [10, 23], [23, 27], [27, 34], [34, 21], [21, 0]],
	[[0, 12], [12, 32], [32, 28], [28, 33], [33, 25], [25, 0]],
	[[0, 18], [18, 19], [19, 20], [20, 4], [4, 8], [8, 0]],
	[[0, 29], [29, 30], [30, 31], [31, 0]],
	[[0, 35], [35, 16], [16, 17], [17, 3], [3, 0]]
]
rute.append(rute1)
rute2 = [
	[[0, 10], [10, 1], [1, 9], [9, 8], [8, 20], [20, 0]],
	[[0, 11], [11, 2], [2, 24], [24, 0]],
	[[0, 12], [12, 7], [7, 13], [13, 32], [32, 6], [6, 26], [26, 21], [21, 0]],
	[[0, 18], [18, 19], [19, 4], [4, 5], [5, 15], [15, 14], [14, 0]],
	[[0, 28], [28, 50], [50, 33], [33, 41], [41, 25], [25, 0]],
	[[0, 29], [29, 43], [43, 48], [48, 0]],
	[[0, 34], [34, 23], [23, 27], [27, 22], [22, 0]],
	[[0, 35], [35, 46], [46, 30], [30, 31], [31, 0]],
	[[0, 36], [36, 42], [42, 45], [45, 0]],
	[[0, 40], [40, 39], [39, 37], [37, 38], [38, 0]],
	[[0, 44], [44, 47], [47, 0]],
	[[0, 49], [49, 16], [16, 17], [17, 3], [3, 0]]
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