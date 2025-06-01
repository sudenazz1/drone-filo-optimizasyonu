from typing import List, Dict
from models.drone import Drone
from models.delivery_point import DeliveryPoint

class PerformanceMetrics:
    """Performans metrikleri hesaplama - EKSİK OLAN ÖZELLIK"""
    
    @staticmethod
    def calculate_average_energy_consumption(drones: List[Drone]) -> float:
        """Ortalama enerji tüketimi hesapla - EKSİK OLAN METRIK"""
        if not drones:
            return 0.0
        
        total_energy = sum(drone.energy_consumed for drone in drones)
        return total_energy / len(drones)
    
    @staticmethod
    def calculate_completion_rate(deliveries: List[DeliveryPoint]) -> float:
        """Tamamlanan teslimat yüzdesi"""
        if not deliveries:
            return 0.0
        
        completed = sum(1 for delivery in deliveries if delivery.delivered)
        return (completed / len(deliveries)) * 100
    
    @staticmethod
    def calculate_efficiency_metrics(drones: List[Drone], deliveries: List[DeliveryPoint]) -> Dict:
        """Detaylı verimlilik metrikleri"""
        total_distance = sum(drone.total_distance for drone in drones)
        total_energy = sum(drone.energy_consumed for drone in drones)
        total_completed = sum(drone.deliveries_completed for drone in drones)
        total_violations = sum(drone.rule_violations for drone in drones)
        
        return {
            'average_energy_per_delivery': total_energy / max(total_completed, 1),
            'average_distance_per_delivery': total_distance / max(total_completed, 1),
            'energy_efficiency_ratio': total_completed / max(total_energy, 1),
            'violation_rate': total_violations / max(total_completed, 1),
            'completion_rate': PerformanceMetrics.calculate_completion_rate(deliveries),
            'average_energy_consumption': PerformanceMetrics.calculate_average_energy_consumption(drones)
        }