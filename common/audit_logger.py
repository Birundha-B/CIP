import csv
import os
from datetime import datetime


LOG_FILE = "audit_log.csv"


def log_audit(sender, subject, department, confidence, decision):

    file_exists = os.path.isfile(LOG_FILE)

    with open(LOG_FILE, "a", newline="", encoding="utf-8") as f:

        writer = csv.writer(f)

        if not file_exists:
            writer.writerow([
                "timestamp",
                "sender",
                "subject",
                "department",
                "confidence",
                "decision"
            ])

        writer.writerow([
            datetime.now(),
            sender,
            subject,
            department,
            confidence,
            decision
        ])

    print(" Audit log saved")