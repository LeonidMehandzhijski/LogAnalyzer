import os
import time
import requests
import argparse

from dotenv import load_dotenv
from log_utils import load_config, parse_line

load_dotenv()

def send_discord_alert(message):
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
    if not webhook_url:
        return
    try:
        requests.post(webhook_url, json={"content": message}, timeout=5)
    except requests.RequestException as error:
        print("Failed to send Discord alert:", error)

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

def get_args():
    parser = argparse.ArgumentParser(description="Monitor logs for suspicious IPs")
    parser.add_argument("--file", default="access.log", help="Path to the log file")
    return parser.parse_args()

def main():
    args = get_args()
    config = load_config()

    print(f"Watching {args.file} for new entries... (Ctrl+C to stop)")
    watch_file(args.file, config)

if __name__ == "__main__":
    main()