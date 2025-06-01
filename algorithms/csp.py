from typing import List, Dict, Set
from utils.geometry import calculate_distance
from models.drone import Drone
from models.delivery_point import DeliveryPoint

class CSPConstraints:
    """CSP kısıtlarının net tanımı - EKSİK OLAN ÖZELLIK"""
    
    @staticmethod
    def single_package_constraint(drone: Drone, delivery: DeliveryPoint) -> bool:
        """Tek paket taşıma kısıtı"""
        return drone.can_carry(delivery.weight)
    
    @staticmethod
    def no_fly_zone_constraint(start_pos, end_pos, no_fly_zones, current_time: str) -> bool:
        """No-fly zone ihlali kontrolü"""
        for nfz in no_fly_zones:
            if nfz.is_active(current_time) and nfz.does_path_intersect(start_pos, end_pos):
                return False
        return True
    
    @staticmethod
    def time_window_constraint(delivery: DeliveryPoint, current_time: str) -> bool:
        """Zaman penceresi kısıtı"""
        return delivery.is_in_time_window(current_time)
    
    @staticmethod
    def battery_constraint(drone: Drone, delivery: DeliveryPoint) -> bool:
        """Batarya kısıtı"""
        return drone.can_reach(delivery.pos, delivery.weight, [])

class CSPVariables:
    """CSP değişkenlerinin net tanımı - EKSİK OLAN ÖZELLIK"""
    
    def __init__(self, drones: List[Drone], deliveries: List[DeliveryPoint]):
        self.drones = {drone.id: drone for drone in drones}
        self.deliveries = {delivery.id: delivery for delivery in deliveries}
        self.assignments = {}  # drone_id -> [delivery_ids]
        self.domains = self._calculate_domains()
    
    def _calculate_domains(self) -> Dict:
        """Her drone için mümkün teslimat domainleri hesapla"""
        domains = {}
        for drone_id, drone in self.drones.items():
            domains[drone_id] = []
            for delivery_id, delivery in self.deliveries.items():
                if CSPConstraints.single_package_constraint(drone, delivery):
                    domains[drone_id].append(delivery_id)
        return domains

class CSP:
    def __init__(self, drones: List[Drone], deliveries: List[DeliveryPoint]):
        self.drones = drones
        self.deliveries = deliveries
        self.variables = CSPVariables(drones, deliveries)
        self.constraints = CSPConstraints()

    def assign_deliveries(self, no_fly_zones: List = None):
        """Kısıtlarla teslimat ataması - İYİLEŞTİRİLMİŞ"""
        if not no_fly_zones:
            no_fly_zones = []
            
        assignments = {}
        unassigned_deliveries = set(d.id for d in self.deliveries)
        
        # Öncelik sırası ile teslimatları işle
        sorted_deliveries = sorted(self.deliveries, key=lambda d: -d.priority)
        
        for delivery in sorted_deliveries:
            if delivery.id not in unassigned_deliveries:
                continue
                
            best_drone = None
            min_cost = float('inf')
            
            for drone in self.drones:
                current_time = drone.current_time.strftime("%H:%M")
                
                # Tüm kısıtları kontrol et
                if not self.constraints.single_package_constraint(drone, delivery):
                    continue
                if not self.constraints.time_window_constraint(delivery, current_time):
                    continue
                if not self.constraints.battery_constraint(drone, delivery):
                    continue
                if not self.constraints.no_fly_zone_constraint(
                    drone.current_pos, delivery.pos, no_fly_zones, current_time):
                    continue
                
                # Maliyet hesapla
                distance = calculate_distance(drone.current_pos, delivery.pos)
                cost = distance + (delivery.weight * 10)  # Ağırlık maliyeti
                
                if cost < min_cost:
                    min_cost = cost
                    best_drone = drone
            
            # Atama yap
            if best_drone:
                if best_drone.id not in assignments:
                    assignments[best_drone.id] = []
                assignments[best_drone.id].append(delivery.id)
                unassigned_deliveries.remove(delivery.id)
                
                # Drone durumunu güncelle
                success = best_drone.move_to(delivery.pos, delivery.weight)
                if success:
                    delivery.delivered = True
                    delivery.assigned_to = best_drone.id
                    delivery.delivery_time = best_drone.current_time.strftime("%H:%M")
                    best_drone.complete_delivery()
                    best_drone.add_to_route(delivery.id)
        
        return assignments

class CSPSolver:
    def solve(self, drones, deliveries, no_fly_zones):
        """Gelişmiş CSP çözücü"""
        csp = CSP(drones, deliveries)
        return csp.assign_deliveries(no_fly_zones)