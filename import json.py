import json
import math

def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)


with open("data.json", "r") as file:
    data = json.load(file)

warehouses = data["warehouses"]
agents = data["agents"]
packages = data["packages"]

report = {}
for agent in agents:
    report[agent] = {
        "packages_delivered": 0,
        "total_distance": 0.0
    }


for pkg in packages:
    warehouse_id = pkg["warehouse"]
    warehouse_loc = warehouses[warehouse_id]

    # Find nearest agent
    nearest_agent = None
    min_dist = float("inf")

    for agent, agent_loc in agents.items():
        d = distance(agent_loc, warehouse_loc)
        if d < min_dist:
            min_dist = d
            nearest_agent = agent

    # Distance: agent → warehouse → destination
    dist_to_warehouse = distance(agents[nearest_agent], warehouse_loc)
    dist_to_destination = distance(warehouse_loc, pkg["destination"])

    total_trip_distance = dist_to_warehouse + dist_to_destination

    # Update report
    report[nearest_agent]["packages_delivered"] += 1
    report[nearest_agent]["total_distance"] += total_trip_distance


best_agent = None
best_efficiency = float("inf")

for agent in report:
    delivered = report[agent]["packages_delivered"]
    total_dist = report[agent]["total_distance"]

    efficiency = total_dist / delivered if delivered > 0 else 0
    report[agent]["total_distance"] = round(total_dist, 2)
    report[agent]["efficiency"] = round(efficiency, 2)

    if efficiency < best_efficiency:
        best_efficiency = efficiency
        best_agent = agent

report["best_agent"] = best_agent


with open("report.json", "w") as file:
    json.dump(report, file, indent=4)

print("Delivery simulation completed successfully!")
