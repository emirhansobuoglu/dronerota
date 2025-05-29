import random
import json
from datetime import datetime, timedelta

def random_time_window(start_hour=9, end_hour=17):
    start = datetime(2025, 5, 12, start_hour)
    end = datetime(2025, 5, 12, end_hour)
    t1 = start + timedelta(minutes=random.randint(0, 60))
    t2 = t1 + timedelta(minutes=random.randint(30, 90))
    return (t1.strftime("%H:%M"), t2.strftime("%H:%M"))

def generate_drones(n=5):
    drones = []
    for i in range(n):
        drone = {
            "id": i,
            "max_weight": round(random.uniform(2.0, 5.0), 2),
            "battery": random.randint(4000, 7000),
            "speed": round(random.uniform(5.0, 15.0), 1),
            "start_pos": (random.randint(0, 100), random.randint(0, 100))
        }
        drones.append(drone)
    return drones

def generate_deliveries(n=20):
    deliveries = []
    for i in range(n):
        delivery = {
            "id": i,
            "pos": (random.randint(0, 100), random.randint(0, 100)),
            "weight": round(random.uniform(0.5, 3.0), 2),
            "priority": random.randint(1, 5),
            "time_window": random_time_window()
        }
        deliveries.append(delivery)
    return deliveries

def generate_no_fly_zones(n=2):
    zones = []
    for i in range(n):
        x, y = random.randint(10, 90), random.randint(10, 90)
        size = random.randint(5, 15)
        zone = {
            "id": i,
            "coordinates": [
                (x, y),
                (x + size, y),
                (x + size, y + size),
                (x, y + size)
            ],
            "active_time": random_time_window()
        }
        zones.append(zone)
    return zones

def save_data(drones, deliveries, zones):
    data = {
        "drones": drones,
        "deliveries": deliveries,
        "no_fly_zones": zones
    }
    with open("sample_data.json", "w") as f:
        json.dump(data, f, indent=4)

# Kullanım
if __name__ == "__main__":
    drones = generate_drones(5)
    deliveries = generate_deliveries(20)
    zones = generate_no_fly_zones(2)
    save_data(drones, deliveries, zones)
    print("Veri dosyası 'sample_data.json' olarak kaydedildi.")
