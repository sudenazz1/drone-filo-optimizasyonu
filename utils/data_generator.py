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
    def generate_test_scenario_2() -> dict:
        """2. Test Senaryosu: 10 drone, 50 teslimat, 5 dinamik no-fly zone - EKSİK OLAN ÖZELLIK"""
        print("🎯 Test Senaryosu 2 oluşturuluyor: 10 drone, 50 teslimat, 5 dinamik no-fly zone")
        
        # 10 drone oluştur
        drones = []
        for i in range(10):
            max_weight = random.uniform(4, 10)  # Daha yüksek kapasite
            battery = random.randint(10000, 20000)  # Daha yüksek batarya
            speed = random.uniform(10, 18)
            start_pos = (random.uniform(10, 90), random.uniform(10, 90))
            drones.append(Drone(i, max_weight, battery, speed, start_pos))
        
        # 50 teslimat noktası oluştur
        deliveries = []
        for i in range(50):
            pos = (random.uniform(5, 95), random.uniform(5, 95))
            weight = random.uniform(0.5, 6)
            priority = random.randint(1, 5)
            # Acil teslimatlar için %20 olasılık
            if random.random() < 0.2:
                priority = 5  # Acil
            hour = random.randint(9, 17)
            time_window = (f"{hour:02d}:00", f"{min(hour+2, 18):02d}:00")
            deliveries.append(DeliveryPoint(i, pos, weight, priority, time_window))
        
        # 5 dinamik no-fly zone oluştur
        no_fly_zones = []
        for i in range(5):
            center_x = random.uniform(15, 85)
            center_y = random.uniform(15, 85)
            radius = random.uniform(8, 20)
            # Daha karmaşık poligonlar (8 köşeli)
            polygon = [(center_x + radius * math.cos(a), center_y + radius * math.sin(a)) 
                       for a in [i * 2 * math.pi / 8 for i in range(8)]]
            
            # Dinamik zaman aralıkları
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