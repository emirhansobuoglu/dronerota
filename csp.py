from datetime import datetime

def time_str_to_minutes(time_str):
    """HH:MM formatındaki zamanı dakika cinsine çevirir"""
    h, m = map(int, time_str.split(":"))
    return h * 60 + m

def is_valid_delivery(drone, delivery, now):
    """
    CSP kurallarına göre bir teslimatın geçerli olup olmadığını kontrol eder.
    Parametreler:
        drone: drone sözlüğü
        delivery: teslimat sözlüğü
        now: dakika cinsinden int zaman (örnek: 570 = 09:30)
    """
    # Ağırlık kontrolü
    if delivery["weight"] > drone["max_weight"]:
        return False

    # Zaman aralığını dakikaya çevir
    start_str, end_str = delivery["time_window"]
    start = time_str_to_minutes(start_str)
    end = time_str_to_minutes(end_str)

    # now zaten int dakika olarak geliyor
    in_time_window = start <= now <= end

    return in_time_window
