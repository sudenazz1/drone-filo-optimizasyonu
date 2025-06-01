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

    def find_path(self, start: Tuple[float, float], goal: Tuple[float, float], current_time: str) -> Optional[List[Tuple[float, float]]]:
        open_set = []
        heapq.heappush(open_set, Node(start, 0.0, calculate_distance(start, goal)))
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

                    neighbor_pos = (round(current_node.position[0] + dx, 5), round(current_node.position[1] + dy, 5))

                    if neighbor_pos in closed_set:
                        continue
                    if not self.is_within_bounds(neighbor_pos):
                        continue
                    if not self.is_valid_path(current_node.position, neighbor_pos, current_time):
                        continue

                    g = current_node.g + calculate_distance(current_node.position, neighbor_pos)
                    h = calculate_distance(neighbor_pos, goal)
                    neighbor_node = Node(neighbor_pos, g, h, current_node)
                    heapq.heappush(open_set, neighbor_node)

        return None
