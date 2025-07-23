# UAV Surveillance Drone System
Autonomous traffic surveillance drone using computer vision and AI to detect road violations, track vehicle behavior, and assist emergency response systems through real-time monitoring. A modular Raspberry Pi–powered UAV (Unmanned Aerial Vehicle) designed to perform smart traffic monitoring, AI-assisted violation detection, and rapid emergency response. Built with robust computer vision, gesture recognition, and intelligent navigation capabilities.

## 🚀 Features

### 🌄 Surveillance & Monitoring

* Real-time video streaming from drone-mounted camera
* Object detection (vehicles, persons, etc.)
* Speed estimation using pixel-to-meter calibration
* License plate reading via OCR
* Gesture detection for traffic signals or SOS

### 🚨 Emergency & Alert System

* Automatic alert generation for:

  * Overspeeding
  * Dangerous driving behavior
  * Emergency gestures
* Sends event metadata and video snapshots to command center

### 🛂 Dual Flight Modes

* **Autonomous Navigation** with AI decision-making
* **Manual Override** using RC joystick

### 🔄 Return-to-Base Function

* Battery level monitored continuously
* Auto-returns to base if battery < 25% or system fault occurs

## 📊 System Architecture

core/
|-- camera_stream.py
|-- object_detector.py
|-- gesture_detector.py
|-- speed_estimator.py
|-- ocr_plate_reader.py
|-- alert_system.py
|-- diagnostics.py
|-- manual_control.py
|-- navigation.py
|-- mode_switcher.py
|-- config.py
|-- debug_logger.py
|-- logger.py
|-- __init__.py

Main/
|-- main.py
|-- test_runner.py

Assets/
|-- model.tflite
|-- labelmap.txt

## 📈 Requirements

Install dependencies from `requirements.txt`:

```bash
pip install -r requirements.txt
```

Ensure Raspberry Pi camera is enabled:

```bash
sudo raspi-config
# Enable camera interface
```

---

## 🛬 Getting Started

### 1. Run Diagnostics

```bash
python core/diagnostics.py
```

### 2. Launch Mission (Autonomous or Manual)

```bash
python main.py
```

### 3. Run Tests (Optional)

```bash
python test_runner.py
```

---

## 🧰 Hardware Integration

* **Camera**: Pi Camera V2 or USB webcam
* **RC Controller** (for manual mode)
* **GPS module** (optional)
* **SIM7600E-H 4G LTE Module,** (optional)
* **LiPo Battery + Power Monitor**

---

## 🚧 Safety Failsafes

* Full system diagnostics before mission start
* Live performance logging
* Auto emergency landing / return if faults detected

---

## 🔧 Developers

Group 4A (Final Year Engineering Project)

Supervised by: Dr. P.O. Tawiah

University of Kwame Nkrumah University of Science and Technology

---

## ✅ TODO / Roadmap

* [x] Basic AI + Detection Pipeline
* [x] Dual Mode Control
* [x] Diagnostics
* [x] Speed + Plate Estimation
* [ ] Cloud logging / Remote dashboard
* [ ] Model pruning / optimization
* [ ] Auto-charging station integration

---

## 🌎 License

MIT License - free for research and educational purposes.
