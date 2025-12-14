import xml.etree.ElementTree as ET
import random

NET_XML = "../map/NY/osm.net.xml"
OUT_ROUTES = "../map/NY/taxi.rou.xml"
NUM_TAXIS = 10
DEPART_TIME = 0

if __name__ == "__main__":
    tree = ET.parse(NET_XML)
    root = tree.getroot()

    drivable_edges = []

    for edge in root.findall("edge"):
        edge_id = edge.get("id")
        function = edge.get("function")

        if function == "internal":
            continue

        lanes = edge.findall("lane")
        if not lanes:
            continue

        usable = False
        for lane in lanes:
            disallow = lane.get("disallow", "")
            if "taxi" not in disallow and "passenger" not in disallow:
                usable = True
                break

        if usable:
            drivable_edges.append(edge_id)

    routes = ET.Element("routes")

    vtype = ET.SubElement(
        routes,
        "vType",
        id="taxi",
        vClass="taxi"
    )

    for i in range(NUM_TAXIS):
        edge = random.choice(drivable_edges)

        veh = ET.SubElement(
            routes,
            "vehicle",
            id=f"taxi_{i}",
            type="taxi",
            depart=str(DEPART_TIME),
            line="taxi",
            insertionCheck="all"
        )

        ET.SubElement(
            veh,
            "param",
            key="has.taxi.device",
            value="true"
        )

        ET.SubElement(
            veh,
            "route",
            edges=edge
        )

    tree_out = ET.ElementTree(routes)
    tree_out.write(OUT_ROUTES, encoding="utf-8", xml_declaration=True)