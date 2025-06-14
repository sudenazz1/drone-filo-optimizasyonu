# algorithms/a_star.py - GÜNCELLENMİŞ
import heapq
from typing import Tuple, Dict, List, Optional
from utils.geometry import calculate_distance

# Türkiye koordinat sınırları
LAT_MIN, LAT_MAX = 36.0, 42.0  # Enlem
LON_MIN, LON_MAX = 26.0, 45.0  # Boylam

class Node:
    def __init__(self, position: Tuple[float, float], g: float = 0.0, h: float = 0.0, parent: Optional['Node'] = None):
        self.position = position
        self.g = g  # Başlangıçtan buraya maliyet
        self.h = h  # Heuristic (tahmini kalan)
        self.f = g + h
        self.parent = parent

    def __lt__(self, other: 'Node'):
        return self.f < other.f

class AStar:
    def __init__(self, no_fly_zones: List):
        self.no_fly_zones = no_fly_zones
        # Adjacency list (komşuluk listesi) - EKLENEN ÖZELLİK
        self.adjacency_list = {}

    def build_adjacency_list(self, nodes: List[Tuple[float, float]]):
        """Graf için komşuluk listesi oluştur - EKSİK OLAN ÖZELLIK"""
        self.adjacency_list = {}
        for node in nodes:
            self.adjacency_list[node] = []
            
        for i, node1 in enumerate(nodes):
            for j, node2 in enumerate(nodes):
                if i != j:
                    distance = calculate_distance(node1, node2)
                    if distance <= 5.0:  # Komşuluk eşiği
                        weight = self.calculate_edge_weight(node1, node2, distance)
                        self.adjacency_list[node1].append((node2, weight))

    def calculate_edge_weight(self, start: Tuple[float, float], end: Tuple[float, float], distance: float) -> float:
        """Kenar ağırlığı hesaplama - EKSİK OLAN FORMULA"""
        # 1. Uzaklık × ağırlık faktörü
        distance_weight = distance * 1.5
        
        # 2. Enerji tüketimi × 100
        energy_consumption = (distance * 0.1) * 100  # Basit enerji modeli
        
        # 3. No-fly zone cezası
        nfz_penalty = 0
        for nfz in self.no_fly_zones:
            if nfz.does_path_intersect(start, end):
                nfz_penalty += 500  # Büyük ceza
        
        # Toplam ağırlık
        total_weight = distance_weight + energy_consumption + nfz_penalty
        return total_weight

    def improved_heuristic(self, current: Tuple[float, float], goal: Tuple[float, float], current_time: str) -> float:
        """İyileştirilmiş heuristic fonksiyonu - EKSİK OLAN ÖZELLIK"""
        # Temel mesafe
        base_distance = calculate_distance(current, goal)
        
        # No-fly zone cezası ekleme  
        nfz_penalty = 0
        for nfz in self.no_fly_zones:
            if nfz.is_active(current_time) and nfz.does_path_intersect(current, goal):
                nfz_penalty += 200  # Heuristic için ceza
        
        return base_distance + nfz_penalty

    def check_drone_capacity(self, drone, delivery_weight: float) -> bool:
        """Drone kapasitesi kontrolü - EKSİK OLAN ÖZELLIK"""
        return drone.can_carry(delivery_weight)

    def reconstruct_path(self, node: Node) -> List[Tuple[float, float]]:
        path = []
        current = node
        while current is not None:
            path.append(current.position)
            current = current.parent
        return path[::-1]

    def is_valid_path(self, start: Tuple[float, float], end: Tuple[float, float], current_time: str) -> bool:
        for nfz in self.no_fly_zones:
            if nfz.is_active(current_time) and nfz.does_path_intersect(start, end):
                return False
        return True

    def is_within_bounds(self, position: Tuple[float, float]) -> bool:
        lat, lon = position
        return LAT_MIN <= lat <= LAT_MAX and LON_MIN <= lon <= LON_MAX

    def find_path(self, start: Tuple[float, float], goal: Tuple[float, float], 
                  current_time: str, drone=None, delivery_weight: float = 0) -> Optional[List[Tuple[float, float]]]:
        """İyileştirilmiş A* algoritması"""
        
        # Drone kapasitesi kontrolü - YENİ EKLENEN
        if drone and not self.check_drone_capacity(drone, delivery_weight):
            print(f"❌ Drone {drone.id} kapasitesi aşıldı: {delivery_weight} > {drone.max_weight}")
            return None
        
        open_set = []
        # İyileştirilmiş heuristic kullan
        initial_h = self.improved_heuristic(start, goal, current_time)
        heapq.heappush(open_set, Node(start, 0.0, initial_h))
        closed_set = set()

        while open_set:
            current_node = heapq.heappop(open_set)

            if calculate_distance(current_node.position, goal) <= 0.5:
                return self.reconstruct_path(current_node)

            closed_set.add(current_node.position)

            for dx in [-0.01, 0, 0.01]:
                for dy in [-0.01, 0, 0.01]:
                    if dx == 0 and dy == 0:
                        continue

                    neighbor_pos = (round(current_node.position[0] + dx, 5), 
                                  round(current_node.position[1] + dy, 5))

                    if neighbor_pos in closed_set:
                        continue
                    if not self.is_within_bounds(neighbor_pos):
                        continue
                    if not self.is_valid_path(current_node.position, neighbor_pos, current_time):
                        continue

                    # İyileştirilmiş maliyet hesabı
                    edge_weight = self.calculate_edge_weight(current_node.position, neighbor_pos, 
                                                          calculate_distance(current_node.position, neighbor_pos))
                    g = current_node.g + edge_weight
                    h = self.improved_heuristic(neighbor_pos, goal, current_time)
                    
                    neighbor_node = Node(neighbor_pos, g, h, current_node)
                    heapq.heappush(open_set, neighbor_node)

        return None