import xml.etree.ElementTree as ET
from xml.dom import minidom
# from ElementTree_pretty import prettify

duration = 40

rute = []
nama_file = ['Clark15','Clark25','Clark35','Clark50']
rute = []
rute0 = [
	[0, 9, 3, 8, 4, 5, 15, 14, 0],
	[0, 1, 12, 7, 13, 6, 11, 0],
	[0, 10, 2, 0] 
]
rute.append(rute0)
rute0 = [
	[0, 17, 4, 5, 15, 14, 16, 18, 0],
	[0, 9, 3, 8, 19, 20, 1, 0],
	[0, 23, 22, 25, 12, 7, 13, 6, 0],
	[0, 21, 10, 2, 24, 11, 0]
]
rute.append(rute0)
rute1 = [
	[0, 17, 4, 5, 15, 14, 16, 18, 0],
	[0, 12, 7, 28, 33, 25, 13, 0],
	[0, 9, 3, 8, 19, 20, 1, 0],
	[0, 2, 29, 35, 30, 31, 11, 0],
	[0, 24, 23, 32, 6, 27, 34, 0],
	[0, 21, 26, 10, 22, 0]
]
rute.append(rute1)
rute2 = [
	[0, 28, 50, 33, 41, 25, 0],
	[0, 29, 43, 44, 42, 36, 48, 0],
	[0, 16, 46, 47, 35, 45, 30, 0],
	[0, 18, 49, 17, 4, 19, 20, 0],
	[0, 3, 40, 37, 5, 39, 15, 14, 38, 0],
	[0, 12, 7, 13, 32, 6, 27, 34, 0],
	[0, 9, 8, 1, 2, 24, 0],
	[0, 26, 10, 31, 11, 23, 22, 0],
	[0, 21, 0] 
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
			if(rute[n][x][i] > 0):
				busStop =  ET.SubElement(vehicle, 'stop', {'busStop':"busStop_"+str(rute[n][x][i]),'duration':str(duration)})

		depot =  ET.SubElement(vehicle, 'stop', {'busStop':"depot",'duration':str(duration)})
		x+=1

	xmlstr = minidom.parseString(ET.tostring(roots)).toprettyxml(indent="   ")
	with open(nama_file[n]+'-trips.xml', "w") as f:
		f.write(xmlstr)