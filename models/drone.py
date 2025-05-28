from datetime import datetime, timedelta
from typing import Tuple, List
from utils.geometry import calculate_distance
from utils.time_utils import is_time_in_range

class Drone:
    def __init__(self, id: int, max_weight: float, battery: int, speed: float, start_pos: Tuple[float, float]):
        self.id = id
        self.max_weight = max_weight
        self.battery = battery
        self.initial_battery = battery
        self.speed = speed
        self.start_pos = start_pos
        self.current_pos = start_pos
        self.current_time = datetime.strptime("09:00", "%H:%M")
        self.available_time = self.current_time
        self.energy_consumed = 0
        self.deliveries_completed = 0
        self.current_route = []
        self.total_distance = 0
        self.rule_violations = 0

    def reset(self):
        self.current_pos = self.start_pos
        self.current_time = datetime.strptime("09:00", "%H:%M")
        self.available_time = self.current_time
        self.battery = self.initial_battery
        self.energy_consumed = 0
        self.deliveries_completed = 0
        self.current_route = []
        self.total_distance = 0
        self.rule_violations = 0

    def can_carry(self, weight: float) -> bool:
        return weight <= self.max_weight

    def calculate_energy_consumption(self, distance: float, weight: float) -> float:
        base_consumption = 10
        weight_factor = 5
        return distance * (base_consumption + weight_factor * weight)

    def can_reach(self, dest_pos: Tuple[float, float], weight: float, no_fly_zones: List) -> bool:
        from models.no_fly_zone import NoFlyZone
        path_distance = calculate_distance(self.current_pos, dest_pos)
        energy_needed = self.calculate_energy_consumption(path_distance, weight)
        current_time_str = self.current_time.strftime("%H:%M")
        for nfz in no_fly_zones:
            if nfz.is_active(current_time_str) and nfz.does_path_intersect(self.current_pos, dest_pos):
                return False
        return energy_needed <= self.battery

    def move_to(self, dest_pos: Tuple[float, float], weight: float) -> bool:
        path_distance = calculate_distance(self.current_pos, dest_pos)
        energy = self.calculate_energy_consumption(path_distance, weight)
        if energy > self.battery:
            return False
        self.current_pos = dest_pos
        self.battery -= energy
        self.energy_consumed += energy
        self.total_distance += path_distance
        travel_time_minutes = (path_distance / self.speed) / 60
        self.current_time += timedelta(minutes=travel_time_minutes + 2)
        self.available_time = self.current_time
        return True

    def add_to_route(self, delivery_point_id: int):
        self.current_route.append(delivery_point_id)

    def complete_delivery(self):
        self.deliveries_completed += 1
