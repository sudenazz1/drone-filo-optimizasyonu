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
