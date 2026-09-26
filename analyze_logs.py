from dotenv import load_dotenv
load_dotenv()

import os
import requests

def send_discord_alert(message):
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
    if not webhook_url:
        return
    try:
        requests.post(webhook_url, json={"content": message}, timeout=5)
    except requests.RequestException as e:
        print("Failed to send Discord alert:", e)

from datetime import datetime
import time

def watch_file(file_path, config):
    recent_by_ip = {}
    already_alerted = set()
    last_status_alert = {}
    cooldown = config.get("alert_cooldown_seconds", 5)

    with open(file_path, "r") as file:
        file.seek(0, 2)
        try:
            while True:
                line = file.readline()
                if line == "":
                    time.sleep(0.5)
                    continue

                parsed = parse_line(line)
                ip = parsed["ip"]

                if parsed["status"] >= config["error_status_threshold"]:
                    last_time = last_status_alert.get(ip)
                    if last_time is None or (parsed["timestamp"] - last_time).total_seconds() >= cooldown:
                        msg = f"ALERT: {parsed['status']} from {ip} on {parsed['path']}"
                        print(msg)
                        last_status_alert[ip] = parsed["timestamp"]

                recent_by_ip.setdefault(ip, []).append(parsed["timestamp"])
                window = config["suspicious_ip_window_seconds"]
                threshold = config["suspicious_ip_request_count"]

                recent_by_ip[ip] = [
                    t for t in recent_by_ip[ip]
                    if (parsed["timestamp"] - t).total_seconds() <= window
                ]

                if len(recent_by_ip[ip]) >= threshold:
                    if ip not in already_alerted:
                        msg = f"SUSPICIOUS: {ip} made {len(recent_by_ip[ip])} requests within {window}s"
                        print(msg)
                        send_discord_alert(msg)
                        already_alerted.add(ip)
                else:
                    already_alerted.discard(ip)

        except KeyboardInterrupt:
            print("\nStopped watching.")

import argparse

def get_args():
    parser = argparse.ArgumentParser(description="Analyze web server access logs")
    parser.add_argument("--file", default="access.log", help="Path to the log file")
    parser.add_argument("--watch", action="store_true", help="Watch the file for new entries in real time")
    return parser.parse_args()

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
def load_logs(file_path="access.log"):
    alllogs = []
    with open(file_path, "r") as file:
        for line_num, line in enumerate(file,1):
            if line_num > 500:
                break
            if not line.strip():
                continue

            singleline = parse_line(line)
            alllogs.append(singleline)
    return alllogs

import json

def load_config(path="config.json"):
    with open(path, "r") as file:
        return json.load(file)

def find_suspicious_ips(logs_by_ip, request_threshold, window_seconds):
    suspicious_ips = []
    for ip, timestamps in logs_by_ip.items():
        if len(timestamps) < request_threshold:
            continue
        timestamps = sorted(timestamps)
        for i in range(len(timestamps) - request_threshold + 1):
            start_time = timestamps[i]
            end_time = timestamps[i + request_threshold - 1]
            if (end_time - start_time).total_seconds() <= window_seconds:
                suspicious_ips.append(ip)
                break
    return suspicious_ips

def main():
    args = get_args()
    config = load_config()
    path_counter = {}
    ip_counter = {}
    logs_by_ip = {}
    max_status = 0

    logs = load_logs(args.file)

    for log in logs:
        ip = log["ip"]
        logs_by_ip.setdefault(ip, []).append(log["timestamp"])
        if log["status"] >= config["error_status_threshold"]:
            max_status += 1
        path_counter[log["path"]] = path_counter.get(log["path"], 0) + 1
        ip_counter[ip] = ip_counter.get(ip, 0) + 1

    suspicious = find_suspicious_ips(
        logs_by_ip,
        config["suspicious_ip_request_count"],
        config["suspicious_ip_window_seconds"],
    )

    most_used_path = max(path_counter, key=path_counter.get)
    most_used_ip = max(ip_counter, key=ip_counter.get)

    print(max_status, "amount of logs had status requests above 400")
    print(most_used_path, "is the path that got hit the most")
    print(most_used_ip, "is the ip that made the most requests")
    print("Suspicious IPs:", suspicious)

    if args.watch:
        print(f"\nWatching {args.file} for new entries... (Ctrl+C to stop)")
        watch_file(args.file, config)

if __name__ == "__main__":
    main()