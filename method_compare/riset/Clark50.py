import xml.etree.ElementTree as ET
from xml.dom import minidom
# from ElementTree_pretty import prettify

tree = ET.parse('DataConvert.xml')
root = tree.getroot()
data = []
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
		for k in range(len(item_rute)-1):
			crute_id = "veh"+str(j)+"_"+str(k)
			depart = "25"
			crute_from = data[item_rute[k]]
			crute_to = data[item_rute[k+1]]
			current_group = ET.SubElement(root, 'trip', {'id':crute_id,'depart':depart,
				'from':crute_from,'to':crute_to })
	xmlstr = minidom.parseString(ET.tostring(root)).toprettyxml(indent="   ")
	with open("TripsData-Clark.xml", "a") as f:
		f.write(xmlstr)


