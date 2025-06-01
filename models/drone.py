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
        
        # YENİ EKLENEN ÖZELLİKLER - Şarj süreleri modeli
        self.charge_rate = 50  # Dakika başına batarya dolum oranı
        self.is_charging = False
        self.charge_start_time = None
        self.charging_station_pos = start_pos  # Şarj istasyonu pozisyonu
        self.min_battery_threshold = battery * 0.2  # %20 minimum batarya

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
        self.is_charging = False
        self.charge_start_time = None

    def can_carry(self, weight: float) -> bool:
        return weight <= self.max_weight

    def calculate_energy_consumption(self, distance: float, weight: float) -> float:
        base_consumption = 10
        weight_factor = 5
        return distance * (base_consumption + weight_factor * weight)

    def needs_charging(self) -> bool:
        """Şarj gereksinimi kontrolü - EKSİK OLAN ÖZELLIK"""
        return self.battery <= self.min_battery_threshold

    def calculate_charging_time(self, target_battery: int = None) -> int:
        """Şarj süresi hesaplama - EKSİK OLAN ÖZELLIK"""
        if target_battery is None:
            target_battery = self.initial_battery
        
        battery_needed = target_battery - self.battery
        charging_time_minutes = max(0, battery_needed / self.charge_rate)
        return int(charging_time_minutes)

    def start_charging(self):
        """Şarj başlat - EKSİK OLAN ÖZELLIK"""
        if not self.is_charging:
            self.is_charging = True
            self.charge_start_time = self.current_time
            # Şarj istasyonuna git
            if self.current_pos != self.charging_station_pos:
                travel_distance = calculate_distance(self.current_pos, self.charging_station_pos)
                travel_time = (travel_distance / self.speed) * 60  # Dakika
                self.current_time += timedelta(minutes=travel_time)
                self.current_pos = self.charging_station_pos

    def complete_charging(self, target_battery: int = None):
        """Şarjı tamamla - EKSİK OLAN ÖZELLIK"""
        if self.is_charging and self.charge_start_time:
            if target_battery is None:
                target_battery = self.initial_battery
            
            charging_time = self.calculate_charging_time(target_battery)
            self.current_time += timedelta(minutes=charging_time)
            self.available_time = self.current_time
            self.battery = target_battery
            self.is_charging = False
            self.charge_start_time = None

    def can_complete_route_with_charging(self, route_deliveries: List, no_fly_zones: List) -> bool:
        """Şarj ile rotayı tamamlayabilir mi - EKSİK OLAN ÖZELLIK"""
        temp_battery = self.battery
        temp_pos = self.current_pos
        
        for delivery in route_deliveries:
            distance = calculate_distance(temp_pos, delivery.pos)
            energy_needed = self.calculate_energy_consumption(distance, delivery.weight)
            
            # Batarya yeterli değilse şarj et
            if temp_battery < energy_needed:
                # Şarj istasyonuna dön ve şarj et
                temp_battery = self.initial_battery
            
            temp_battery -= energy_needed
            temp_pos = delivery.pos
            
            if temp_battery < 0:  # Şarj etse bile yeterli değil
                return False
        
        return True

    def can_reach(self, dest_pos: Tuple[float, float], weight: float, no_fly_zones: List) -> bool:
        from models.no_fly_zone import NoFlyZone
        path_distance = calculate_distance(self.current_pos, dest_pos)
        energy_needed = self.calculate_energy_consumption(path_distance, weight)
        current_time_str = self.current_time.strftime("%H:%M")
        
        # No-fly zone kontrolü
        for nfz in no_fly_zones:
            if nfz.is_active(current_time_str) and nfz.does_path_intersect(self.current_pos, dest_pos):
                return False
        
        # Batarya kontrolü (şarj seçeneği ile)
        if energy_needed <= self.battery:
            return True
        elif energy_needed <= self.initial_battery:
            # Şarj ederek ulaşabilir
            return True
        else:
            return False

    def move_to(self, dest_pos: Tuple[float, float], weight: float, force_charge: bool = False) -> bool:
        path_distance = calculate_distance(self.current_pos, dest_pos)
        energy = self.calculate_energy_consumption(path_distance, weight)
        
        # Şarj gereksinimi kontrolü
        if energy > self.battery or force_charge:
            if self.needs_charging() or force_charge:
                print(f"🔋 Drone {self.id} şarj oluyor...")
                self.start_charging()
                self.complete_charging()
        
        # Hareket et
        if energy > self.battery:
            return False
            
        self.current_pos = dest_pos
        self.battery -= energy
        self.energy_consumed += energy
        self.total_distance += path_distance
        travel_time_minutes = (path_distance / self.speed) * 60  # Saatte km -> dakikaya çevir
        self.current_time += timedelta(minutes=travel_time_minutes + 2)  # +2 dk teslimat süresi
        self.available_time = self.current_time
        return True

    def add_to_route(self, delivery_point_id: int):
        self.current_route.append(delivery_point_id)

    def complete_delivery(self):
        self.deliveries_completed += 1

    def get_efficiency_metrics(self) -> dict:
        """Drone verimlilik metrikleri - EKSİK OLAN ÖZELLIK"""
        return {
            'energy_efficiency': self.deliveries_completed / max(self.energy_consumed, 1),
            'distance_efficiency': self.deliveries_completed / max(self.total_distance, 1),
            'battery_usage_rate': (self.initial_battery - self.battery) / self.initial_battery,
            'violations_rate': self.rule_violations / max(self.deliveries_completed, 1)
        }
