import random
from math import sqrt
from csp import is_valid_delivery
from astar import astar_with_no_fly_penalty

def euclidean(p1, p2):
    return sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def calculate_fitness(assignments, drones, deliveries, no_fly_zones):
    completed = 0
    total_energy = 0
    penalty_count = 0
    overused_battery_count = 0

    path_cache = {}  # (drone_id, delivery_id): path
    print("📊 [Fitness] Hesaplama başlatıldı...")

    for d_id, delivery_ids in assignments.items():
        drone = next(d for d in drones if d["id"] == d_id)
        start = tuple(drone["start_pos"])
        battery_limit = drone["battery"]
        drone_energy_used = 0

        print(f"🚁 Drone {d_id} → Teslimatlar: {delivery_ids}")

        for delivery_id in delivery_ids:
            delivery = next(d for d in deliveries if d["id"] == delivery_id)

            # CSP kontrolü (zaman ve ağırlık)
            if not is_valid_delivery(drone, delivery):
                print(f"⚠ [CSP Red] Drone {d_id} → Teslimat {delivery_id}")
                continue

            goal = tuple(delivery["pos"])
            cache_key = (d_id, delivery_id)

            # Cache kontrolü
            if cache_key in path_cache:
                path = path_cache[cache_key]
            else:
                path = astar_with_no_fly_penalty(start, goal, no_fly_zones, max_steps=2000)
                path_cache[cache_key] = path

            if path:
                path_len = len(path)
                energy = path_len * delivery["weight"]
                drone_energy_used += energy
                total_energy += energy
                completed += 1
                start = goal
            else:
                penalty_count += 1
                print(f"❌ [Rota Yok] Drone {d_id} → Teslimat {delivery_id}")

        if drone_energy_used > battery_limit:
            overused_battery_count += 1
            print(f"🔋 [Batarya AŞIMI] Drone {d_id} | Enerji: {drone_energy_used:.1f} / Kapasite: {battery_limit}")

    # Fitness değeri formülü
    fitness = (
        completed * 100
        - total_energy
        - penalty_count * 100
        - overused_battery_count * 300
    )

    print(f"📈 Fitness: {fitness:.2f} | Tamamlanan: {completed}, Ceza: {penalty_count}, Batarya Aşımı: {overused_battery_count}, Toplam Enerji: {total_energy:.1f}")
    return fitness



from random import shuffle, choice
from astar import astar_with_no_fly_penalty
from csp import is_valid_delivery

def generate_individual(drones, deliveries, no_fly_zones):
    assignments = {d["id"]: [] for d in drones}
    delivery_ids = [d["id"] for d in deliveries]
    shuffle(delivery_ids)

    for delivery_id in delivery_ids:
        delivery = next(d for d in deliveries if d["id"] == delivery_id)
        valid_drones = []

        for drone in drones:
            if not is_valid_delivery(drone, delivery):
                continue

            # Rota var mı?
            start = tuple(drone["start_pos"])
            goal = tuple(delivery["pos"])
            path = astar_with_no_fly_penalty(start, goal, no_fly_zones, max_steps=1000)

            if path:
                valid_drones.append(drone["id"])

        if valid_drones:
            assigned = choice(valid_drones)
            assignments[assigned].append(delivery_id)

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
    delivery_list = []
    for d_id, deliveries in assignments.items():
        for deliv in deliveries:
            delivery_list.append((d_id, deliv))
    if not delivery_list:
        return assignments
    for _ in range(int(len(delivery_list) * mutation_rate)):
        d1, delivery_id = random.choice(delivery_list)
        d2 = random.choice(list(assignments.keys()))
        if delivery_id in assignments[d1]:
            assignments[d1].remove(delivery_id)
            assignments[d2].append(delivery_id)
    return assignments

def run_genetic_algorithm(drones, deliveries, no_fly_zones, generations=5, pop_size=10):
    print("🧬 Popülasyon başlatılıyor...")
    population = []
    for _ in range(pop_size):
        ind = generate_individual(drones, deliveries, no_fly_zones)
        fit = calculate_fitness(ind, drones, deliveries, no_fly_zones)
        population.append({"assignments": ind, "fitness": fit})

    for gen in range(generations):
        population.sort(key=lambda x: x["fitness"], reverse=True)
        new_population = population[:2]

        while len(new_population) < pop_size:
            p1, p2 = random.sample(population[:5], 2)
            child_assignments = crossover(p1["assignments"], p2["assignments"])
            mutated = mutate(child_assignments)
            fit = calculate_fitness(mutated, drones, deliveries, no_fly_zones)
            new_population.append({"assignments": mutated, "fitness": fit})

        population = new_population
        print(f"\n🔄 Nesil: {gen + 1} tamamlandı.")

    best = max(population, key=lambda x: x["fitness"])
    return best["assignments"], best["fitness"]
