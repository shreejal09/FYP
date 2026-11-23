# logger.py
# Saves our decisions to a JSON file so we have an audit trail.

import json
import os
from datetime import datetime

# We will save all logs into this file
LOG_FILE = "logs/audit.log"


def save_verdict(verdict):
    # Make sure the logs folder exists
    os.makedirs("logs", exist_ok=True)

    # Convert our Verdict object into a dictionary
    data = {
        "time": datetime.now().isoformat(),
        "tool": verdict.tool_name,
        "decision": verdict.decision,
        "layer": verdict.layer,
        "reason": verdict.reason,
        "findings": []
    }

    # Add any findings if they exist
    for f in verdict.findings:
        data["findings"].append({
            "rule": f.rule,
            "severity": f.severity,
            "reason": f.reason
        })

    # Write the data to the log file (append mode)
    with open(LOG_FILE, "a") as file:
        file.write(json.dumps(data) + "\n")
        
    print("Logged:", data)