from astar import astar_with_no_fly_penalty
from csp import is_valid_delivery
from math import sqrt

def euclidean(p1, p2):
    return sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def minutes_to_str(minutes):
    h = int(minutes) // 60
    m = int(minutes) % 60
    return f"{h:02d}:{m:02d}"

def plan_with_astar(drones, deliveries, no_fly_zones):
    assigned = set()
    assignments = {d["id"]: [] for d in drones}

    recharge_threshold = 0.3
    recharge_time = 30

    drone_states = {
        d["id"]: {
            "pos": tuple(d["start_pos"]),
            "battery": d["battery"],
            "left": d["battery"],
            "time": 570
        }
        for d in drones
    }

    progress = True
    while progress:
        progress = False
        for drone in drones:
            d_id = drone["id"]
            state = drone_states[d_id]
            best_delivery = None
            best_path = None
            best_cost = float("inf")

            for delivery in deliveries:
                if delivery["id"] in assigned:
                    continue

                if not is_valid_delivery(drone, delivery, state["time"]):
                    continue

                path = astar_with_no_fly_penalty(state["pos"], tuple(delivery["pos"]), no_fly_zones, max_steps=2000, current_time=state["time"])
                if not path:
                    continue

                dist = len(path)
                cost = dist * delivery["weight"]
                if cost < state["left"] and cost < best_cost:
                    best_cost = cost
                    best_path = path
                    best_delivery = delivery

            if best_delivery:
                assignments[d_id].append(best_delivery["id"])
                assigned.add(best_delivery["id"])
                state["left"] -= best_cost
                state["pos"] = tuple(best_delivery["pos"])
                state["time"] += len(best_path) / drone["speed"]
                if state["left"] < drone["battery"] * recharge_threshold:
                    state["time"] += recharge_time
                    state["left"] = drone["battery"]
                progress = True

    return assignments