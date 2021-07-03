import xml.etree.ElementTree as ET
from xml.dom import minidom

list_route = []
list_edges = []
routes = ET.parse('all-rute.xml')
root = routes.getroot()
for child in root:
	atr_child = child.attrib
	vehid = atr_child['id']
	list_route.append(vehid)
	for item_child in child:
		atr_item =  item_child.attrib
		edges_item = atr_item['edges']
		list_edges.append(edges_item)

roots = ET.Element('routes')
for i in range(len(list_route)):
	route_item = ET.SubElement(roots, 'route', {'id':list_route[i],'edges':list_edges[i]})

xmlstr = minidom.parseString(ET.tostring(roots)).toprettyxml(indent="   ")
with open('trips.xml', "w") as f:
	f.write(xmlstr)