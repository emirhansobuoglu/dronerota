import json
from csp import is_valid_delivery
from astar import astar_with_no_fly_penalty
from math import sqrt

# Mesafe hesaplama
def euclidean(p1, p2):
    return sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

# En uygun teslimatı seç
def assign_best_delivery(drone, deliveries, no_fly_zones, assigned_ids):
    start_pos = tuple(drone["start_pos"])
    best_score = float("inf")
    best_delivery = None

    for delivery in deliveries:
        if delivery["id"] in assigned_ids:
            continue  # daha önce atanmış

        if not is_valid_delivery(drone, delivery):
            continue  # CSP'den geçmedi

        goal_pos = tuple(delivery["pos"])
        path = astar_with_no_fly_penalty(start_pos, goal_pos, no_fly_zones=no_fly_zones)

        if not path:
            continue  # rota yoksa geç

        dist = len(path)
        priority = delivery["priority"]
        score = dist - (priority * 10)  # önceliği yüksek olan ödüllendirilir

        if score < best_score:
            best_score = score
            best_delivery = delivery

    return best_delivery

# Tüm drone'lara teslimat ataması yap
def assign_deliveries(drones, deliveries, no_fly_zones):
    assignments = {}
    assigned_ids = set()

    for drone in drones:
        best = assign_best_delivery(drone, deliveries, no_fly_zones, assigned_ids)
        if best:
            assignments[drone["id"]] = best["id"]
            assigned_ids.add(best["id"])
        else:
            assignments[drone["id"]] = None  # atanamadı

    return assignments
