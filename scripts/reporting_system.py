import logging
import os
import json
import threading
from datetime import datetime

class ReportingSystem:
    def __init__(self, log_dir="logs"):
        self.log_dir = log_dir
        os.makedirs(self.log_dir, exist_ok=True)
        self.log_file = os.path.join(self.log_dir, "agent_activity.log")

        # Create a dedicated logger for the ReportingSystem
        self.logger = logging.getLogger("ReportingSystemLogger")
        self.logger.setLevel(logging.INFO)

        # Create a file handler for the logger
        file_handler = logging.FileHandler(self.log_file)
        file_handler.setLevel(logging.INFO)

        # Create a logging format
        formatter = logging.Formatter('%(asctime)s - %(message)s')
        file_handler.setFormatter(formatter)

        # Add the file handler to the logger
        self.logger.addHandler(file_handler)

        self.lock = threading.Lock()

    def log_activity(self, activity):
        with self.lock:
            self.logger.info(activity)

    def generate_report(self):
        report = {
            "timestamp": datetime.now().isoformat(),
            "activities": []
        }
        with self.lock:
            with open(self.log_file, "r") as f:
                for line in f:
                    report["activities"].append(line.strip())
            report_file = os.path.join(self.log_dir, f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
            with open(report_file, "w") as f:
                json.dump(report, f, indent=4)
        return report_file

if __name__ == "__main__":
    reporting_system = ReportingSystem()
    reporting_system.log_activity("Agent started.")
    reporting_system.log_activity("Performed reconnaissance on target 127.0.0.1.")
    report_file = reporting_system.generate_report()
    print(f"Report generated: {report_file}")
