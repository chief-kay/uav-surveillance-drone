"""
camera_stream.py
Purpose: Capture and stream real-time video from onboard camera for analysis and transmission.
"""

import cv2
from core.debug_logger import DebugLogger

logger = DebugLogger()

class CameraStream:
    def __init__(self, camera_index=0, resolution=(640, 480), fps=30):
        self.camera_index = camera_index
        self.resolution = resolution
        self.fps = fps
        self.cap = None

    def start_stream(self):
        self.cap = cv2.VideoCapture(self.camera_index)
        if not self.cap.isOpened():
            logger.error("[CAMERA STREAM] Failed to open camera.")
            return False

        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.resolution[0])
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.resolution[1])
        self.cap.set(cv2.CAP_PROP_FPS, self.fps)
        logger.info("[CAMERA STREAM] Camera stream started.")
        return True

    def read_frame(self):
        if self.cap is None:
            logger.warning("[CAMERA STREAM] Stream not started.")
            return None

        ret, frame = self.cap.read()
        if not ret:
            logger.error("[CAMERA STREAM] Failed to read frame.")
            return None
        return frame

    def stop_stream(self):
        if self.cap:
            self.cap.release()
            logger.info("[CAMERA STREAM] Stream stopped.")

if __name__ == "__main__":
    cam = CameraStream()
    if cam.start_stream():
        while True:
            frame = cam.read_frame()
            if frame is not None:
                cv2.imshow("Live Feed", frame)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
        cam.stop_stream()
        cv2.destroyAllWindows()
