"""
test_runner.py
Purpose: Modular test runner to validate all core components before flight.
"""

import traceback
import time

from core.camera_stream import CameraStream
from core.object_detector import ObjectDetector
from core.ocr_plate_reader import OCRPlateReader
from core.speed_estimator import SpeedEstimator
from core.gesture_detector import GestureDetector
from core.alert_system import AlertSystem
from core.navigation import NavigationController
from core.diagnostics import Diagnostics
from core.manual_control import manual_control_mode
from core.debug_logger import DebugLogger
from config import Config

logger = DebugLogger()
config = Config()

def run_test(name, func):
    print(f"[TEST] Running {name}...")
    try:
        result = func()
        print(f"[PASS] {name}")
        return True
    except Exception as e:
        print(f"[FAIL] {name} - {e}")
        traceback.print_exc()
        return False

def test_camera_stream():
    cam = CameraStream().start()
    time.sleep(2)
    frame = cam.read()
    cam.stop()
    assert frame is not None, "No frame captured"
    return True

def test_object_detector():
    detector = ObjectDetector()
    dummy_frame = config.get_dummy_frame()
    detections = detector.detect(dummy_frame)
    assert isinstance(detections, list), "Detection result is not a list"
    return True

def test_plate_reader():
    reader = OCRPlateReader()
    dummy_frame = config.get_dummy_frame()
    result = reader.read_plate(dummy_frame, (0, 0, 100, 50))  # fake bbox
    assert isinstance(result, str) or result is None, "Invalid plate result"
    return True

def test_speed_estimator():
    estimator = SpeedEstimator(pixel_to_meter_ratio=10, fps=30)
    estimator.update_position("test", 10)
    time.sleep(0.1)
    estimator.update_position("test", 20)
    speed = estimator.get_speed("test")
    assert isinstance(speed, float), "Speed is not float"
    return True

def test_gesture_detector():
    detector = GestureDetector()
    dummy_frame = config.get_dummy_frame()
    gestures = detector.detect_gesture(dummy_frame)
    assert isinstance(gestures, list), "Gestures not a list"
    return True

def test_alert_system():
    alert = AlertSystem()
    alert.trigger_alert("test event")
    return True

def test_navigation():
    nav = NavigationController()
    nav.respond_to_event("overspeeding", (100, 100, 200, 200))
    return True

def test_diagnostics():
    diag = Diagnostics()
    status, report = diag.full_diagnostic()
    assert isinstance(report, dict), "Diagnostics report not a dict"
    return True

def test_manual_control():
    # Skip actual RC interaction in test environment.
    print("[INFO] Manual control simulation skipped in test mode.")
    return True

def run_all_tests():
    logger.info("[TEST_RUNNER] Starting all system tests...")

    test_cases = [
        ("Camera Stream", test_camera_stream),
        ("Object Detector", test_object_detector),
        ("OCR Plate Reader", test_plate_reader),
        ("Speed Estimator", test_speed_estimator),
        ("Gesture Detector", test_gesture_detector),
        ("Alert System", test_alert_system),
        ("Navigation Controller", test_navigation),
        ("Diagnostics", test_diagnostics),
        ("Manual Control", test_manual_control),
    ]

    passed = 0
    for name, test_func in test_cases:
        if run_test(name, test_func):
            passed += 1

    total = len(test_cases)
    print(f"\n[SUMMARY] Passed {passed} / {total} tests")
    logger.info(f"[TEST_RUNNER] Completed. Passed {passed}/{total}")

if __name__ == "__main__":
    run_all_tests()
