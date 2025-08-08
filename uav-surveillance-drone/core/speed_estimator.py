"""
Speed Estimator Module
Author: Group 4A
Purpose: Estimate vehicle speed across frames using basic frame displacement
"""

import time
from collections import defaultdict

class SpeedEstimator:
    def __init__(self, pixel_to_meter_ratio=0.05, fps=30):
        self.tracked_positions = defaultdict(list)  # {object_id: [(timestamp, x_center)]}
        self.pixel_to_meter_ratio = pixel_to_meter_ratio  # rough scale conversion
        self.fps = fps  # camera frame rate

    def update_position(self, object_id, x_center):
        timestamp = time.time()
        self.tracked_positions[object_id].append((timestamp, x_center))

        # Keep only latest two positions
        if len(self.tracked_positions[object_id]) > 2:
            self.tracked_positions[object_id].pop(0)

    def get_speed(self, object_id):
        if len(self.tracked_positions[object_id]) < 2:
            return None

        (t1, x1), (t2, x2) = self.tracked_positions[object_id]
        delta_time = t2 - t1
        delta_dist = abs(x2 - x1) * self.pixel_to_meter_ratio

        # speed = distance / time, convert to km/h
        speed = (delta_dist / delta_time) * 3.6 if delta_time > 0 else 0
        return round(speed, 2)

if __name__ == "__main__":
    tracker = SpeedEstimator()
    tracker.update_position("car1", 230)
    time.sleep(0.2)
    tracker.update_position("car1", 280)
    print(f"Estimated speed: {tracker.get_speed('car1')} km/h")
