import math
import random
from typing import List, Tuple
from models.drone import Drone
from models.delivery_point import DeliveryPoint
from models.no_fly_zone import NoFlyZone

class DataGenerator:
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

    @staticmethod
    def load_predefined_dataset() -> dict:
        """HAZIR VERİ SETİ - Gerçekçi test verisi"""
        print("📊 Hazır veri seti yükleniyor...")
        
        # Hazır drone verisi
        drone_data = [
            {"id": 1, "max_weight": 4.0, "battery": 12000, "speed": 8.0, "start_pos": (10, 10)},
            {"id": 2, "max_weight": 3.5, "battery": 10000, "speed": 10.0, "start_pos": (20, 30)},
            {"id": 3, "max_weight": 5.0, "battery": 15000, "speed": 7.0, "start_pos": (50, 50)},
            {"id": 4, "max_weight": 2.0, "battery": 8000, "speed": 12.0, "start_pos": (80, 20)},
            {"id": 5, "max_weight": 6.0, "battery": 20000, "speed": 5.0, "start_pos": (40, 70)}
        ]
        
        # Hazır teslimat verisi
        delivery_data = [
            {"id": 1, "pos": (15, 25), "weight": 1.5, "priority": 3, "time_window": ("09:00", "10:00")},
            {"id": 2, "pos": (30, 40), "weight": 2.0, "priority": 5, "time_window": ("09:00", "09:30")},
            {"id": 3, "pos": (70, 80), "weight": 3.0, "priority": 2, "time_window": ("09:20", "10:20")},
            {"id": 4, "pos": (90, 10), "weight": 1.0, "priority": 4, "time_window": ("09:10", "09:40")},
            {"id": 5, "pos": (45, 60), "weight": 4.0, "priority": 1, "time_window": ("09:30", "10:30")},
            {"id": 6, "pos": (25, 15), "weight": 2.5, "priority": 3, "time_window": ("09:00", "09:50")},
            {"id": 7, "pos": (60, 30), "weight": 1.0, "priority": 5, "time_window": ("09:05", "09:25")},
            {"id": 8, "pos": (85, 90), "weight": 3.5, "priority": 2, "time_window": ("09:40", "10:40")},
            {"id": 9, "pos": (10, 80), "weight": 2.0, "priority": 4, "time_window": ("09:15", "09:45")},
            {"id": 10, "pos": (95, 50), "weight": 1.5, "priority": 3, "time_window": ("09:00", "10:00")},
            {"id": 11, "pos": (55, 20), "weight": 0.5, "priority": 5, "time_window": ("09:00", "09:20")},
            {"id": 12, "pos": (35, 75), "weight": 2.0, "priority": 1, "time_window": ("09:50", "11:00")},
            {"id": 13, "pos": (75, 40), "weight": 3.0, "priority": 3, "time_window": ("09:10", "09:50")},
            {"id": 14, "pos": (20, 90), "weight": 1.5, "priority": 4, "time_window": ("09:30", "10:10")},
            {"id": 15, "pos": (65, 65), "weight": 4.5, "priority": 2, "time_window": ("09:25", "10:15")},
            {"id": 16, "pos": (40, 10), "weight": 2.0, "priority": 5, "time_window": ("09:00", "09:30")},
            {"id": 17, "pos": (5, 50), "weight": 1.0, "priority": 3, "time_window": ("09:15", "09:55")},
            {"id": 18, "pos": (50, 85), "weight": 3.0, "priority": 1, "time_window": ("10:00", "11:00")},
            {"id": 19, "pos": (80, 70), "weight": 2.5, "priority": 4, "time_window": ("09:20", "10:00")},
            {"id": 20, "pos": (30, 55), "weight": 1.5, "priority": 2, "time_window": ("09:40", "10:20")}
        ]
        
        # Hazır no-fly zone verisi
        nfz_data = [
            {
                "id": 1,
                "coordinates": [(40, 30), (60, 30), (60, 50), (40, 50)],
                "active_time": ("09:00", "11:00")
            },
            {
                "id": 2,
                "coordinates": [(70, 10), (90, 10), (90, 30), (70, 30)],
                "active_time": ("09:30", "10:30")
            },
            {
                "id": 3,
                "coordinates": [(10, 60), (30, 60), (30, 80), (10, 80)],
                "active_time": ("09:00", "10:00")
            }
        ]
        
        # Drone objelerini oluştur
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
        
        # Delivery objelerini oluştur
        deliveries = []
        for data in delivery_data:
            delivery = DeliveryPoint(
                id=data["id"] - 1,  # 0-indexed
                pos=data["pos"],
                weight=data["weight"],
                priority=data["priority"],
                time_window=data["time_window"]
            )
            deliveries.append(delivery)
        
        # No-fly zone objelerini oluştur
        no_fly_zones = []
        for data in nfz_data:
            nfz = NoFlyZone(
                id=data["id"] - 1,  # 0-indexed
                coordinates=data["coordinates"],
                active_time=data["active_time"]
            )
            no_fly_zones.append(nfz)
        
        print(f"✅ Hazır veri seti yüklendi: {len(drones)} drone, {len(deliveries)} teslimat, {len(no_fly_zones)} yasak bölge")
        
        return {
            'drones': drones,
            'deliveries': deliveries,
            'no_fly_zones': no_fly_zones,
            'scenario_name': 'Predefined Dataset',
            'description': f'{len(drones)} drones, {len(deliveries)} deliveries with real-world constraints'
        }

    @staticmethod
    def generate_test_scenario_2() -> dict:
        """2. Test Senaryosu: 10 drone, 50 teslimat, 5 dinamik no-fly zone"""
        print("🎯 Test Senaryosu 2 oluşturuluyor: 10 drone, 50 teslimat, 5 dinamik no-fly zone")
        
        # 10 drone oluştur
        drones = []
        for i in range(10):
            max_weight = random.uniform(4, 10)
            battery = random.randint(10000, 20000)
            speed = random.uniform(10, 18)
            start_pos = (random.uniform(10, 90), random.uniform(10, 90))
            drones.append(Drone(i, max_weight, battery, speed, start_pos))
        
        # 50 teslimat noktası oluştur
        deliveries = []
        for i in range(50):
            pos = (random.uniform(5, 95), random.uniform(5, 95))
            weight = random.uniform(0.5, 6)
            priority = random.randint(1, 5)
            if random.random() < 0.2:
                priority = 5  # %20 acil teslimat
            hour = random.randint(9, 17)
            time_window = (f"{hour:02d}:00", f"{min(hour+2, 18):02d}:00")
            deliveries.append(DeliveryPoint(i, pos, weight, priority, time_window))
        
        # 5 dinamik no-fly zone oluştur
        no_fly_zones = []
        for i in range(5):
            center_x = random.uniform(15, 85)
            center_y = random.uniform(15, 85)
            radius = random.uniform(8, 20)
            polygon = [(center_x + radius * math.cos(a), center_y + radius * math.sin(a)) 
                       for a in [i * 2 * math.pi / 8 for i in range(8)]]
            
            start_hour = random.randint(9, 15)
            duration = random.randint(1, 4)
            time_window = (f"{start_hour:02d}:00", f"{min(start_hour + duration, 18):02d}:00")
            no_fly_zones.append(NoFlyZone(i, polygon, time_window))
        
        return {
            'drones': drones,
            'deliveries': deliveries,
            'no_fly_zones': no_fly_zones,
            'scenario_name': 'Test Scenario 2',
            'description': '10 drones, 50 deliveries, 5 dynamic no-fly zones'
        }

    @staticmethod
    def generate_mixed_scenario() -> dict:
        """Karma senaryo: Hazır veri + rastgele veri karışımı"""
        print("🔄 Karma senaryo oluşturuluyor...")
        
        # Hazır veriyi yükle
        predefined = DataGenerator.load_predefined_dataset()
        
        # Ek rastgele teslimatlar ekle
        additional_deliveries = []
        for i in range(10):  # 10 ek teslimat
            pos = (random.uniform(0, 100), random.uniform(0, 100))
            weight = random.uniform(0.5, 3.0)
            priority = random.randint(1, 5)
            hour = random.randint(10, 16)
            time_window = (f"{hour:02d}:00", f"{hour+1:02d}:00")
            additional_deliveries.append(DeliveryPoint(
                id=len(predefined['deliveries']) + i,
                pos=pos,
                weight=weight,
                priority=priority,
                time_window=time_window
            ))
        
        # Mevcut teslimatları birleştir
        all_deliveries = predefined['deliveries'] + additional_deliveries
        
        return {
            'drones': predefined['drones'],
            'deliveries': all_deliveries,
            'no_fly_zones': predefined['no_fly_zones'],
            'scenario_name': 'Mixed Scenario',
            'description': f"{len(predefined['drones'])} drones, {len(all_deliveries)} mixed deliveries"
        }