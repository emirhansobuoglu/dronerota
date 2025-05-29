from datetime import datetime

def parse_time(time_str: str) -> datetime:
    """
    Saat string'ini datetime objesine çevirir.
    Örn: "09:30" → datetime(2025, 1, 1, 9, 30)
    """
    return datetime.strptime(time_str, "%H:%M")

def is_valid_delivery(drone: dict, delivery: dict, current_time: str = "09:30") -> bool:
    """
    Bir drone'un belirli bir teslimatı yapıp yapamayacağını kontrol eder.
    Kısıtlar:
      - Teslimatın ağırlığı drone'un kapasitesini aşmamalı.
      - Şu anki saat teslimat zaman aralığı içinde olmalı.

    Parametreler:
      - drone: {"max_weight": float, ...}
      - delivery: {"weight": float, "time_window": ["HH:MM", "HH:MM"]}
      - current_time: "HH:MM" formatında saat (default: 09:30)

    Geri dönüş:
      - True: Teslimat yapılabilir
      - False: Kısıtlardan biri ihlal edilmiş
    """
    now = parse_time(current_time)
    start, end = map(parse_time, delivery["time_window"])

    in_time_window = start <= now <= end
    weight_ok = delivery["weight"] <= drone["max_weight"]

    return in_time_window and weight_ok
