import heapq
from typing import Tuple, List
from utils.time_utils import is_time_in_range

class DeliveryPoint:
    def __init__(self, id: int, pos: Tuple[float, float], weight: float, priority: int, time_window: Tuple[str, str]):
        self.id = id
        self.pos = pos
        self.weight = weight
        self.priority = priority  # 1: düşük, 5: yüksek (5 = ACİL)
        self.time_window = time_window
        self.delivered = False
        self.assigned_to = None
        self.delivery_time = None
        self.is_urgent = priority >= 4  # Acil teslimat kontrolü - YENİ EKLENEN

    def reset(self):
        self.delivered = False
        self.assigned_to = None
        self.delivery_time = None

    def is_in_time_window(self, current_time_str: str) -> bool:
        return is_time_in_range(current_time_str, self.time_window)
    
    def __lt__(self, other):
        """Min-Heap için karşılaştırma (yüksek öncelik = düşük sayı)"""
        return self.priority > other.priority  # Tersine çevir (5 > 1)

class UrgentDeliveryQueue:
    """Acil teslimatlar için Min-Heap öncelik kuyruğu - EKSİK OLAN ÖZELLIK"""
    
    def __init__(self):
        self.heap = []
        self.urgent_deliveries = set()
    
    def add_urgent_delivery(self, delivery: DeliveryPoint):
        """Acil teslimat ekle"""
        if delivery.is_urgent and delivery.id not in self.urgent_deliveries:
            heapq.heappush(self.heap, delivery)
            self.urgent_deliveries.add(delivery.id)
    
    def get_next_urgent(self) -> DeliveryPoint:
        """Bir sonraki acil teslimatı al"""
        if self.heap:
            delivery = heapq.heappop(self.heap)
            self.urgent_deliveries.remove(delivery.id)
            return delivery
        return None
    
    def has_urgent_deliveries(self) -> bool:
        """Acil teslimat var mı kontrolü"""
        return len(self.heap) > 0
    
    def get_urgent_count(self) -> int:
        """Acil teslimat sayısı"""
        return len(self.heap)