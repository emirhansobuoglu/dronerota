import random
from math import sqrt
from datetime import datetime
from csp import is_valid_delivery
from astar import astar_with_no_fly_penalty

def euclidean(p1, p2):
    return sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def minutes_to_str(minutes):
    h = int(minutes) // 60
    m = int(minutes) % 60
    return f"{h:02d}:{m:02d}"

def calculate_fitness(assignments, drones, deliveries, no_fly_zones):
    completed = 0
    total_energy = 0
    penalty_count = 0
    overused_battery_count = 0
    csp_rejected = 0

    path_cache = {}
    assigned_global = set()
    print("📊 [Fitness] Hesaplama başlatıldı...")

    recharge_threshold = 0.3
    recharge_time = 30

    for d_id, delivery_ids in assignments.items():
        drone = next(d for d in drones if d["id"] == d_id)
        start = tuple(drone["start_pos"])
        battery_limit = drone["battery"]
        drone_energy_used = 0
        current_time_min = 570

        print(f"🚁 Drone {d_id} → Teslimatlar: {delivery_ids}")

        for delivery_id in delivery_ids:
            if delivery_id in assigned_global:
                print(f"⚠ [Çift Teslimat] Teslimat {delivery_id} başka drone tarafından atanmış.")
                continue

            delivery = next(d for d in deliveries if d["id"] == delivery_id)
            current_time_str = minutes_to_str(current_time_min)

            if not is_valid_delivery(drone, delivery, current_time_min):
                print(f"⚠ [CSP Red] Drone {d_id} → Teslimat {delivery_id} | Saat: {current_time_str}")
                csp_rejected += 1
                continue

            goal = tuple(delivery["pos"])
            cache_key = (d_id, delivery_id)

            if cache_key in path_cache:
                path = path_cache[cache_key]
            else:
                path = astar_with_no_fly_penalty(start, goal, no_fly_zones, max_steps=2000, current_time=current_time_str)
                path_cache[cache_key] = path

            if path:
                path_len = len(path)
                energy = (path_len * delivery["weight"]) * (drone["speed"] / 10)
                drone_energy_used += energy
                total_energy += energy
                completed += 1
                assigned_global.add(delivery_id)
                start = goal

                travel_time = path_len / drone["speed"]
                current_time_min += travel_time

                remaining_battery = battery_limit - drone_energy_used
                if remaining_battery < battery_limit * recharge_threshold:
                    current_time_min += recharge_time
                    print(f"🔌 [Şarj] Drone {d_id} → Şarj süresi eklendi ({recharge_time} dk) | Kalan Batarya: {remaining_battery:.2f}")
            else:
                penalty_count += 1
                print(f"❌ [Rota Yok] Drone {d_id} → Teslimat {delivery_id}")

        if drone_energy_used > battery_limit:
            overused_battery_count += 1
            print(f"🔋 [Batarya AŞIMI] Drone {d_id} | Enerji: {drone_energy_used:.1f} / Kapasite: {battery_limit}")

    fitness = (
        completed * 100
        - total_energy
        - penalty_count * 100
        - overused_battery_count * 300
    )

    print(f"📈 Fitness: {fitness:.2f} | Tamamlanan: {completed}, Ceza: {penalty_count}, Batarya Aşımı: {overused_battery_count}, Toplam Enerji: {total_energy:.1f}")
    return fitness, completed, csp_rejected, penalty_count, overused_battery_count, total_energy


from random import shuffle, choice

def generate_individual(drones, deliveries, no_fly_zones):
    assignments = {d["id"]: [] for d in drones}
    delivery_ids = [d["id"] for d in deliveries]
    shuffle(delivery_ids)
    assigned = set()

    for delivery_id in delivery_ids:
        if delivery_id in assigned:
            continue

        delivery = next(d for d in deliveries if d["id"] == delivery_id)
        valid_drones = []

        for drone in drones:
            if not is_valid_delivery(drone, delivery, 570):
                continue

            start = tuple(drone["start_pos"])
            goal = tuple(delivery["pos"])
            path = astar_with_no_fly_penalty(start, goal, no_fly_zones, max_steps=1000, current_time="09:30")

            if path:
                valid_drones.append(drone["id"])

        if valid_drones:
            assigned_drone = choice(valid_drones)
            assignments[assigned_drone].append(delivery_id)
            assigned.add(delivery_id)

    return assignments

def crossover(parent1, parent2):
    child = {}
    for d_id in parent1:
        if random.random() < 0.5:
            child[d_id] = parent1[d_id][:]
        else:
            child[d_id] = parent2[d_id][:]
    return child

def mutate(assignments, mutation_rate=0.1):
    delivery_list = [(d_id, deliv) for d_id, deliveries in assignments.items() for deliv in deliveries]
    if not delivery_list:
        return assignments

    for _ in range(int(len(delivery_list) * mutation_rate)):
        d1, delivery_id = random.choice(delivery_list)
        d2 = random.choice(list(assignments.keys()))
        if delivery_id in assignments[d1]:
            assignments[d1].remove(delivery_id)
            if delivery_id not in assignments[d2]:
                assignments[d2].append(delivery_id)
    return assignments

def run_genetic_algorithm(drones, deliveries, no_fly_zones, generations=5, pop_size=10):
    print("🧬 Popülasyon başlatılıyor...")
    population = []
    for _ in range(pop_size):
        ind = generate_individual(drones, deliveries, no_fly_zones)
        fit, *_ = calculate_fitness(ind, drones, deliveries, no_fly_zones)
        population.append({"assignments": ind, "fitness": fit})

    for gen in range(generations):
        population.sort(key=lambda x: x["fitness"], reverse=True)
        new_population = population[:2]

        while len(new_population) < pop_size:
            p1, p2 = random.sample(population[:5], 2)
            child_assignments = crossover(p1["assignments"], p2["assignments"])
            mutated = mutate(child_assignments)
            fit, *_ = calculate_fitness(mutated, drones, deliveries, no_fly_zones)
            new_population.append({"assignments": mutated, "fitness": fit})

        population = new_population
        print(f"\n🔄 Nesil: {gen + 1} tamamlandı.")

    best = max(population, key=lambda x: x["fitness"])
    best_assignments = best["assignments"]
    best_fitness, completed, csp_rejected, penalty_count, battery_over, total_energy = calculate_fitness(best_assignments, drones, deliveries, no_fly_zones)

    return best_assignments, best_fitness, completed, csp_rejected, penalty_count, battery_over, total_energy