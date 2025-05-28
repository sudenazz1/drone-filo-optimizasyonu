import heapq
from typing import Tuple, Dict, List, Optional
from utils.geometry import calculate_distance

class Node:
    def __init__(self, position: Tuple[float, float], g: float = 0.0, h: float = 0.0, parent: Optional['Node'] = None):
        self.position = position
        self.g = g  # Start'tan bu node'a maliyet
        self.h = h  # Heuristic
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

    def find_path(self, start: Tuple[float, float], goal: Tuple[float, float], current_time: str) -> Optional[List[Tuple[float, float]]]:
        open_set = []
        heapq.heappush(open_set, Node(start, 0.0, calculate_distance(start, goal)))

        closed_set = set()

        while open_set:
            current_node = heapq.heappop(open_set)
            if calculate_distance(current_node.position, goal) < 1.0:
                return self.reconstruct_path(current_node)

            closed_set.add(current_node.position)

            # Basit 8 komşuluk
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx == 0 and dy == 0:
                        continue
                    neighbor_pos = (current_node.position[0] + dx, current_node.position[1] + dy)
                    if neighbor_pos in closed_set:
                        continue
                    if not self.is_valid_path(current_node.position, neighbor_pos, current_time):
                        continue
                    g = current_node.g + calculate_distance(current_node.position, neighbor_pos)
                    h = calculate_distance(neighbor_pos, goal)
                    neighbor_node = Node(neighbor_pos, g, h, current_node)
                    heapq.heappush(open_set, neighbor_node)

        return None
