import json

from datetime import datetime

def parse_line(line):
    clean_line = line.strip()
    timestamp_str, ip, method, path, status = clean_line.rsplit(" ", 4)
    status_int = int(status)
    timestamp_dt = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
    log_data = {
        "timestamp": timestamp_dt,
        "ip": ip,
        "method": method,
        "path": path,
        "status": status_int,
    }
    return log_data

def load_config(path="config.json"):
    with open(path, "r") as file:
        return json.load(file)
