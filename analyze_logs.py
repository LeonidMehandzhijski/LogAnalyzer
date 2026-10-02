import argparse

from log_utils import load_config, parse_line

def get_args():
    parser = argparse.ArgumentParser(description="Analyze web server access logs")
    parser.add_argument("--file", default="access.log", help="Path to the log file")

    return parser.parse_args()

def load_logs(file_path="access.log"):
    all_logs = []
    with open(file_path, "r") as file:
        for line in file:
            if not line.strip():
                continue
            single_line = parse_line(line)
            all_logs.append(single_line)
    return all_logs

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

def summarize_logs(logs, config):
    ip_counter = {}
    logs_by_ip = {}
    error_count = 0
    path_counter = {}
    for log in logs:
        ip = log["ip"]
        logs_by_ip.setdefault(ip, []).append(log["timestamp"])
        if log["status"] >= config["error_status_threshold"]:
            error_count += 1
        path_counter[log["path"]] = path_counter.get(log["path"], 0) + 1
        ip_counter[ip] = ip_counter.get(ip, 0) + 1

    suspicious_ips = find_suspicious_ips(
         logs_by_ip,
        config["suspicious_ip_request_count"],
        config["suspicious_ip_window_seconds"],
    )

    most_used_path = max(path_counter, key=path_counter.get)
    most_used_ip = max(ip_counter, key=ip_counter.get)

    return {
        "error_count": error_count,
        "most_used_path": most_used_path,
        "most_used_ip": most_used_ip,
        "suspicious_ips": suspicious_ips,
    }

def main():
    args = get_args()
    config = load_config()

    logs = load_logs(args.file)
    if not logs:
        print("No logs found.")
        return

    summary = summarize_logs(logs, config)

    print(summary["error_count"], "amount of logs had status requests greater than or equal to ", config["error_status_threshold"])
    print(summary["most_used_path"], "is the path that got hit the most")
    print(summary["most_used_ip"], "is the ip that made the most requests")
    print("Suspicious IPs:", summary["suspicious_ips"])

if __name__ == "__main__":
    main()
