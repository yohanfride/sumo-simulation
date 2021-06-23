import xml.etree.ElementTree as ET
from xml.dom import minidom
# from ElementTree_pretty import prettify

duration = 240

rute = []
nama_file = ['Clark15','Clark25','Clark35','Clark50']
rute = []
rute0 = [
	[0, 5, 15, 14, 13, 6, 0],
	[0, 2, 9, 8, 4, 3, 1, 0],
	[0, 10, 7, 12, 11, 0] 
]
rute.append(rute0)
rute0 = [
	[0, 20, 4, 8, 3, 1, 0],
	[0, 17, 16, 18, 19, 14, 0],
	[0, 15, 5, 9, 24, 21, 0],
	[0, 25, 6, 7, 13, 11, 0],
	[0, 2, 23, 12, 0],
	[0, 22, 10, 0]
]
rute.append(rute0)
rute1 = [
	[0, 20, 4, 8, 3, 1, 0],
	[0, 29, 35, 30, 31, 0],
	[0, 17, 16, 18, 19, 14, 0],
	[0, 15, 5, 9, 24, 21, 0],
	[0, 32, 28, 25, 6, 27, 0],
	[0, 33, 7, 13, 11, 0],
	[0, 12, 34, 22, 23, 0],
	[0, 2, 10, 26, 0] 
]
rute.append(rute1)
rute2 = [
	[0, 42, 45, 31, 0],
	[0, 44, 47, 29, 48, 0],
	[0, 36, 35, 17, 0],
	[0, 38, 37, 39, 14, 0],
	[0, 49, 16, 20, 0],
	[0, 5, 15, 3, 8, 24, 0],
	[0, 4, 40, 18, 1, 11, 0],
	[0, 43, 46, 21, 0],
	[0, 41, 33, 25, 0],
	[0, 32, 28, 6, 27, 0],
	[0, 50, 7, 13, 26, 0],
	[0, 9, 19, 2, 23, 0],
	[0, 12, 34, 22, 0],
	[0, 30, 10, 0]
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