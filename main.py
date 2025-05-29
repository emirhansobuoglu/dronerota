import json
import matplotlib.pyplot as plt
from shapely.geometry import Polygon
from genetic import run_genetic_algorithm
from astar import astar_with_no_fly_penalty

# ------------------ VERİ YÜKLE ------------------
with open("sample_data.json", "r") as f:
    data = json.load(f)

drones = data["drones"]
deliveries = data["deliveries"]
no_fly_zones = data["no_fly_zones"]

# ------------------ GENETİK ALGORİTMA ------------------
print("🔁 Genetik algoritma başlatılıyor...")
assignments, best_fitness = run_genetic_algorithm(
    drones, deliveries, no_fly_zones,
    generations=5,  # test için düşük tutuldu
    pop_size=6
)

# ------------------ SONUÇLARI YAZDIR ------------------
print("\n🎉 Genetik algoritma tamamlandı!")
print(f"🏆 En iyi fitness: {best_fitness:.2f}\n")

for drone_id, delivery_list in assignments.items():
    if delivery_list:
        print(f"🚁 Drone {drone_id} → 📦 Teslimatlar: {delivery_list}")
    else:
        print(f"🚁 Drone {drone_id} → ⛔ Teslimat atanmadı")

# ------------------ GÖRSELLEŞTİRME ------------------
colors = ["blue", "green", "purple", "orange", "cyan", "brown", "magenta"]
plt.figure(figsize=(12, 6))

for drone in drones:
    d_id = drone["id"]
    start = tuple(drone["start_pos"])
    deliveries_ids = assignments.get(d_id, [])

    current_pos = start
    for i, del_id in enumerate(deliveries_ids):
        delivery = next(d for d in deliveries if d["id"] == del_id)
        goal = tuple(delivery["pos"])
        path = astar_with_no_fly_penalty(current_pos, goal, no_fly_zones, max_steps=1000)

        if path:
            x, y = zip(*path)
            color = colors[d_id % len(colors)]
            plt.plot(x, y, label=f"Drone {d_id} → Teslimat {del_id}", color=color)
            plt.scatter(*current_pos, color="black", marker="o", s=30)
            plt.scatter(*goal, color="red", marker="x", s=50)
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
plt.title("🚁 Drone Teslimat Rotaları (Genetik Algoritma ile)")
plt.xlim(0, 100)
plt.ylim(0, 100)
plt.xlabel("X Koordinat")
plt.ylabel("Y Koordinat")
plt.grid(True)
plt.legend(loc="best")
plt.tight_layout()
plt.show()
