# import xml.etree.ElementTree as ET
# from xml.dom import minidom

# our_route = ET.parse('our-route.xml')
# random_route = ET.parse('bsd.rou.xml')
# root_our_route = our_route.getroot()
# root_random_route = random_route.getroot()
# for child in root_our_route:
#     atr_child = child.attrib
#     current_group = ET.SubElement(root_random_route, 'routes', {'id':atr_child['id'],'edges':atr_child['edges']})

# xmlst = minidom.parseString(ET.tostring(root_random_route)).toprettyxml(indent="   ")
# with open("TripsData-Clark.xml", "w") as f:
#     f.write(xmlst)

# os.system("some_command < input_file | another_command > output_file") 

import os
cmd = "python D:/PASCA/Thesis-kerja/sumo/tools/randomTrips.py -n BSD.net.xml -r bsd2.rou.xml -e 500 -l"
returned_value = os.system(cmd)  # returns the exit code in unix

import xml.etree.ElementTree as ET
from xml.dom import minidom

our_route = ET.parse('our-route.xml')
random_route = ET.parse('bsd2.rou.xml')
root_our_route = our_route.getroot()
root_random_route = random_route.getroot()
for child in root_our_route:
    atr_child = child.attrib
    # current_group = ET.SubElement(root_random_route, 'route', {'id':atr_child['id'],'edges':atr_child['edges']})
    current_group = ET.Element('route', {'id':atr_child['id'],'edges':atr_child['edges']})
    root_random_route.insert(0,current_group)


xmlst = minidom.parseString(ET.tostring(root_random_route)).toprettyxml(indent="   ")
with open("bsd2.rou.xml", "w") as f:
    f.write(xmlst)
