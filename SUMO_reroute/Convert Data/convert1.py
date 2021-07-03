import xml.etree.ElementTree as ET
from xml.dom import minidom
# from ElementTree_pretty import prettify

tree = ET.parse('DataConvert.xml')
root = tree.getroot()
data = []
n = 16

for child in root:
	# print(child.tag, child.attrib)
	atr = child.attrib
	ids =  int(atr['id'].split("_")[1])
	lanes = atr['lane'].split("_")[0]
	# print(ids)
	data.append(lanes)

# for i in range(4):
# 	root = ET.Element('trips')
# 	root.set('title', nama_file[i])
# 	crute = rute[i]
# 	for j in range(len(crute)):
# 		item_rute = crute[j]
# 		for k in range(len(item_rute)-1):
# 			crute_id = "veh"+str(j)+"_"+str(k)
# 			depart = "25"
# 			crute_from = data[item_rute[k]]
# 			crute_to = data[item_rute[k+1]]
# 			current_group = ET.SubElement(root, 'trip', {'id':crute_id,'depart':depart,
# 				'from':crute_from,'to':crute_to })
# 	xmlstr = minidom.parseString(ET.tostring(root)).toprettyxml(indent="   ")
# 	with open("TripsData.xml", "a") as f:
# 		f.write(xmlstr)

for i in range(n):
	for j in range(n):
		if i != j:
			crute_id = "rute_"+str(i)+"_"+str(j)
			depart = "25"
			crute_from = data[i]
			crute_to = data[j]
			current_group = ET.SubElement(root, 'trip', {'id':crute_id,'depart':depart,
				'from':crute_from,'to':crute_to })
xmlstr = minidom.parseString(ET.tostring(root)).toprettyxml(indent="   ")
with open("TripsData.xml", "a") as f:
	f.write(xmlstr)