from typing import Tuple
from utils.time_utils import is_time_in_range

class DeliveryPoint:
    def __init__(self, id: int, pos: Tuple[float, float], weight: float, priority: int, time_window: Tuple[str, str]):
        self.id = id
        self.pos = pos
        self.weight = weight
        self.priority = priority  # 1: düşük, 5: yüksek
        self.time_window = time_window
        self.delivered = False
        self.assigned_to = None
        self.delivery_time = None

    def reset(self):
        self.delivered = False
        self.assigned_to = None
        self.delivery_time = None

    def is_in_time_window(self, current_time_str: str) -> bool:
        return is_time_in_range(current_time_str, self.time_window)
