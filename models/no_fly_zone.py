from typing import List, Tuple
from utils.time_utils import is_time_in_range
from utils.geometry import point_in_polygon, does_path_intersect_polygon

class NoFlyZone:
    def __init__(self, id: int, coordinates: List[Tuple[float, float]], active_time: Tuple[str, str]):
        self.id = id
        self.coordinates = coordinates
        self.active_time = active_time

    def is_active(self, current_time_str: str) -> bool:
        return is_time_in_range(current_time_str, self.active_time)

    def is_point_inside(self, point: Tuple[float, float]) -> bool:
        return point_in_polygon(point, self.coordinates)

    def does_path_intersect(self, start: Tuple[float, float], end: Tuple[float, float]) -> bool:
        return does_path_intersect_polygon(start, end, self.coordinates)
