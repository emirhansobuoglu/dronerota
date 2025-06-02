import json
import random

def generate_drones(n=10):
    drones = []
    for i in range(n):
        drone = {
            "id": i,
            "max_weight": round(random.uniform(2.0, 6.0), 2),
            "battery": random.randint(8000, 20000),
            "speed": round(random.uniform(6.0, 14.0), 2),
            "start_pos": [random.randint(0, 100), random.randint(0, 100)]
        }
        drones.append(drone)
    return drones

def generate_deliveries(n=50):
    deliveries = []
    for i in range(n):
        start_hour = random.randint(9, 10)
        start_min = random.randint(0, 59)
        duration = random.randint(15, 60)
        end_hour = start_hour + (start_min + duration) // 60
        end_min = (start_min + duration) % 60

        delivery = {
            "id": i,
            "pos": [random.randint(0, 100), random.randint(0, 100)],
            "weight": round(random.uniform(0.5, 4.5), 2),
            "priority": random.randint(1, 5),
            "time_window": [
                f"{start_hour:02d}:{start_min:02d}",
                f"{end_hour:02d}:{end_min:02d}"
            ]
        }
        deliveries.append(delivery)
    return deliveries

def generate_no_fly_zones(n=5):
    zones = []
    for i in range(n):
        x = random.randint(10, 80)
        y = random.randint(10, 80)
        w = random.randint(5, 15)
        h = random.randint(5, 15)

        start_hour = random.randint(9, 10)
        start_min = random.randint(0, 59)
        duration = random.randint(10, 60)
        end_hour = start_hour + (start_min + duration) // 60
        end_min = (start_min + duration) % 60

        zone = {
            "id": i,
            "coordinates": [
                [x, y],
                [x + w, y],
                [x + w, y + h],
                [x, y + h]
            ],
            "active_time": [
                f"{start_hour:02d}:{start_min:02d}",
                f"{end_hour:02d}:{end_min:02d}"
            ]
        }
        zones.append(zone)
    return zones

def generate_dataset():
    dataset = {
        "drones": generate_drones(10),
        "deliveries": generate_deliveries(50),
        "no_fly_zones": generate_no_fly_zones(5)
    }

    with open("sample_data_large.json", "w") as f:
        json.dump(dataset, f, indent=4)
    print("✅ Yeni veri dosyası başarıyla oluşturuldu: sample_data_large.json")

if __name__ == "__main__":
    generate_dataset()
