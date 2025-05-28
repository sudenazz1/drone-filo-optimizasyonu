from datetime import datetime
from typing import Tuple

def is_time_in_range(time_str: str, time_range: Tuple[str, str]) -> bool:
    start_time = datetime.strptime(time_range[0], "%H:%M")
    end_time = datetime.strptime(time_range[1], "%H:%M")
    check_time = datetime.strptime(time_str, "%H:%M")
    return start_time <= check_time <= end_time
