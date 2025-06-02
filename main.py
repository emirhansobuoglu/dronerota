import json
import matplotlib.pyplot as plt
from shapely.geometry import Polygon
from genetic import run_genetic_algorithm
from astar import astar_with_no_fly_penalty
from astar_planner import plan_with_astar

# ------------------ VERİ YÜKLE ------------------
with open("sample_data_large.json", "r") as f:
    data = json.load(f)

drones = data["drones"]
deliveries = data["deliveries"]
no_fly_zones = data["no_fly_zones"]

# ------------------ GENETİK ALGORİTMA ------------------
print("🔁 Genetik algoritma başlatılıyor...")
assignments, best_fitness, completed, csp_rejected, penalty_count, battery_over, total_energy = run_genetic_algorithm(
    drones, deliveries, no_fly_zones,
    generations=5,
    pop_size=10
)

# ------------------ SONUÇLARI YAZDIR ------------------
print("\n🎉 Genetik algoritma tamamlandı!")
print(f"🏆 En iyi fitness: {best_fitness:.2f}\n")

for drone_id, delivery_list in assignments.items():
    if delivery_list:
        print(f"🚁 Drone {drone_id} → 📦 Teslimatlar: {delivery_list}")
    else:
        print(f"🚁 Drone {drone_id} → ⛔ Teslimat atanmadı")

# ------------------ PERFORMANS ANALİZİ ------------------
print("\n📊 PERFORMANS ANALİZİ (GA)")
print(f"✔️ Tamamlanan teslimatlar: {completed}")
print(f"⚠️ CSP reddedilenler: {csp_rejected}")
print(f"❌ Rota bulunamayanlar: {penalty_count}")
print(f"🔋 Batarya aşımı yaşayan drone sayısı: {battery_over}")
print(f"⚡ Toplam enerji tüketimi: {total_energy:.2f}")
print(f"⚡ Ortalama enerji / teslimat: {(total_energy / completed) if completed else 0:.2f}")

# ------------------ A* PLANLAYICI ------------------
print("\n🧭 A* algoritması ile planlama başlatılıyor...")
astar_assignments = plan_with_astar(drones, deliveries, no_fly_zones)
print("✅ A* tamamlandı. Sonuçlar:")
for drone_id, delivery_list in astar_assignments.items():
    if delivery_list:
        print(f"🚁 Drone {drone_id} (A*) → 📦 Teslimatlar: {delivery_list}")
    else:
        print(f"🚁 Drone {drone_id} (A*) → ⛔ Teslimat atanmadı")

# ------------------ GÖRSELLEŞTİRME ------------------
colors = ["blue", "green", "purple", "orange", "cyan", "brown", "magenta", "gray", "lime", "pink"]
plt.figure(figsize=(12, 6))

# --- GA rotaları çiz ---
for drone in drones:
    d_id = drone["id"]
    start = tuple(drone["start_pos"])
    deliveries_ids = assignments.get(d_id, [])
    current_pos = start

    for del_id in deliveries_ids:
        delivery = next(d for d in deliveries if d["id"] == del_id)
        goal = tuple(delivery["pos"])
        path = astar_with_no_fly_penalty(current_pos, goal, no_fly_zones, max_steps=1000, current_time=30)
        if path:
            x, y = zip(*path)
            color = colors[d_id % len(colors)]
            plt.plot(x, y, label=f"GA - Drone {d_id} → {del_id}", color=color, linestyle='-')
            plt.scatter(*current_pos, color="black", marker="o", s=30)
            plt.scatter(*goal, color="red", marker="x", s=50)
            current_pos = goal

# --- A* rotaları çiz ---
for drone in drones:
    d_id = drone["id"]
    start = tuple(drone["start_pos"])
    deliveries_ids = astar_assignments.get(d_id, [])
    current_pos = start

    for del_id in deliveries_ids:
        delivery = next(d for d in deliveries if d["id"] == del_id)
        goal = tuple(delivery["pos"])
        path = astar_with_no_fly_penalty(current_pos, goal, no_fly_zones, max_steps=1000, current_time=30)
        if path:
            x, y = zip(*path)
            color = colors[d_id % len(colors)]
            plt.plot(x, y, label=f"A* - Drone {d_id} → {del_id}", color=color, linestyle='--')  # <-- çizgi tipi farklı
            current_pos = goal

# ------------------ NO-FLY ZONE GÖSTERİMİ ------------------
first_zone = True
for zone in no_fly_zones:
    poly = Polygon(zone["coordinates"])
    px, py = poly.exterior.xy
    label = "No-Fly Zone" if first_zone else None
    first_zone = False
    plt.fill(px, py, color="orange", alpha=0.3, label=label)

# ------------------ SABİT GÖSTERİMLER ------------------
plt.scatter([], [], color="black", marker="o", label="Başlangıç Noktası", s=30)
plt.scatter([], [], color="red", marker="x", label="Teslimat Noktası", s=50)

# ------------------ AYARLAR ------------------
plt.title("🚁 Drone Teslimat Rotaları (GA ve A* Karşılaştırması)")
plt.xlim(0, 100)
plt.ylim(0, 100)
plt.xlabel("X Koordinat")
plt.ylabel("Y Koordinat")
plt.grid(True)
plt.legend(loc="best")
plt.tight_layout()
plt.show()
