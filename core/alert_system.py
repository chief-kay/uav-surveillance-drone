"""
Alert System Module
Author: Group 4A
Purpose: Handles verbal alerts, message dispatch, and simulated emergency communication
"""

import pyttsx3
from datetime import datetime

class AlertSystem:
    def __init__(self):
        self.engine = pyttsx3.init()

    def speak_alert(self, message: str):
        """Converts alert message to speech."""
        print(f"[SPEAKING ALERT] {message}")
        self.engine.say(message)
        self.engine.runAndWait()

    def format_alert_message(self, event: str, location: str = "Ayeduase Road, Kumasi") -> str:
        """Creates a structured verbal alert."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return (
            f"This is Drone Unit 4A. At {timestamp}, {event} was detected at {location}. "
            f"Immediate assistance is requested."
        )

    def trigger_alert(self, event: str):
        """High-level function to trigger full verbal alert cycle."""
        alert_message = self.format_alert_message(event)
        self.speak_alert(alert_message)
        return alert_message

if __name__ == "__main__":
    system = AlertSystem()
    system.trigger_alert("a traffic obstruction due to illegally parked vehicles")
