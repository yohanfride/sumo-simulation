import xml.etree.ElementTree as ET
from xml.dom import minidom
# from ElementTree_pretty import prettify

tree = ET.parse('DataConvert.xml')
root = tree.getroot()
data = []
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


