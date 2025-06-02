# 🚁 Drone Teslimat Optimizasyonu (GA & A*)

Bu proje, drone'lar ile zaman kısıtlı teslimatları optimize etmek amacıyla Genetik Algoritma (GA) ve A* (A-Star) algoritmalarını karşılaştırarak çalışır. Proje; batarya limiti, no-fly zone (uçuşa yasak bölge), teslimat zamanı, enerji tüketimi gibi çoklu kısıtları dikkate alır.

## 🔧 Kullanılan Teknolojiler
- Python 3.x
- matplotlib (görselleştirme için)
- shapely (no-fly zone polygonları için)
- JSON (veri okuma)
- A* ve Genetik Algoritma implementasyonu

## 📁 Proje Yapısı
```
.
├── main.py                # Ana yürütme dosyası (GA ve A* çalıştırır, karşılaştırma yapar)
├── genetic.py             # Genetik algoritma mantığı ve fitness hesaplaması
├── astar.py               # A* algoritmasının temel rotalama fonksiyonu
├── astar_planner.py       # A* algoritması ile görev atama planlaması
├── csp.py                 # Zaman penceresi ve kısıt kontrolleri
├── sample_data_large.json # Drone, teslimat ve no-fly zone bilgileri
└── README.md              # Proje tanıtım ve kullanım dosyası
```

## ⚙️ Kurulum ve Çalıştırma
1. Gerekli kütüphaneleri kurun:
   ```bash
   pip install matplotlib shapely
   ```

2. Ana dosyayı çalıştırın:
   ```bash
   python main.py
   ```

3. Çalışma sonrası terminalde analizler ve matplotlib ile grafiksel bir çıktı görüntülenir.

## 🎯 Özellikler
- [x] Genetik Algoritma ile rotalama ve görev atama
- [x] A* algoritması ile en kısa yol hesaplama ve görev atama
- [x] No-fly zone engelleri
- [x] Batarya limiti ve şarj etme süresi
- [x] Zaman pencereli teslimat kısıtı
- [x] Detaylı karşılaştırmalı performans analizi ve görselleştirme

## 📊 Örnek Görsel
![WhatsApp Image 2025-06-02 at 11 51 27 (1)](https://github.com/user-attachments/assets/0a54aba7-46af-407c-a308-b9c88d3dc57d)

## 🧠 Karşılaştırma Mantığı
- **Genetik Algoritma**: Rastgele atanmış bireylerden başlayan, çaprazlama ve mutasyonla iyileştirilen çözümler üretir.
- **A***: Her drone için greedy ama kurallara uygun en iyi teslimatı sırayla seçerek görev atar.
- **Karşılaştırma**:
  - A* daha çok teslimat tamamlayabilir, ama GA daha az enerji harcar.
  - A* deterministik, GA daha esnek ama rastgele davranır.
  - Her iki yöntemin rotaları grafikle karşılaştırmalı gösterilir.
