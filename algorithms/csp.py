from typing import List
from models.drone import Drone
from models.delivery_point import DeliveryPoint

class CSP:
    def __init__(self, drones: List[Drone], deliveries: List[DeliveryPoint]):
        self.drones = drones
        self.deliveries = deliveries

    def assign_deliveries(self):
        for delivery in sorted(self.deliveries, key=lambda d: -d.priority):
            for drone in self.drones:
                if drone.can_carry(delivery.weight) and delivery.is_in_time_window(drone.current_time.strftime("%H:%M")):
                    if drone.can_reach(delivery.pos, delivery.weight, []):  # No-fly zones CSP'de opsiyonel
                        success = drone.move_to(delivery.pos, delivery.weight)
                        if success:
                            delivery.delivered = True
                            delivery.assigned_to = drone.id
                            delivery.delivery_time = drone.current_time.strftime("%H:%M")
                            drone.complete_delivery()
                            drone.add_to_route(delivery.id)
                            break
class CSPSolver:
    def solve(self, drones, deliveries, no_fly_zones):
        assignments = {}
        delivery_index = 0

        for drone in drones:
            drone_deliveries = []
            for _ in range(len(deliveries) // len(drones)):
                if delivery_index < len(deliveries):
                    drone_deliveries.append(deliveries[delivery_index])
                    delivery_index += 1
            assignments[drone.id] = drone_deliveries

        return assignments
