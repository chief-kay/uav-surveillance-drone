"""
Main program for running the drone's AI detection pipeline.
Integrates video stream with object detection, alert system, speed tracking, plate reader, navigation and logging.
"""

from Core.camera_stream import CameraStream
from Core.object_detector import ObjectDetector
from Core.alert_system import AlertSystem
from Core.ocr_plate_reader import OCRPlateReader
from Core.speed_estimator import SpeedEstimator
from Core.gesture_detector import GestureDetector
from Core.navigation import NavigationController
from Core.logger import EventLogger
from Core import config

import cv2


def main():
    print("[SYSTEM] Initializing UAV Surveillance Drone...")

    camera = CameraStream().start()
    detector = ObjectDetector()
    alert = AlertSystem()
    plate_reader = OCRPlateReader()
    speed_tracker = SpeedEstimator(
        pixel_to_meter_ratio=config.CONFIG["PIXEL_TO_METER_RATIO"],
        fps=config.CONFIG["CAMERA_FPS"]
    )
    gesture = GestureDetector()
    navigator = NavigationController()
    logger = EventLogger(
        csv_path=config.CONFIG["LOG_CSV_PATH"],
        json_path=config.CONFIG["LOG_JSON_PATH"]
    )

    print("[SYSTEM] Drone surveillance active.")

    while True:
        frame = camera.read()
        if frame is None:
            continue

        detections = detector.detect(frame)

        for d in detections:
            object_id = d.get("id", d.get("label", "unknown"))
            bbox = d["bbox"]
            label = d["label"]

            speed_tracker.update_position(object_id, (bbox[0] + bbox[2]) // 2)
            d["speed"] = speed_tracker.get_speed(object_id)

            # Simulated violations
            if d.get("speed", 0) and d["speed"] > config.CONFIG["SPEED_LIMIT_KMPH"]:
                d["event"] = "overspeeding"
                d["requires_action"] = True

            if label.lower() == "car":
                plate = plate_reader.read_plate(frame, bbox)
                if plate:
                    d["plate"] = plate

            gestures = gesture.detect_gesture(frame)
            if gestures:
                for g in gestures:
                    if g["confidence"] > config.CONFIG["GESTURE_CONFIDENCE_THRESHOLD"]:
                        d["event"] = g["gesture"]
                        d["requires_action"] = True

            if d.get("requires_action"):
                alert.trigger_alert(d["event"])
                navigator.respond_to_event(d["event"], bbox)
                logger.log_event(d)

            x1, y1, x2, y2 = bbox
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
            cv2.putText(frame, d["label"], (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

        cv2.imshow("Drone Surveillance Feed", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    camera.stop()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()


"""
main.py
Author: Group 4A
Purpose: Hybrid control system for UAV — supports autonomous and manual flight modes.
"""

import time
from core.diagnostics import Diagnostics
from core.mode_switcher import ModeSwitcher
from core.manual_control import manual_control_mode
from core.navigation import autonomous_navigation
from core.debug_logger import DebugLogger
from core.config import Config

logger = DebugLogger()
config = Config()

BATTERY_CRITICAL_THRESHOLD = 25  # % battery level for return-to-base

def start_mission():
    logger.info("[SYSTEM] UAV boot sequence started.")

    diagnostics = Diagnostics()
    passed, report = diagnostics.full_diagnostic()

    if not passed:
        logger.warning("[SYSTEM] Diagnostics not fully passed.")
        
        # Evaluate if takeoff can proceed without network
        critical = report.get("Battery", 0) < 40 or not report.get("Camera")
        if critical:
            logger.error("[SYSTEM] Critical systems failed. Aborting.")
            return
        else:
            logger.warning("[SYSTEM] Non-critical systems failed (e.g., network). Continuing...")

    logger.info("[SYSTEM] Diagnostics passed or partially accepted. Proceeding to mode selection.")

    mode_switcher = ModeSwitcher()
    mode = mode_switcher.get_mode()
    logger.info(f"[MODE] Selected: {mode}")

    try:
        if mode == "manual":
            logger.info("[MODE] Engaging Manual Control Mode.")
            manual_control_mode()

        elif mode == "autonomous":
            logger.info("[MODE] Engaging Autonomous Navigation Mode.")
            autonomous_navigation()

        else:
            logger.warning(f"[MODE] Unknown mode '{mode}', defaulting to Manual.")
            manual_control_mode()

    except KeyboardInterrupt:
        logger.warning("[SYSTEM] Mission interrupted by user.")

    except Exception as e:
        logger.exception(f"[SYSTEM] Unexpected error: {str(e)}")

    finally:
        logger.info("[SYSTEM] UAV shutdown sequence complete.")

if __name__ == "__main__":
    start_mission()
