# utils/data_generator.py - İYİLEŞTİRİLMİŞ VERSİYON

import math
import random
from typing import List, Tuple, Dict
from models.drone import Drone
from models.delivery_point import DeliveryPoint
from models.no_fly_zone import NoFlyZone

class DataGenerator:
    
    @staticmethod
    def validate_dataset(drones: List[Drone], deliveries: List[DeliveryPoint], 
                        no_fly_zones: List[NoFlyZone]) -> Dict[str, any]:
        """VERİ SETİ DOĞRULAMA - YENİ EKLENEN ÖZELLİK"""
        validation_report = {
            'is_valid': True,
            'warnings': [],
            'errors': [],
            'statistics': {}
        }
        
        # 1. Temel sayı kontrolleri
        if len(drones) == 0:
            validation_report['errors'].append("Drone sayısı sıfır!")
            validation_report['is_valid'] = False
        
        if len(deliveries) == 0:
            validation_report['errors'].append("Teslimat sayısı sıfır!")
            validation_report['is_valid'] = False
        
        # 2. Kapasite kontrolleri
        total_delivery_weight = sum(d.weight for d in deliveries)
        total_drone_capacity = sum(d.max_weight for d in drones)
        
        if total_delivery_weight > total_drone_capacity:
            validation_report['warnings'].append(
                f"Toplam teslimat ağırlığı ({total_delivery_weight:.1f}) > "
                f"Toplam drone kapasitesi ({total_drone_capacity:.1f})"
            )
        
        # 3. Batarya kontrolleri
        max_distance = 0
        for delivery in deliveries:
            for drone in drones:
                distance = math.sqrt(
                    (delivery.pos[0] - drone.start_pos[0])**2 + 
                    (delivery.pos[1] - drone.start_pos[1])**2
                )
                max_distance = max(max_distance, distance)
        
        min_battery = min(d.battery for d in drones)
        estimated_energy_need = max_distance * 10  # Basit tahmin
        
        if min_battery < estimated_energy_need:
            validation_report['warnings'].append(
                f"En düşük batarya ({min_battery}) uzak teslimatlar için yetersiz olabilir"
            )
        
        # 4. İstatistikler
        validation_report['statistics'] = {
            'total_drones': len(drones),
            'total_deliveries': len(deliveries),
            'total_no_fly_zones': len(no_fly_zones),
            'avg_drone_capacity': sum(d.max_weight for d in drones) / len(drones),
            'avg_delivery_weight': sum(d.weight for d in deliveries) / len(deliveries),
            'capacity_utilization': (total_delivery_weight / total_drone_capacity) * 100,
            'high_priority_deliveries': sum(1 for d in deliveries if d.priority >= 4),
            'max_distance_to_cover': max_distance
        }
        
        return validation_report
    
    @staticmethod
    def load_predefined_dataset(validate: bool = True) -> dict:
        """HAZIR VERİ SETİ - VALİDASYON DESTEĞİ İLE"""
        print("📊 Hazır veri seti yükleniyor...")
        
        # SİZİN HAZIR VERİ SETİNİZ
        drone_data = [
            {"id": 1, "max_weight": 4.0, "battery": 12000, "speed": 8.0, "start_pos": (10, 10)},
            {"id": 2, "max_weight": 3.5, "battery": 10000, "speed": 10.0, "start_pos": (20, 30)},
            {"id": 3, "max_weight": 5.0, "battery": 15000, "speed": 7.0, "start_pos": (50, 50)},
            {"id": 4, "max_weight": 2.0, "battery": 8000, "speed": 12.0, "start_pos": (80, 20)},
            {"id": 5, "max_weight": 6.0, "battery": 20000, "speed": 5.0, "start_pos": (40, 70)}
        ]
        
        delivery_data = [
            {"id": 1, "pos": (15, 25), "weight": 1.5, "priority": 3, "time_window": (0, 60)},
            {"id": 2, "pos": (30, 40), "weight": 2.0, "priority": 5, "time_window": (0, 30)},
            {"id": 3, "pos": (70, 80), "weight": 3.0, "priority": 2, "time_window": (20, 80)},
            {"id": 4, "pos": (90, 10), "weight": 1.0, "priority": 4, "time_window": (10, 40)},
            {"id": 5, "pos": (45, 60), "weight": 4.0, "priority": 1, "time_window": (30, 90)},
            {"id": 6, "pos": (25, 15), "weight": 2.5, "priority": 3, "time_window": (0, 50)},
            {"id": 7, "pos": (60, 30), "weight": 1.0, "priority": 5, "time_window": (5, 25)},
            {"id": 8, "pos": (85, 90), "weight": 3.5, "priority": 2, "time_window": (40, 100)},
            {"id": 9, "pos": (10, 80), "weight": 2.0, "priority": 4, "time_window": (15, 45)},
            {"id": 10, "pos": (95, 50), "weight": 1.5, "priority": 3, "time_window": (0, 60)},
            {"id": 11, "pos": (55, 20), "weight": 0.5, "priority": 5, "time_window": (0, 20)},
            {"id": 12, "pos": (35, 75), "weight": 2.0, "priority": 1, "time_window": (50, 120)},
            {"id": 13, "pos": (75, 40), "weight": 3.0, "priority": 3, "time_window": (10, 50)},
            {"id": 14, "pos": (20, 90), "weight": 1.5, "priority": 4, "time_window": (30, 70)},
            {"id": 15, "pos": (65, 65), "weight": 4.5, "priority": 2, "time_window": (25, 75)},
            {"id": 16, "pos": (40, 10), "weight": 2.0, "priority": 5, "time_window": (0, 30)},
            {"id": 17, "pos": (5, 50), "weight": 1.0, "priority": 3, "time_window": (15, 55)},
            {"id": 18, "pos": (50, 85), "weight": 3.0, "priority": 1, "time_window": (60, 100)},
            {"id": 19, "pos": (80, 70), "weight": 2.5, "priority": 4, "time_window": (20, 60)},
            {"id": 20, "pos": (30, 55), "weight": 1.5, "priority": 2, "time_window": (40, 80)}
        ]
        
        nfz_data = [
            {
                "id": 1,
                "coordinates": [(40, 30), (60, 30), (60, 50), (40, 50)],
                "active_time": (0, 120)
            },
            {
                "id": 2,
                "coordinates": [(70, 10), (90, 10), (90, 30), (70, 30)],
                "active_time": (30, 90)
            },
            {
                "id": 3,
                "coordinates": [(10, 60), (30, 60), (30, 80), (10, 80)],
                "active_time": (0, 60)
            }
        ]
        
        # GELİŞTİRİLMİŞ TIME WINDOW DÖNÜŞTÜRME
        def convert_numeric_to_time_string(time_tuple, base_hour=9):
            """Sayısal time_window'u string formatına çevir"""
            start_minutes, end_minutes = time_tuple
            
            # Dakikaları saat:dakika formatına çevir
            start_total_minutes = start_minutes
            end_total_minutes = end_minutes
            
            start_hour = base_hour + (start_total_minutes // 60)
            start_min = start_total_minutes % 60
            end_hour = base_hour + (end_total_minutes // 60)
            end_min = end_total_minutes % 60
            
            # 24 saat formatını aşmasını önle
            start_hour = min(start_hour, 23)
            end_hour = min(end_hour, 23)
            
            return (f"{start_hour:02d}:{start_min:02d}", f"{end_hour:02d}:{end_min:02d}")
        
        # Objeler oluştur
        drones = []
        for data in drone_data:
            drone = Drone(
                id=data["id"] - 1,  # 0-indexed
                max_weight=data["max_weight"],
                battery=data["battery"],
                speed=data["speed"],
                start_pos=data["start_pos"]
            )
            drones.append(drone)
        
        deliveries = []
        for data in delivery_data:
            time_window_str = convert_numeric_to_time_string(data["time_window"])
            delivery = DeliveryPoint(
                id=data["id"] - 1,
                pos=data["pos"],
                weight=data["weight"],
                priority=data["priority"],
                time_window=time_window_str
            )
            deliveries.append(delivery)
        
        no_fly_zones = []
        for data in nfz_data:
            active_time_str = convert_numeric_to_time_string(data["active_time"])
            nfz = NoFlyZone(
                id=data["id"] - 1,
                coordinates=data["coordinates"],
                active_time=active_time_str
            )
            no_fly_zones.append(nfz)
        
        # VALİDASYON KONTROLÜ
        if validate:
            validation_report = DataGenerator.validate_dataset(drones, deliveries, no_fly_zones)
            
            print(f"\n🔍 VERİ SETİ VALİDASYON RAPORU:")
            print(f"✅ Geçerlilik: {'BAŞARILI' if validation_report['is_valid'] else 'BAŞARISIZ'}")
            
            if validation_report['errors']:
                print("❌ HATALAR:")
                for error in validation_report['errors']:
                    print(f"   - {error}")
            
            if validation_report['warnings']:
                print("⚠️ UYARILAR:")
                for warning in validation_report['warnings']:
                    print(f"   - {warning}")
            
            stats = validation_report['statistics']
            print(f"\n📊 İSTATİSTİKLER:")
            print(f"   🚁 Dronlar: {stats['total_drones']} (Ort. kapasite: {stats['avg_drone_capacity']:.1f}kg)")
            print(f"   📦 Teslimatlar: {stats['total_deliveries']} (Ort. ağırlık: {stats['avg_delivery_weight']:.1f}kg)")
            print(f"   🚫 Yasak bölgeler: {stats['total_no_fly_zones']}")
            print(f"   📈 Kapasite kullanımı: {stats['capacity_utilization']:.1f}%")
            print(f"   🔥 Yüksek öncelikli: {stats['high_priority_deliveries']}")
            print(f"   📏 Max mesafe: {stats['max_distance_to_cover']:.1f}")
        
        print(f"\n✅ Hazır veri seti başarıyla yüklendi!")
        
        return {
            'drones': drones,
            'deliveries': deliveries,
            'no_fly_zones': no_fly_zones,
            'scenario_name': 'Validated Predefined Dataset',
            'description': f'{len(drones)} drones, {len(deliveries)} deliveries with validation',
            'validation_report': validation_report if validate else None
        }
    
    @staticmethod
    def generate_mixed_scenario_improved() -> dict:
        """GELİŞTİRİLMİŞ karma senaryo"""
        print("🔄 Geliştirilmiş karma senaryo oluşturuluyor...")
        
        # Hazır veriyi yükle (validasyon ile)
        predefined = DataGenerator.load_predefined_dataset(validate=True)
        
        # Ek rastgele teslimatlar - hazır verilerle uyumlu
        additional_deliveries = []
        base_id = len(predefined['deliveries'])
        
        for i in range(8):  # 8 ek teslimat (20+8=28 toplam)
            pos = (random.uniform(5, 95), random.uniform(5, 95))
            weight = random.uniform(0.5, 3.0)  # Hafif teslimatlar
            priority = random.randint(2, 5)
            
            # Time window'u hazır verilerle uyumlu yap
            start_minute = random.randint(0, 80)
            duration = random.randint(30, 60)
            end_minute = min(start_minute + duration, 120)
            
            start_hour = 9 + (start_minute // 60)
            start_min = start_minute % 60
            end_hour = 9 + (end_minute // 60)
            end_min = end_minute % 60
            
            time_window = (f"{start_hour:02d}:{start_min:02d}", f"{end_hour:02d}:{end_min:02d}")
            
            additional_deliveries.append(DeliveryPoint(
                id=base_id + i,
                pos=pos,
                weight=weight,
                priority=priority,
                time_window=time_window
            ))
        
        all_deliveries = predefined['deliveries'] + additional_deliveries
        
        # Son validasyon
        final_validation = DataGenerator.validate_dataset(
            predefined['drones'], all_deliveries, predefined['no_fly_zones']
        )
        
        return {
            'drones': predefined['drones'],
            'deliveries': all_deliveries,
            'no_fly_zones': predefined['no_fly_zones'],
            'scenario_name': 'Improved Mixed Scenario',
            'description': f"{len(predefined['drones'])} drones, {len(all_deliveries)} validated mixed deliveries",
            'validation_report': final_validation
        }

    # ... (diğer metodlar aynı kalabilir)
    
    @staticmethod
    def generate_drones(n: int) -> List[Drone]:
        drones = []
        for i in range(n):
            max_weight = random.uniform(3, 8)
            battery = random.randint(8000, 15000)
            speed = random.uniform(8, 15)
            start_pos = (random.uniform(0, 100), random.uniform(0, 100))
            drones.append(Drone(i, max_weight, battery, speed, start_pos))
        return drones

    @staticmethod
    def generate_delivery_points(n: int) -> List[DeliveryPoint]:
        delivery_points = []
        for i in range(n):
            pos = (random.uniform(0, 100), random.uniform(0, 100))
            weight = random.uniform(1, 4)
            priority = random.randint(1, 5)
            hour = random.randint(9, 15)
            time_window = (f"{hour:02d}:00", f"{hour+1:02d}:00")
            delivery_points.append(DeliveryPoint(i, pos, weight, priority, time_window))
        return delivery_points

    @staticmethod
    def generate_no_fly_zones(n: int) -> List[NoFlyZone]:
        no_fly_zones = []
        for i in range(n):
            center_x = random.uniform(20, 80)
            center_y = random.uniform(20, 80)
            radius = random.uniform(5, 15)
            polygon = [(center_x + radius * random.uniform(0.8, 1.2) * math.cos(a),
                        center_y + radius * random.uniform(0.8, 1.2) * math.sin(a)) 
                       for a in [i * 2 * math.pi / 6 for i in range(6)]]
            hour = random.randint(9, 14)
            time_window = (f"{hour:02d}:00", f"{hour+2:02d}:00")
            no_fly_zones.append(NoFlyZone(i, polygon, time_window))
        return no_fly_zones