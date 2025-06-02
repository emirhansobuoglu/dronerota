import math
from heapq import heappush, heappop
from shapely.geometry import Polygon, Point

# İki nokta arası Öklid mesafesi
def euclidean(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

# No-fly zone'ları Polygon nesnelerine çevir (aktif zaman bilgisiyle birlikte)
def build_no_fly_polygons(no_fly_zones):
    return [(Polygon(zone["coordinates"]), zone.get("active_time")) for zone in no_fly_zones]

# "HH:MM" formatındaki saat bilgisini dakikaya çevir
def time_str_to_minutes(tstr):
    try:
        h, m = map(int, tstr.split(":"))
        return h * 60 + m
    except:
        return None

# Belirli bir zaman belirli bir zaman aralığında mı kontrolü
def is_time_in_interval(time_min, start_str, end_str):
    start = time_str_to_minutes(start_str)
    end = time_str_to_minutes(end_str)
    if start is None or end is None:
        return False
    return start <= time_min <= end

# A* algoritması – No-fly zone çarpışmaları için ceza bazlı yol planlama
def astar_with_no_fly_penalty(start, goal, no_fly_zones=[], weight=1.0, penalty=50.0, max_steps=5000, current_time="09:30"):
    no_fly_polygons = build_no_fly_polygons(no_fly_zones)

    # current_time'ı dakikaya çevir
    if isinstance(current_time, str) and ":" in current_time:
        current_minutes = time_str_to_minutes(current_time)
    else:
        current_minutes = int(current_time)

    open_set = []
    heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    steps = 0

    while open_set:
        steps += 1
        if steps > max_steps:
            return None  # maksimum adımı geçtiyse rotayı sonlandır

        _, current = heappop(open_set)
        if current == goal:
            # Rotayı geriye sararak oluştur
            path = [current]
            while current in came_from:
                current = came_from[current]
                path.append(current)
            path.reverse()
            return path

        # 8 yönlü hareket (üst-alt-sol-sağ ve çaprazlar)
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue

                neighbor = (current[0] + dx, current[1] + dy)

                # Koordinatlar harita dışında mı?
                if not (0 <= neighbor[0] <= 100 and 0 <= neighbor[1] <= 100):
                    continue

                point = Point(neighbor)
                is_in_zone = False

                for poly, active_time in no_fly_polygons:
                    if poly.contains(point):
                        if active_time:
                            if is_time_in_interval(current_minutes, active_time[0], active_time[1]):
                                is_in_zone = True
                                break
                        else:
                            is_in_zone = True
                            break

                penalty_cost = penalty if is_in_zone else 0

                tentative_g = g_score[current] + euclidean(current, neighbor) * weight + penalty_cost

                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score = tentative_g + euclidean(neighbor, goal)
                    heappush(open_set, (f_score, neighbor))

    return None  # rota bulunamadı
