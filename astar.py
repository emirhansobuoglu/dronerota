import math
from heapq import heappush, heappop
from shapely.geometry import Polygon, Point

# Mesafe fonksiyonu
def euclidean(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

# No-fly zone polygon oluşturucu
def build_no_fly_polygons(no_fly_zones):
    return [Polygon(zone["coordinates"]) for zone in no_fly_zones]

# A* algoritması (no-fly cezalı)
def astar_with_no_fly_penalty(start, goal, no_fly_zones=[], weight=1.0, penalty=50.0, max_steps=5000):
    no_fly_polygons = build_no_fly_polygons(no_fly_zones)

    open_set = []
    heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    steps = 0
    while open_set:
        steps += 1
        if steps > max_steps:
            return None
        _, current = heappop(open_set)
        if current == goal:
            path = [current]
            while current in came_from:
                current = came_from[current]
                path.append(current)
            path.reverse()
            return path

        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                neighbor = (current[0] + dx, current[1] + dy)

                if not (0 <= neighbor[0] <= 100 and 0 <= neighbor[1] <= 100):
                    continue

                point = Point(neighbor)
                penalty_cost = penalty if any(poly.contains(point) for poly in no_fly_polygons) else 0

                tentative_g = g_score[current] + euclidean(current, neighbor) * weight + penalty_cost
                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score = tentative_g + euclidean(neighbor, goal)
                    heappush(open_set, (f_score, neighbor))

    return None  # rota bulunamadı
