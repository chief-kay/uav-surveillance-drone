"""
OCR Plate Reader Module
Author: Group 4A
Purpose: Extracts license plate text from detected vehicle frames
"""

import cv2
import pytesseract

class OCRPlateReader:
    def __init__(self, tesseract_cmd: str = None):
        if tesseract_cmd:
            pytesseract.pytesseract.tesseract_cmd = tesseract_cmd
        self.config = '--oem 3 --psm 8 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-'

    def read_plate(self, frame, bbox):
        """
        Crops the bounding box around a car plate and applies OCR
        :param frame: Full camera frame
        :param bbox: Bounding box of vehicle (x1, y1, x2, y2)
        :return: Extracted text or None
        """
        x1, y1, x2, y2 = bbox
        plate_region = frame[y1:y2, x1:x2]

        # Preprocess for better OCR
        gray = cv2.cvtColor(plate_region, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (3, 3), 0)
        _, thresh = cv2.threshold(blur, 150, 255, cv2.THRESH_BINARY_INV)

        text = pytesseract.image_to_string(thresh, config=self.config)
        plate = text.strip().replace("\n", "")

        if len(plate) >= 6:
            print(f"[PLATE DETECTED] {plate}")
            return plate
        return None

if __name__ == "__main__":
    reader = OCRPlateReader()
    # Example usage: reader.read_plate(frame, [x1, y1, x2, y2])
